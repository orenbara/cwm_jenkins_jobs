import os
import requests
import pytest
import json
import time


class TestFuncTesting:

 # Utility Functions:
    def get_snapshot_id(self):
        url = f"https://staging.cloudwm.com/service/server/{self.server_id}/snapshots"
        response = requests.request("GET", url, headers=self.cwm_headers)
        print(response.text)
        parsed_response = json.loads(response.text)
        if len(parsed_response) == 0:
            print("The response is empty - no snapshots")
            return -1
        else:
            id_value = parsed_response[0]['id']
            print(id_value)
            return id_value


    def delete_snapshot(self):
        snapshot_problem = 1
        for i in range(3):
            snapshot_id = self.get_snapshot_id()
            if snapshot_id == -1:
                snapshot_problem = 0
                break
            else:
                # id of snapshot was captured
                url = f"https://{self.cwm_url}/service/server/{self.server_id}/snapshot"
                payload = f'{{"snapshotId":{snapshot_id}}}'
                response = requests.request("delete", url, headers=self.cwm_headers, data=payload)
                print(response.text)
                response_content = response.json()
                if isinstance(response_content, dict):
                    assert "errors" not in response_content, f"Found errors in response: {response_content['errors']}"
                    time.sleep(10)
                else:
                    snapshot_problem = 0
                    break  
        if snapshot_problem != 0:
            assert False
        else:
            return True


################# TESTS ###############
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
        if self.delete_snapshot() == False:
            print("Problem with snapshot")
            assert False
    
        url = f"https://{self.cwm_url}/service/server/{self.server_id}/cpu"
        payload = "{\"cpu\":\"2B\"}"
        response = requests.request("PUT", url, headers=self.cwm_headers, data=payload)
        print(response.text)
        assert 200 <= response.status_code < 300, f"Expected success status code, got {response.status_code}"
        response_content = response.json()
        if isinstance(response_content, dict):  # Check if the response is a dictionary
            assert "errors" not in response_content, f"Found errors in response: {response_content['errors']}"


    @pytest.mark.flaky(reruns=3, reruns_delay=30)
    def test_cwm_resize_disk(self):
        if self.delete_snapshot() == False:
            print("Problem with snapshot")
            assert False
            
        url = f"https://{self.cwm_url}/service/server/{self.server_id}/disk"
        payload = "{\"size\":\"40\",\"index\":\"0\",\"provision\":1}"
        response = requests.request("PUT", url, headers=self.cwm_headers, data=payload)
        print(response.text)
        assert 200 <= response.status_code < 300, f"Expected success status code, got {response.status_code}"
        response_content = response.json()
        if isinstance(response_content, dict):  # Check if the response is a dictionary
            assert "errors" not in response_content, f"Found errors in response: {response_content['errors']}"


    
    