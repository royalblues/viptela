
import requests
import sys
import json
import time
import datetime
import urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class rest_api_lib:
    def __init__(self, vmanage_ip, username, password):
        self.vmanage_ip = vmanage_ip
        self.session = {}
        self.login(self.vmanage_ip, username, password)

    def login(self, vmanage_ip, username, password):
        """Login to vmanage"""
        base_url_str = 'https://%s/'%vmanage_ip
        login_action = '/j_security_check'

        #Format data for loginForm
        login_data = {'j_username' : username, 'j_password' : password}

        #Url for posting login data
        login_url = base_url_str + login_action
        url = base_url_str + login_url
        sess = requests.session()

        #If the vmanage has a certificate signed by a trusted authority change verify to True
        login_response = sess.post(url=login_url, data=login_data, verify=False)

        if '<html>' in login_response.content:
            print "Login Failed"
            sys.exit(0)

        self.session[vmanage_ip] = sess

        """GET request"""
        url = "https://%s/dataservice/template/policy/vsmart"%(self.vmanage_ip)
        response = self.session[self.vmanage_ip].get(url, verify=False)
        data = response.json()

        for k,v in data.items():
            if k=='data':
                value=v
                #print json.dumps(value, indent=4, sort_keys=True)
                for k1 in value:
                    if k1['policyDescription']=='time-policy':
                        policy_id = k1['policyId']
                        i=0
                        while i<3:
                            i+=1
                            post_request_activate(self,policy_id)
                            time.sleep(75)
                            post_request_deactivate(self,policy_id)
                            time.sleep(75)

def post_request_activate(self, policy_id, headers={'Content-Type': 'application/json'}):
        url = "https://%s/dataservice/template/policy/vsmart/activate/%s"%(self.vmanage_ip,policy_id)
        payload = "{\n }"
        response = self.session[self.vmanage_ip].post(url=url, data=payload, headers=headers, verify=False)
        data = response.content
        print data
        t = datetime.datetime.now()
        print "Policy Activated @ %s "%t


def post_request_deactivate(self, policy_id, headers={'Content-Type': 'application/json'}):
        url = "https://%s/dataservice/template/policy/vsmart/deactivate/%s"%(self.vmanage_ip,policy_id)
        payload = "{\n }"
        response = self.session[self.vmanage_ip].post(url=url, data=payload, headers=headers, verify=False)
        data = response.content
        print data
        t = datetime.datetime.now()
        print "Policy Deactivated @ %s "%t

def main():
    vmanage_ip,username,password = "1.2.3.4","username","password"
    obj = rest_api_lib(vmanage_ip, username, password)
    

if __name__ == "__main__":
    sys.exit(main())
