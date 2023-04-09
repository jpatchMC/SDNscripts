import requests
import json

def getCookie(addr) :

#NX REST API Authen See REST API Reference for format of payload below

    url = "https://"+ addr + "/api/aaaLogin.json"
 
    payload= {"aaaUser" :
              {"attributes" :
                   {"name" : "cisco",
                    "pwd" : "cisco"}
               }
          }

    response = requests.post(url, json=payload, verify = False)
    #print(response.json())
    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]

def interface_ip4(addr,cookie):
    url = "https://"+addr+"/api/node/mo/sys/ipv4/inst/dom-default.json?query-target=children"
                          
    #auth_cookie={"APIC-cookie" : cookie} can be use interchangable with the "headers" varible format
    payload=None
    headers = {'Content-Type' : 'text/plain','Cookie' : 'APIC-Cookie='+cookie}
    response= requests.request("GET",url,data=json.dumps(payload),headers=headers,verify=False)#cookies=auth_cookie,
    #response = requests.request("GET", url, data=json.dumps(payload), cookies=auth_cookie,verify=False)
    return response.json()

def clean_json_make_table(json):
    for interfaces in json['imdata']:
            print(interfaces['ipv4If']['attributes']['dn'],interfaces['ipv4If']['attributes']['id'])

def main():
    addy='10.10.20.177'
    cookie=getCookie(addy)
    print(cookie)
    int_ip4=interface_ip4(addy,cookie)
    #print(int_ip4)#['imdata'])
    clean_json_make_table(int_ip4)



if __name__== "__main__" :
    main()

# _________            .___       ___.                ____.            .__      __________         __         .__     
# \_   ___ \  ____   __| _/____   \_ |__ ___.__.     |    | ____  _____|  |__   \______   \_____ _/  |_  ____ |  |__  
# /    \  \/ /  _ \ / __ |/ __ \   | __ <   |  |     |    |/  _ \/  ___/  |  \   |     ___/\__  \\   __\/ ___\|  |  \ 
# \     \___(  <_> ) /_/ \  ___/   | \_\ \___  | /\__|    (  <_> )___ \|   Y  \  |    |     / __ \|  | \  \___|   Y  \
#  \______  /\____/\____ |\___  >  |___  / ____| \________|\____/____  >___|  /  |____|    (____  /__|  \___  >___|  /
#         \/            \/    \/       \/\/                          \/     \/                  \/          \/     \/ 