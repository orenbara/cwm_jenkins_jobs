import os
import requests

class FuncTesting:

    def __init__(self, server_id, auth_client_id,auth_client_secret, cwm_url):
        self.cwm_headers = {
            "content-type": "application/json",
            "AuthClientId": auth_client_id,
            "AuthSecret": auth_client_secret
        }
        self.server_id = server_id
        self.cwm_url = cwm_url
    
    def test_cwm_auth(self):
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
    
    def test_cwm_cpu(self):
        url = f"https://{self.cwm_url}/service/server/{self.server_id}/cpu"

        payload = "{\"cpu\":\"2B\"}"
        
        response = requests.request("PUT", url, headers=self.cwm_headers, data=payload)
        
        print(response.text)
        return response
        
def test_cwm_functions():
    # variables:
    server_id = os.environ.get('serverId')
    auth_client_id = os.environ.get('clientId')
    auth_client_secret = os.environ.get('secret')
    cwm_url = os.environ.get('cwm_url')

    tester = FuncTesting(server_id,auth_client_id ,auth_client_secret, cwm_url)
    
    # Authenticate test to CWM:        
    #tester.test_cwm_auth()
    
    
    ################ Test CPU ################
    response = tester.test_cwm_cpu()
    
    # Check the HTTP status code
    assert 200 <= response.status_code < 300, f"Expected success status code, got {response.status_code}"
    response_content = response.json()
    if isinstance(response_content, dict):  # Check if the response is a dictionary
        assert "errors" not in response_content, f"Found errors in response: {response_content['errors']}"