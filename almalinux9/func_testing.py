import os
import requests
import pytest

class TestFuncTesting:
    
    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.server_id = os.environ.get('serverId')
        self.auth_client_id = os.environ.get('clientId')
        self.auth_client_secret = os.environ.get('secret')
        self.cwm_url = os.environ.get('cwm_url')
        self.cwm_headers = {
            "content-type": "application/json",
            "AuthClientId": self.auth_client_id,
            "AuthSecret": self.auth_client_secret
        }

    @pytest.mark.skip
    def test_cwm_auth(self):
        url = "https://staging.cloudwm.com/service/authenticate"
        payload = {
            "clientId": self.auth_client_id,
            "secret": self.auth_client_secret
        }
        response = requests.request("POST", url, headers=self.cwm_headers, json=payload)
        print(response.text)
        
        # Add any assertions related to auth test here
    
    
    @pytest.mark.flaky(reruns=5, reruns_delay=60)
    def test_cwm_cpu(self):
        url = f"https://{self.cwm_url}/service/server/{self.server_id}/cpu"
        payload = "{\"cpu\":\"6B\"}"
        response = requests.request("PUT", url, headers=self.cwm_headers, data=payload)
        print(response.text)

        assert 200 <= response.status_code < 300, f"Expected success status code, got {response.status_code}"
        
        response_content = response.json()
        if isinstance(response_content, dict):  # Check if the response is a dictionary
            assert "errors" not in response_content, f"Found errors in response: {response_content['errors']}"

    @pytest.mark.flaky(reruns=3, reruns_delay=30)
    def test_cwm_resize_disk(self):
        url = f"https://{self.cwm_url}/service/server/{self.server_id}/disk"

        payload = "{\"size\":\"20\",\"index\":\"0\",\"provision\":\"1\"}"
        response = requests.request("PUT", url, headers=self.cwm_headers, data=payload)

        print(response.text)

        assert 200 <= response.status_code < 300, f"Expected success status code, got {response.status_code}"
        
        response_content = response.json()
        if isinstance(response_content, dict):  # Check if the response is a dictionary
            assert "errors" not in response_content, f"Found errors in response: {response_content['errors']}"