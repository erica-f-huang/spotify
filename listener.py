from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, urlencode
import webbrowser

# from main import CLIENT_ID, REDIRECT_URI

auth_code = None

def get_auth_url(client_id: string, redirect_uri: string):
    body = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "user-top-read"
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