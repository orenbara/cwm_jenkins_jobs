import os
import requests

class FuncTesting:

    def __init__(self, message):
        self.message = message

    def greet(self):
        return self.message

def test_cwm_functions():
    # Authenticate to CWM:
    
    # Fetching values from Jenkins environment variables
    client_id = os.environ.get('clientId')
    secret_key = os.environ.get('secret')

    url = "https://staging.cloudwm.com/service/authenticate"

    payload = {
        "clientId": client_id,
        "secret": secret_key
    }

    headers = {
      "Content-Type": "application/json"
    }
    response = requests.request("POST", url, headers=headers, json=payload)

    print(response.text)

  