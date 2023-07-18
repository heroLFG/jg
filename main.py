from flask import Flask, request, Response, send_from_directory
from flask_cors import CORS
import requests
from requests import adapters
import ssl
from urllib3 import poolmanager

class TLSAdapter(adapters.HTTPAdapter):

    def init_poolmanager(self, connections, maxsize, block=False):
        """Create and initialize the urllib3 PoolManager."""
        ctx = ssl.create_default_context()
        ctx.set_ciphers('DEFAULT@SECLEVEL=1')
        self.poolmanager = poolmanager.PoolManager(
                num_pools=connections,
                maxsize=maxsize,
                block=block,
                ssl_version=ssl.PROTOCOL_TLS,
                ssl_context=ctx)

session = requests.session()
session.mount('https://', TLSAdapter())

app = Flask(__name__, static_folder='static')  # define static folder
CORS(app, resources={r"/*": {"origins": ["http://localhost:5000", "http://127.0.0.1:5000"]}})  # replace 'port' with your localhost port number

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def catch_all(path):
    url = f'https://jumpgate-tri.org/{path}'
    print(url)
    try:
        response = session.get(url)
    except Exception as e:
        print(e)
    return Response(response.content, mimetype='application/json')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)  # Runs the server in public mode on port 5000
