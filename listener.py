from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, urlencode
import webbrowser
import string
import base64
import requests
import sys

from main import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

auth_code = None

### GETTING NEW TOKEN/ REAUTHORIZING ###
# MAIN FUNCTION: get_refresh_token()
# HELPERS: get_code(), get_auth_url(), and CallbackHandler class
# USAGE: get_refresh_token() return a refresh token which can then be put into the .env file

def get_auth_url(client_id: string, redirect_uri: string):
    body = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "user-top-read ugc-image-upload user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-read-playback-position user-read-recently-played user-library-modify user-library-read "
    }

    return "https://accounts.spotify.com/authorize?" + urlencode(body)

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        query = parse_qs(urlparse(self.path).query)
        auth_code = query.get("code", [None])[0]

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"You can close this tab now.")

    def log_message(self, format, *args):
        pass  # suppress default request logging in the terminal

def get_code(client_id: string, redirect_uri: string):
    global auth_code
    webbrowser.open(get_auth_url(client_id, redirect_uri))

    server = HTTPServer(("127.0.0.1", 8080), CallbackHandler)
    server.handle_request()  # blocks here until ONE request comes in, then stops

    return auth_code

def get_refresh_token():
    to_encode = f"{CLIENT_ID}:{CLIENT_SECRET}"
    to_encode_bytes = to_encode.encode('utf-8')
    encoded_auth = str(base64.b64encode(to_encode_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"

    headers = {
        "Authorization": f"Basic {encoded_auth}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    body = {
        "grant_type": "authorization_code",
        "code": get_code(CLIENT_ID, REDIRECT_URI),
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post(url, headers=headers, data=body)

    if response.status_code != 200:
        sys.exit(f"Failed with status code: {response.status_code}")
    
    # return either refresh or access token depending on parameter
    # if(token_type != "refresh" && token_type != "access"):
    #     print("'token_type' needs to be either 'refresh' or 'access'")
    #     return
    
    print(response.json()["refresh_token"])
    return response.json()["refresh_token"]

if __name__ == "__main__":
    get_refresh_token()