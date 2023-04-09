import json
import requests

"""
Modify these please
"""
username = "cisco"
password = "cisco"

ip_addr =  "10.10.20.177"
endpoints = "/api/node/mo/sys/ipv4/inst/dom-default.json?query-target=children"
payload = None
def aaa_login(username, password, ip_addr):
    payload = {
        'aaaUser' : {
            'attributes' : {
                'name' : username,
                'pwd' : password
                }
            }
        }
    url = "https://" + ip_addr + "/api/aaaLogin.json"
    auth_cookie = {}

    response = requests.request("POST", url, data=json.dumps(payload),verify=False)
    if response.status_code == requests.codes.ok:
        data = json.loads(response.text)['imdata'][0]
        token = str(data['aaaLogin']['attributes']['token'])
        auth_cookie = {"APIC-cookie" : token}

    #print ()
    #print ("aaaLogin RESPONSE:")
    #print (json.dumps(json.loads(response.text), indent=2))

    return response.status_code, auth_cookie


def aaa_logout(username, ip_addr, auth_cookie):
    payload = {
        'aaaUser' : {
            'attributes' : {
                'name' : username
                }
            }
        }
    url = "https://" + ip_addr + "/api/aaaLogout.json"

    response = requests.request("POST", url, data=json.dumps(payload),
                                cookies=auth_cookie,verify=False)

    #print ()
    #print ("aaaLogout RESPONSE:")
    #print (json.dumps(json.loads(response.text), indent=2))
    #print ()


def get(ip_addr, auth_cookie, url, payload):
    response = requests.request("GET", url, data=json.dumps(payload),
                                cookies=auth_cookie,verify=False)

    #print ()
    #print ("GET RESPONSE:")
    #print(response.json())
    return response.json()
    #print (json.dumps(json.loads(response.text), indent=2))


if __name__ == '__main__':
    status, auth_cookie = aaa_login(username, password, ip_addr)
    if status == requests.codes.ok:
        url = "https://" + ip_addr + endpoints 
        get_response=get(ip_addr, auth_cookie, url, payload)
        #print(get_response['imdata'])
        for interfaces in get_response['imdata']:
            print(interfaces['ipv4If']['attributes']['dn'],interfaces['ipv4If']['attributes']['id'])
            #print ()
        aaa_logout(username, ip_addr, auth_cookie)