import os
from dotenv import load_dotenv

load_dotenv()  



INFURA_URL = os.getenv("INFURA_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

MORALIS_API_KEY = os.getenv("MORALIS_API_KEY")

SUNO_API_KEY = os.getenv("SUNO_API_KEY")
SUNO_GENERATE_SOUND_API = "https://apibox.erweima.ai/api/v1/generate"
GENERATE_MUSIC_CALLBACK_URL = "https://alzelalmedical.com/api/suno/callback"

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE = "music_database"

SONGS_ABI_PATH = "abis/songs_abi.json"
NFT_ABI_PATH = "abis/nft_abi.json"
COPYRIGHT_ABI_PATH = "abis/copyright_abi.json"
FAN_ABI_PATH = "abis/fan_abi.json"