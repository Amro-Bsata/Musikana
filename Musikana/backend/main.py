from web3 import Web3
from moralis import evm_api
from eth_account.messages import encode_defunct
from eth_account import Account


from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from pymongo import MongoClient


import requests
import json
import secrets
import datetime

import config
from utils import deserialize_song, check_parameter_length,update_one_element_in_fan_area,fan_area_exists,song_exists,get_songs_by_ids,get_permissions,get_song_id_per_contract

###############################################################################################################################################
# Intialisierung der Variable 

app = Flask(__name__)
CORS(app) 
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
jwt = JWTManager(app)



infura_url = config.INFURA_URL

w3 = Web3(Web3.HTTPProvider(infura_url))

contract_address = config.CONTRACT_ADDRESS
songs_abi = json.load(open(config.SONGS_ABI_PATH,"r"))
nft_abi = json.load(open(config.NFT_ABI_PATH,"r"))
copyright_abi = json.load(open(config.COPYRIGHT_ABI_PATH,"r"))
fan_abi = json.load(open(config.FAN_ABI_PATH,"r"))

contract_instance = w3.eth.contract(address=contract_address, abi=songs_abi)

moralis_api_key = config.MORALIS_API_KEY

generate_music_callback_url = config.GENERATE_MUSIC_CALLBACK_URL
suno_api_key = config.SUNO_API_KEY
suno_generate_sound_api = config.SUNO_GENERATE_SOUND_API


client = MongoClient(config.MONGODB_URI)
db = client[config.MONGODB_DATABASE]


nonces = {}

#############################################################################
#Routes


@app.route("/")
def hi():
    return "Beste API der Erde"


@app.route('/next_song_id')
def get_next_song_id():

    if w3.is_connected():
        return([contract_instance.functions.next_song_id().call()])
    else:
        return jsonify({"error": "Blockchain-Verbindung fehlgeschlagen"}), 500



@app.route('/song/<song_id>')
def get_song_per_id(song_id):

    if w3.is_connected():
        song_id = int(song_id)
        if song_id == -1:
            return{}
        song = contract_instance.functions.get_song(song_id).call()
        song = deserialize_song(song)
        return song
    else:
        return jsonify({"error": "Blockchain-Verbindung fehlgeschlagen"}), 500





@app.route('/songs/')
def get_songs():

    if w3.is_connected():
        result = []
        last_id = int(request.args.get("lastID"))
        first_id = int(request.args.get("firstID"))
        next_song_id = get_next_song_id()
        next_song_id = next_song_id[0]
        if last_id > next_song_id:
            last_id = next_song_id
        if first_id >= last_id or first_id < 0:
            return "ERROR: First Id is to big"
        ids = range(first_id,last_id)
        result = get_songs_by_ids(ids,get_song_per_id)
        return result
    else:
        return jsonify({"error": "Blockchain-Verbindung fehlgeschlagen"}), 500



@app.route('/genre/<genre>')
def get_songs_by_genre(genre):
    if w3.is_connected():    
        result = []
        genre = str(genre)
        ids = contract_instance.functions.get_songs_by_genre(genre).call()
        result = get_songs_by_ids(ids,get_song_per_id)
        return result
    else:
        return jsonify({"error": "Blockchain-Verbindung fehlgeschlagen"}), 500




@app.route('/wallet/<owner>')
def get_nfts_per_owner(owner):
    
    result= {"OWNER_NFT":[],"FAN_NFT":[],"COPYRIGHT_NFT":[]}
    

    params = {
    "address": str(owner),  
    "chain": "sepolia", 
    "format": "decimal",
    }

    response = evm_api.nft.get_wallet_nfts(
    api_key=moralis_api_key,
    params=params,
    )

    if  "result" not in response:
        return []
        
    nfts = response["result"]
    for nft in nfts:
        nft_contract_address = nft["token_address"]
        nft_contract_address = w3.to_checksum_address(nft_contract_address)
        try:
            song_id = get_song_id_per_contract(nft_contract_address,w3)
        except Exception:
            song_id = -1 
            
        if song_id != -1:
            nft_type = nft["symbol"]
            song = get_song_per_id(song_id)
            result[nft_type].append(song)

    return result



@app.route('/api/nonce', methods=['GET'])
def get_nonce():
    address = request.args.get('address', '').lower()
    if not address:
        return jsonify({ 'error': 'Address is required' }), 400

    # Create a random hex nonce
    nonce = secrets.token_hex(16)


    nonces[address] = {
    'nonce': nonce,
    'created_at': datetime.datetime.utcnow()
}


    return jsonify({ 'nonce': nonce })




@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    address = data.get('address', '').lower()
    signature = data.get('signature', '')

    nonce_data = nonces.get(address)
    if not nonce_data:
        return jsonify({'error': 'No nonce for this address'}), 400

    # Prüfen ob Nonce älter als 5 Minuten
    if datetime.datetime.now(datetime.timezone.utc) - nonce_data['created_at'] > datetime.timedelta(minutes=5):
        del nonces[address]
        return jsonify({'error': 'Nonce expired'}), 400

    message = encode_defunct(text=nonce_data['nonce'])
    try:
        recovered = Account.recover_message(message, signature=signature)
    except Exception:
        return jsonify({ 'error': 'Invalid signature' }), 400

    #sonst ram läuft voll
    del nonces[address]

    if recovered.lower() == address:
        
        access_token = create_access_token(identity=address,expires_delta=datetime.timedelta(hours=12))  

        return jsonify({ 'success': True, 'access_token': access_token })

    else:
        return jsonify({ 'error': 'Signature verification failed' }), 401


@app.route('/generate',methods=["POST"])
@jwt_required()
def generate_song():

    data_from_caller = request.get_json() 

    song_name = data_from_caller["song_name"]
    prompt = data_from_caller["prompt"]
    styles = data_from_caller["styles"] if type(data_from_caller["styles"]) == str else ",".join(data_from_caller["styles"])
    negative_styles = data_from_caller["negative_styles"] if type(data_from_caller["negative_styles"]) == str else ", ".join(data_from_caller["negative_styles"])

    if check_parameter_length(song_name,prompt,styles,negative_styles) == False:
        return {"code":6969,"msg":f"Error: prompt length limit: 400 characters.\nstyle length limit: 200 characters.\ntitle length limit: 80 characters"}

    payload = json.dumps({
    "prompt": prompt,
    "style": styles,
    "title": song_name,
    "customMode": False,
    "instrumental": False,
    "model": "V3_5",
    "negativeTags": negative_styles,
    "callBackUrl": generate_music_callback_url
    })

    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {suno_api_key}'
    }

    response = requests.request("POST", suno_generate_sound_api , headers=headers, data=payload)

    response_as_json = response.json()
    response_code = response_as_json["code"]

    if response_code != 200:
        return {"code":6969,"msg":f"Error: {response.text}"}

    task_id = response_as_json["data"]["taskId"]

    return {"code":200,"task_id":task_id}




@app.route("/suno/callback", methods=["POST"])
def receive_callback():
    collection = db['callbacks']

    try:
        response = request.json
        data = response.get("data", {})
        task_id = data.get("task_id")
        
        if task_id:
            collection.update_one(
                {"task_id": task_id}, 
                {"$set": {"response": response}}, 
                upsert=True
            )
            return jsonify({"message": "Callback empfangen"}), 200
        else:
            return jsonify({"error": "task_id fehlt"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/suno/<task_id>", methods=["GET"])
def get_callback(task_id):
    collection = db['callbacks']
    try:
        result = collection.find_one({"task_id": task_id})
        
        if result:
            # Die '_id' aus dem MongoDB-Dokument entfernen sonst kommt ein Fehler beider Rückgabe
            result.pop('_id', None)
            return jsonify(result), 200
        else:
            return jsonify({"error": "Task ID nicht gefunden"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/update/fan/area", methods=["POST"])  
@jwt_required()
def update_fan_area():
    current_user = get_jwt_identity()
    try:
        data_from_caller = request.get_json(force=True)

        song_id = data_from_caller["song_id"]
        remixs = data_from_caller["remixs"]
        messages = data_from_caller["chat"]
        music_video = data_from_caller["mv"]
    except Exception as e:
        return jsonify({"status": "error", "message": f"Fehler beim Parsen der Daten: {str(e)}"}), 400

    if not song_id or not song_exists(song_id):
        return jsonify({"status": "error", "message": "Song nicht gefunden"}), 404

    permission = get_permissions(current_user,song_id, get_nfts_per_owner)
    if  permission != "owner":
        return jsonify({"msg":"Error no permession"}),69

    update_results = []
    
    if remixs is not None:
        success = update_one_element_in_fan_area(song_id, "remixs", remixs)
        update_results.append(("remixs", success))
    
    if messages is not None:
        success = update_one_element_in_fan_area(song_id, "chat", messages)
        update_results.append(("chat", success))
    
    if music_video is not None:
        success = update_one_element_in_fan_area(song_id, "mv", music_video)
        update_results.append(("mv", success))

    return jsonify({
        "status": "success",
        "updates": {field: success for field, success in update_results}
    }), 200



@app.route("/create/fan/area", methods=["POST"])  
@jwt_required()
def create_fan_area():
    current_user = get_jwt_identity()

    collection = db['songs']
    try:
        data_from_caller = request.get_json(force=True)
        song_id = data_from_caller["song_id"]
        force_to_create = data_from_caller["force_to_create"]
    except Exception as e:
        return jsonify({
            "status": "Error",
            "msg": f"Fehler beim Lesen der Daten: {str(e)}"
        }), 400

    permission = get_permissions(current_user,song_id, get_nfts_per_owner)
    if permission != "owner":
        return jsonify({"msg":"Error no permession"}),69

    # Prüfen, ob bereits ein Fan-Bereich existiert
    if fan_area_exists(song_id) and not force_to_create:
        return jsonify({
            "status": "Error",
            "msg": f"Das Lied hat bereits eine Fan Area."
        }), 400

    fan_area = {
        "song_id": song_id,
        "remixs": [],
        "chat": [],
        "mv": None
    }

    try:
        result = collection.insert_one(fan_area)
        return jsonify({
            "status": "Success",
            "msg": f"Fan-Bereich für Song {song_id} wurde neu erstellt.",
            "inserted_id": str(result.inserted_id)
        }), 201
    except Exception as e:
        return jsonify({
            "status": "Error",
            "msg": f"Fehler beim Einfügen: {str(e)}"
        }), 500

@app.route("/get/fan/area/<song_id>", methods=["get"])  
@jwt_required()
def get_fan_area(song_id):
    song_id= int(song_id)
    current_user = get_jwt_identity()
    permission = get_permissions(current_user,song_id, get_nfts_per_owner)
    if permission != "fan" and permission != "owner":
        return jsonify({"msg":"Error no permession"}),69
    collection = db['songs']
    if not fan_area_exists(song_id):
        return jsonify({
            "status": "Error",
            "msg": f"Das Lied hat kein Fan Area."
        }), 404

    song = collection.find_one({"song_id": song_id})
    song.pop("_id", None)
    return jsonify(song),200



@app.route("/market/songs", methods=["get"])  
def get_songs_on_market():
    result = []
    next_song_id = get_next_song_id()
    last_id = next_song_id[0]
    ids = range(0,last_id)
    songs = get_songs_by_ids(ids,get_song_per_id)
    for song in songs:
        copyright_nft_contract = song["copyright_nft_contract"]
        copyright_nft_contract = w3.to_checksum_address(copyright_nft_contract)
        nft_contract_instance = w3.eth.contract(address=copyright_nft_contract, abi=copyright_abi)
        max_supply = int(nft_contract_instance.functions.max_supply().call())
        total_supply = int(nft_contract_instance.functions.total_supply().call())
        nfts_to_sell = max_supply - total_supply
        if nfts_to_sell > 0:
            result.append(song)
    
    return result

@app.route("/fannft/remaining/<song_id>", methods=["get"])  
def remaining_fan_nft(song_id):
    song_id = int(song_id)
    song = get_song_per_id(song_id)
    fan_nft_contract = song["fan_nft_contract"]
    fan_nft_contract = w3.to_checksum_address(fan_nft_contract)
    nft_contract_instance = w3.eth.contract(address=fan_nft_contract, abi=fan_abi)
    max_supply = int(nft_contract_instance.functions.max_supply().call())
    total_supply = int(nft_contract_instance.functions.total_supply().call())
    nfts_to_sell = max_supply - total_supply
    if nfts_to_sell > 0:
        return jsonify(True),200
    return jsonify(False),69
###############################################################################################################################################
if __name__ == "__main__":
    app.run()