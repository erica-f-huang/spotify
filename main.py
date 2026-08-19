from dotenv import load_dotenv
import os
import base64
import requests
import sys
import webbrowser

from listener import get_code #listener.py is pt of this project

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
REDIRECT_URI = "http://127.0.0.1:8080"

#NOTE: on 2/16/27 will need to edit this to take in a code (which you get from get_code()) to get new refresh token
def get_token():
    to_encode = f"{CLIENT_ID}:{CLIENT_SECRET}"
    to_encode_bytes = to_encode.encode('utf-8')
    encoded_auth = str(base64.b64encode(to_encode_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": f"Basic {encoded_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    body = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(url, headers=headers, data=body)

    if response.status_code != 200:
        sys.exit(f"Failed with status code: {response.status_code}")
    
    # print(response.json()["refresh_token"])
    return response.json()["access_token"]

# TOKEN = get_token(get_code(CLIENT_ID, REDIRECT_URI))
TOKEN = get_token()

###################################

# either artists or tracks
def top_items(item: string):
    if((item != "artists") and (item != "tracks")):
        print("item has to be either 'artists' or 'tracks'")
        return

    url = f"https://api.spotify.com/v1/me/top/{item}"

    header = {
        "Authorization": f"Bearer {TOKEN}"
    }

    response = requests.get(url, headers=header)

    if response.status_code != 200:
        sys.exit(f"Failed with status code: {response.status_code}")
    
    top_items = response.json()["items"]

    for i in top_items:
        print(i["name"])

    
if __name__ == "__main__":
    top_items("tracks")