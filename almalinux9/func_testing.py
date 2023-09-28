import os
import requests

class FuncTesting:

    self.cwm_headers = {
            "AuthClientId": os.environ.get('clientId'),
            "AuthSecret": os.environ.get('secret'),
            "content-type": "application/json"
    }

    def greet(self):
        return self.message
    
    def cwm_auth(self):
        # Fetching values from Jenkins environment variables
        client_id = os.environ.get('clientId')
        secret_key = os.environ.get('secret')

        url = "https://staging.cloudwm.com/service/authenticate"

        payload = {
            "clientId": client_id,
            "secret": secret_key
        }

        
        response = requests.request("POST", url, headers=self.headers, json=payload)
        print(response.text)
    
    def cwm_cpu(self, serverId: str):
        url = f"https://staging.cloudwm.com/service/server/{serverId}/cpu"

        cpu_value = "4B"  # You'd need to define this
        payload = {"cpu": cpu_value}
        response = requests.request("PUT", url, headers=self.headers, json=payload)
        
        print(response.text)
        return response
        
def test_cwm_functions():
    # variables:
    server_id = os.environ.get('serverId')
    
    tester = FuncTesting()
    
    # Authenticate test to CWM:        
    tester.cwm_auth()
    
    # Test change cpu
    tester.cwm_cpu(server_id)
