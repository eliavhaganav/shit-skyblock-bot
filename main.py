import requests
from API_KEY import key
from pprint import pprint
import base64
import io
import gzip
from nbt import nbt

# Set the player name
player_name = "AnAverageBigBou"

def get_player_uuid(api_key, player_name):
    try:
        url_uuid = f"https://api.hypixel.net/player?key={api_key}&name={player_name}"
        response_uuid = requests.get(url_uuid)
        data_uuid = response_uuid.json()

        print("Raw UUID Response:")
        pprint(data_uuid)

        if data_uuid["success"]:
            return data_uuid.get("player", {}).get("uuid")
    except Exception as e:
        print(f"Error retrieving UUID: {e}")

    return None

def decode_nbt_data(nbt_data):
    try:
        data = nbt.NBTFile(fileobj = io.BytesIO(base64.b64decode(nbt_data)))
        return data
    except Exception as e:
        print(f"Error decoding NBT data: {e}")
    return None
def get_talisman_bag_data(api_key):
    profileIndex = 0
    try:
        # Get player UUID
        player_uuid = get_player_uuid(api_key, player_name)
        if player_uuid:
            url_profiles = f"https://api.hypixel.net/skyblock/profiles?key={api_key}&uuid={player_uuid}"
            response_profiles = requests.get(url_profiles)
            data_profiles = response_profiles.json()
            if data_profiles["success"]:
                profiles = data_profiles.get("profiles", [])
                tali_bag = profiles[profileIndex].get("members").get(player_uuid).get("talisman_bag").get("data")
                tali_data = decode_nbt_data(tali_bag)
                tag_list = tali_data['i']
                for tag_compound in tag_list:
                    if 'tag' in tag_compound:
                        print(tag_compound['tag']['ExtraAttributes']['id'])  # Print id of talisman
    except Exception as e:
        print(f"Error retrieving talisman_bag data: {e}")
        
# Get talisman_bag data for the specified player
get_talisman_bag_data(key)