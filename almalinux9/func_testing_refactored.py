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
                print("Found a snapshot - trying to delete")
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
                    print("SUCCESFULY deleted the snapshot")
                    snapshot_problem = 0
                    break  
        if snapshot_problem != 0:
            assert False
        else:
            return True
        
    def execute_cwm_func(self, url, payload, http_func, cwm_headers):
      print(f"[EXECUTION_FUNC]:\nURL: {url}\nPAYLOAD: {payload}\nHTTP_FUNC: {http_func}")
      if self.delete_snapshot() == False:
          print("Problem with snapshot")
          assert False
      response = requests.request(http_func , url, headers=cwm_headers, json=payload)
      print(response.text)
      assert 200 <= response.status_code < 300, f"Expected success status code, got {response.status_code}"
      response_content = response.json()
      if isinstance(response_content, dict):  # Check if the response is a dictionary
          assert "errors" not in response_content, f"Found errors in response: {response_content['errors']}"

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
        self.new_pass = os.environ.get('new_pass')
        

    


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
    
    
    @pytest.mark.flaky(reruns=5, reruns_delay=15)
    def test_cwm_cpu(self):
        self.execute_cwm_func(url=f"https://{self.cwm_url}/service/server/{self.server_id}/cpu"
                         , payload="{\"cpu\":\"2B\"}", http_func="PUT", cwm_headers=self.cwm_headers)


    @pytest.mark.flaky(reruns=5, reruns_delay=10)
    def test_cwm_ram(self):
        self.execute_cwm_func(url=f"https://{self.cwm_url}/service/server/{self.server_id}/ram"
                         , payload="{\"ram\":\"2048\"}", http_func="PUT", cwm_headers=self.cwm_headers)



    @pytest.mark.flaky(reruns=5, reruns_delay=5)
    def test_cwm_resize_disk(self):
        self.execute_cwm_func(url=f"https://{self.cwm_url}/service/server/{self.server_id}/disk"
                         , payload="{\"size\":\"20\",\"index\":\"0\",\"provision\":1}", http_func="PUT", cwm_headers=self.cwm_headers)


    @pytest.mark.skip
    def test_cwm_add_ip(self):
        '''
        currently network testing is problematic in CWM, there is no api direct support and i dont understand the part after id in the api request:
        https://staging.cloudwm.com/svc/server/564d233e-0ee8-b994-9a59-1caaaac41919/nics/00%3A50%3A56%3A02%3Aa7%3A57/ip
        '''
        if self.delete_snapshot() == False:
            print("Problem with snapshot")
            assert False

    
    @pytest.mark.flaky(reruns=6, reruns_delay=20)
    def test_cwm_add_disk(self):
        self.execute_cwm_func(url=f"https://{self.cwm_url}/service/server/{self.server_id}/disk"
                 , payload="{\"size\": 10,\"provision\": 1}", http_func="POST", cwm_headers=self.cwm_headers)


    @pytest.mark.flaky(reruns=6, reruns_delay=15)
    def test_cwm_remove_disk(self):
        self.execute_cwm_func(url=f"https://staging.cloudwm.com/service/server/{self.server_id}/disk/remove"
                 , payload="{\"index\": 1,\"confirm\": 1}" , http_func="DELETE", cwm_headers=self.cwm_headers)


    @pytest.mark.flaky(reruns=6, reruns_delay=15)
    def test_cwm_add_snapshot(self):
        self.execute_cwm_func(url=f"https://staging.cloudwm.com/service/server/{self.server_id}/snapshot"
                 , payload="{\"name\":\"jenkins_test_snapshot\"}" , http_func="POST", cwm_headers=self.cwm_headers)
        

    @pytest.mark.flaky(reruns=6, reruns_delay=10)
    def test_cwm_remove_snapshot(self):
        self.delete_snapshot()

            

    @pytest.mark.flaky(reruns=6, reruns_delay=5)
    def test_cwm_pass_change(self):
        self.execute_cwm_func(url=f"https://staging.cloudwm.com/service/server/{self.server_id}/password"
                 , payload=f"{{\"password\":\"{self.new_pass}\"}}" , http_func="PUT", cwm_headers=self.cwm_headers)
