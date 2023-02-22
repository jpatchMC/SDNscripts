import requests
import json
import urllib3
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #shut those warnings up, not a good idea in prod

def commands(name):
    switchuser='cisco'
    switchpassword='cisco'

    url='https://10.10.20.177/ins'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
    {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
        "cmd": "config t",
        "version": 1
        },
        "id": 1
    },
    {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
        "cmd": "hostname "+ name,
        "version": 1
        },
        "id": 2
    }
    ]
    response = requests.post(url,data=json.dumps(payload),verify=False, headers=myheaders,auth=(switchuser,switchpassword)).json()
    return
def isnamegud():
    checkif = True
    while checkif == True:
        host_name= input("change host name to what?:\n")
        if host_name.isalnum():#isalnum from w3schools            
            checkif = False
        else:
            print("ERROR: needs to alphanumeric")
            checkif = True
    return host_name



def main():
    name_change = isnamegud()
    commands(name_change)




if __name__== "__main__" :
    main()