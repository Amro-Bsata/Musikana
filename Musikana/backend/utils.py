
from pymongo import MongoClient
import config
import json 

client = MongoClient(config.MONGODB_URI)
db = client[config.MONGODB_DATABASE]
nft_abi = json.load(open(config.NFT_ABI_PATH,"r"))


def deserialize_song(data_list):
    if len(data_list) == 0 or data_list is None:
        return {}
    return {
        "song_id": data_list[0],
        "song_name": data_list[1],
        "styles": data_list[2],
        "negative_styles": data_list[3],
        "uri": data_list[4],
        "fan_nft_maxSupply": data_list[5],
        "copyright_nft_maxSupply": data_list[6],
        "copyright_nft_price": data_list[7],
        "owner_nft_contract": data_list[8],
        "fan_nft_contract": data_list[9],
        "copyright_nft_contract": data_list[10],
        "owner": data_list[11]
    }


def check_parameter_length(song_name, prompt, styles, negative_styles):
    if len(prompt) > 400 or len(styles) > 200 or len(negative_styles) > 200 or len(song_name) > 80:
        return False
    return True

# move
def update_one_element_in_fan_area(song_id, element_name, element_value):
    collection = db['songs']
    
    if song_id is None or not song_exists(song_id):
        return False

    update_result = collection.update_one(
        {"song_id": song_id},       
        {"$set": {element_name: element_value}} 
    )


    return update_result.modified_count > 0


#move
def song_exists(song_id) -> bool:
    collection = db['songs']
    song = collection.find_one({"song_id": song_id})
    result = song is not None # true wenn es vorhanden
    return result

#move
def fan_area_exists(song_id) -> bool:
    collection = db['songs']
    
    song = collection.find_one({"song_id": song_id})

    if not song:
        return False  # Song existiert nicht → keine Fan-Area möglich

    # Prüfen, ob die Fan-Area-Felder existieren
    has_fan_area = "remixs" in song and "chat" in song and "mv" in song

    return has_fan_area

def get_songs_by_ids(ids,get_song_per_id):
    result = []
    if ids == None or len(ids) == 0:
        return result

    for song_id in ids:
        song = get_song_per_id(song_id)
        result.append(song)
    return result


def get_permissions(user_address, song_id, get_nfts_per_owner):
    songs = get_nfts_per_owner(user_address)
    for song in songs["OWNER_NFT"]:
        if song["song_id"] == song_id:
            return "owner"

    for song in songs["FAN_NFT"]:
        if song["song_id"] == song_id:
            return "fan"

    return None

def get_song_id_per_contract(contract,w3):
    
    nft_contract_instance = w3.eth.contract(address=contract, abi=nft_abi)
    try:
        song_id = nft_contract_instance.functions.song_id().call() # try except vileleicht ist die nft von anderem collection
    except Exception:
        song_id = -1
    print(song_id)
    return song_id

