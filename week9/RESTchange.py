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



def main():
    avail_devices = ['10.10.20.177','10.10.20.178']
    checkbool = True
    while checkbool == True:
        address = input("by IP; What device are we editing?\n")
        #checkbool = IPchecker(address)
    #while checkbool == True:
        #address = input("by IP; What device are we editing?\n")
        checkbool = verify_addy_is_present(address,avail_devices)
    #address = '10.10.20.177'
    cookie = getCookie(address)
    print(cookie)
    nameresponse = what_hostname(address,cookie)
    print(nameresponse)

def verify_addy_is_present(address,devices):
    #just verify the req ip addy is in my list -o- devices
    
    checkbool = True
    if address in devices:
        checkbool = False
    else:
        print("thats not an availible device")
        checkbool = True
    return checkbool

'''def IPchecker(ip_ask): #verify valid IP but not if present in list of devices' IPs
    
    #check_number =ip_ask.replace(".","")
    if check_number.isnumeric(): 
        IP_check = ip_ask.split(".") #i need to check them individually
        if len(IP_check) == 4:
            A = int(IP_check[0])
            B = int(IP_check[1])
            C = int(IP_check[2])
            D = int(IP_check[3])
            if A <= 255 and B <= 255 and C <= 255 and D <= 255:
                #print(f"{ip_check} is valid")
                    valid_bool=False
                    #return valid_bool
            else:
                #print("needs to be a valid IP address")
                valid_bool = True
        else:
            #print("need to be a properly formatted IP address(3 digets, dot 3 more. 4 groups total)")                
            valid_bool = True
    else:
        #print("needs to be a valid IP address(with numbers)")
        valid_bool = True
    return valid_bool'''

def what_hostname(address,cookie):
    #this will just ask for a new host name and pass it to device another function within will verifiy the hostname
    checkbool = True
    while checkbool == True:
        name=input("what is the new hostname?\n")
        checkbool =verifyname(name)
    url = "https://"+address+"/api/mo/sys.json"
    headers = {
    'Content-Type' : 'text/plain',
    'Cookie' : 'APIC-Cookie='+cookie
    }
    payload = {
    "topSystem": {
        "attributes": {
        "name": name
        }
    }
    }
    response=requests.request("POST", url, verify= False,headers=headers,data=json.dumps(payload))
    return response

def verifyname(host_name):
    #verify hostname is only alphanumberic and the 1st char is a letter
    if host_name.isalnum() and host_name[0].isalpha():#isalnum from w3schools                        
        checkif = False
    else:
        print("ERROR: needs to alphanumeric")
        checkif = True
    return checkif


if __name__== "__main__" :
    main()

# _________            .___       ___.                ____.            .__      __________         __         .__     
# \_   ___ \  ____   __| _/____   \_ |__ ___.__.     |    | ____  _____|  |__   \______   \_____ _/  |_  ____ |  |__  
# /    \  \/ /  _ \ / __ |/ __ \   | __ <   |  |     |    |/  _ \/  ___/  |  \   |     ___/\__  \\   __\/ ___\|  |  \ 
# \     \___(  <_> ) /_/ \  ___/   | \_\ \___  | /\__|    (  <_> )___ \|   Y  \  |    |     / __ \|  | \  \___|   Y  \
#  \______  /\____/\____ |\___  >  |___  / ____| \________|\____/____  >___|  /  |____|    (____  /__|  \___  >___|  /
#         \/            \/    \/       \/\/                          \/     \/                  \/          \/     \/ 