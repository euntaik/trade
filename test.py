import requests

url = "https://api.upbit.com/v1/market/all"

querystring = {"isDetails": "false"}

response = requests.request("GET", url, params=querystring)

print(response.text)


import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode

import requests

access_key = os.environ["UPBIT_OPEN_API_ACCESS_KEY"]
secret_key = os.environ["UPBIT_OPEN_API_SECRET_KEY"]
server_url = os.environ["UPBIT_OPEN_API_SERVER_URL"]

payload = {"access_key": access_key, "nonce": str(uuid.uuid4())}

print(payload)

jwt_token = jwt.encode(payload, secret_key)
authorize_token = "Bearer {}".format(jwt_token)
headers = {"Authorization": authorize_token}

res = requests.get(server_url + "/v1/api_keys", headers=headers)

print(res.json())
