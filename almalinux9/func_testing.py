import os
import requests

class FuncTesting:

    def __init__(self, server_id, auth_client_id,auth_client_secret):
        self.cwm_headers = {
            "AuthClientId": auth_client_id,
            "AuthSecret": auth_client_secret,
            "content-type": "application/json"
        }
        self.server_id = server_id
    
    def cwm_auth(self):
        # Fetching values from Jenkins environment variables
        client_id = os.environ.get('clientId')
        secret_key = os.environ.get('secret')

        url = "https://staging.cloudwm.com/service/authenticate"

        payload = {
            "clientId": client_id,
            "secret": secret_key
        }

        response = requests.request("POST", url, headers=self.cwm_headers, json=payload)
        print(response.text)
    
    def cwm_cpu(self):
        url = f"https://staging.cloudwm.com/service/server/{self.server_id}/cpu"

        cpu_value = "4B"  # You'd need to define this
        payload = {"cpu": cpu_value}
        response = requests.request("PUT", url, headers=self.cwm_headers, json=payload)
        
        print(response.text)
        return response
        
def test_cwm_functions():
    # variables:
    server_id = os.environ.get('serverId')
    auth_client_id = os.environ.get('clientId')
    auth_client_secret = os.environ.get('secret')

    tester = FuncTesting(server_id,auth_client_id ,auth_client_secret)
    
    # Authenticate test to CWM:        
    tester.cwm_auth()
    
    # Test change cpu
    tester.cwm_cpu()
