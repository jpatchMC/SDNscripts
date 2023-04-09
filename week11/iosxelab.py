import requests
import json


def getInts(ip):
    url = "https://"+ip+":443/restconf/data/ietf-interfaces:interfaces"


    username = 'cisco'
    password = 'cisco'
    payload={}
    headers = {
    'Content-Type': 'application/yang-data+json',
    'Accept': 'application/yang-data+json',
    'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm'
    }

    response = requests.request("GET", url, auth = (username,password), verify = False, headers=headers, data=json.dumps(payload))
    return response.json()
#print(response.json)
def printInt(dictionary):
    sort = dictionary['ietf-interfaces:interfaces']['interface']
    for item in sort:
        if item['name'] != "Loopback0":
        #print (f"{item['name']}")
            for addresses in item['ietf-ip:ipv4']['address']:
            
                print(f"{item['name']}\t{addresses['ip']}\t{addresses['netmask']}")

    



def main():
    deviceIP = "10.10.20.175"
    intDict = getInts(deviceIP)  #This gets the interfaces model
    print (intDict)
    printInt(intDict)#['ietf-interfaces:interfaces'])
    



if __name__== "__main__" :
    main()

# _________            .___       ___.                ____.            .__      __________         __         .__     
# \_   ___ \  ____   __| _/____   \_ |__ ___.__.     |    | ____  _____|  |__   \______   \_____ _/  |_  ____ |  |__  
# /    \  \/ /  _ \ / __ |/ __ \   | __ <   |  |     |    |/  _ \/  ___/  |  \   |     ___/\__  \\   __\/ ___\|  |  \ 
# \     \___(  <_> ) /_/ \  ___/   | \_\ \___  | /\__|    (  <_> )___ \|   Y  \  |    |     / __ \|  | \  \___|   Y  \
#  \______  /\____/\____ |\___  >  |___  / ____| \________|\____/____  >___|  /  |____|    (____  /__|  \___  >___|  /
#         \/            \/    \/       \/\/                          \/     \/                  \/          \/     \/ 
