import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #shut those warnings up, not a good idea in prod

def getCookie(addr) :

#NX REST API Authen See REST API Reference for format of payload below

    url = "https://"+ addr+"/api/aaaLogin.json"
 
    payload= {"aaaUser" :
              {"attributes" :
                   {"name" : "cisco",
                    "pwd" : "cisco"}
               }
          }

    response = requests.post(url, json=payload, verify = False)
    #print(response.json())
    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]
# create vlan and adds name based on passed in vars
def create_vlan(addr,cookie,vlan_num,vlan_name):
    #no need for "config t" in browser#
    #  vlan # name _
    url = 'https://'+addr+'/api/mo/sys.json'
    headers = {'Content-Type' : 'text/plain','Cookie' : 'APIC-Cookie='+cookie}
    payload ={
    "topSystem": {
        "children": [
        {
            "bdEntity": {
            "children": [
                {
                "l2BD": {
                    "attributes": {
                    "fabEncap": "vlan-"+vlan_num,
                    "name": vlan_name
                    }
                }
                }
            ]
            }
        }
        ]
    }
    }

    response= requests.request("POST",url,data=json.dumps(payload),headers=headers,verify=False)
    #print(response)
    return response
#adds an IP address to created/new vlan based on passed in vars
def add_IP_to_vlan(addr,cookie,vlan_num,IP_addy):
    url = 'https://'+addr+'/api/mo/sys.json'
    headers = {'Content-Type' : 'text/plain','Cookie' : 'APIC-Cookie='+cookie}
    payload ={
    "topSystem": {
        "children": [
        {
            "ipv4Entity": {
            "children": [
                {
                "ipv4Inst": {
                    "children": [
                    {
                        "ipv4Dom": {
                        "attributes": {
                            "name": "default"
                        },
                        "children": [
                            {
                            "ipv4If": {
                                "attributes": {
                                "id": "vlan"+vlan_num
                                },
                                "children": [
                                {
                                    "ipv4Addr": {
                                    "attributes": {
                                        "addr": IP_addy
                                    }
                                    }
                                }
                                ]
                            }
                            }
                        ]
                        }
                    }
                    ]
                }
                }
            ]
            }
        },
        {
            "interfaceEntity": {
            "children": [
                {
                "sviIf": {
                    "attributes": {
                    "adminSt": "up",
                    "id": "vlan"+vlan_num
                    }
                }
                }
            ]
            }
        }
        ]
    }
    }
    response= requests.request("POST",url,data=json.dumps(payload),headers=headers,verify=False)
    #print(response)
    return response
#define hsrp failover address and group based on passed in vars 
def HSRP(addr,cookie,vlan_num,hsrp,hsrp_grp):
    url = 'https://'+addr+'/api/mo/sys.json'
    headers = {'Content-Type' : 'text/plain','Cookie' : 'APIC-Cookie='+cookie}
    payload ={
    "topSystem": {
        "children": [
        {
            "interfaceEntity": {
            "children": [
                {
                "sviIf": {
                    "attributes": {
                    "id": "vlan"+vlan_num
                    }
                }
                }
            ]
            }
        },
        {
            "hsrpEntity": {
            "children": [
                {
                "hsrpInst": {
                    "children": [
                    {
                        "hsrpIf": {
                        "attributes": {
                            "id": "vlan"+vlan_num
                        },
                        "children": [
                            {
                            "hsrpGroup": {
                                "attributes": {
                                "af": "ipv4",
                                "id": hsrp_grp,
                                "ip": hsrp,
                                "ipObtainMode": "admin"
                                }
                            }
                            }
                        ]
                        }
                    }
                    ]
                }
                }
            ]
            }
        }
        ]
    }
}
    response= requests.request("POST",url,data=json.dumps(payload),headers=headers,verify=False)
    return response
#add OSPF ID and area based on passed in input
def add_OSPF(addr,cookie,vlan_num,ospf_ID,ospf_area):
    url = 'https://'+addr+'/api/mo/sys.json'
    headers = {'Content-Type' : 'text/plain','Cookie' : 'APIC-Cookie='+cookie}
    payload={
    "topSystem": {
        "children": [
        {
            "ospfEntity": {
            "children": [
                {
                "ospfInst": {
                    "attributes": {
                    "name": ospf_ID
                    },
                    "children": [
                    {
                        "ospfDom": {
                        "attributes": {
                            "name": "default"
                        },
                        "children": [
                            {
                            "ospfIf": {
                                "attributes": {
                                "advertiseSecondaries": "yes",
                                "area": ospf_area,
                                "id": "vlan"+vlan_num
                                }
                            }
                            }
                        ]
                        }
                    }
                    ]
                }
                }
            ]
            }
        },
        {
            "interfaceEntity": {
            "children": [
                {
                "sviIf": {
                    "attributes": {
                    "id": "vlan"+vlan_num
                    }
                }
                }
            ]
            }
        }
        ]
    }
}

    response= requests.request("POST",url,data=json.dumps(payload),headers=headers,verify=False)
    return response

def Ip_split_add(IP_addy,count):
    octets_and_cidr = IP_addy.split(".")
    last_octet_and_cidr = octets_and_cidr[3].split("/")
    last_octet = last_octet_and_cidr[0]
    cidr = last_octet_and_cidr[1]
    new_last_octet = str(int(last_octet) + count)
    new_octets_and_cidr = octets_and_cidr[:3] + [new_last_octet, cidr]
    new_ip_address = ".".join(new_octets_and_cidr[:-1]) + "/" + new_octets_and_cidr[-1]
    return new_ip_address

def main():
    
    device_address=['10.10.20.177','10.10.20.178']
    vlan_num = input("what vlan number we makin(number only) ")
    vlan_name = input("what are we namin this? ")
    IP_addy = input("what will the IP address for this new vlan on the 1st device be?\nFORMAT #.#.#.#/#\t")
    hsrp_grp=input("what hsrp group? ")
    hsrp = input(f"what will the hsrp address be?\n is should be the same network as {IP_addy} ")
    ospf_ID = input("what ospf process ID? ")#"1"
    area_ospf =  input("what ospf area \nFORMAT #.#.#.#\t")#"0.0.0.0"
    #token = getCookie(device_address)
    #print(token)
    count = 0
    for device in device_address:
        token = getCookie(device)
        print(token)
        mk_vlan = create_vlan(device,token,vlan_num,vlan_name)
        if mk_vlan.status_code == 200:
            print(f"created Vlan{vlan_num} named {vlan_name}!!")
        else:
            print("Error")
        working_IP =Ip_split_add(IP_addy,count)
        add_ip = add_IP_to_vlan(device,token,vlan_num,working_IP)
        if add_ip.status_code == 200:
            print(f"IP if {working_IP} added to Vlan{vlan_num}")
        else:
            print("Error")
        
        hsrp_add=HSRP(device,token,vlan_num,hsrp,hsrp_grp)
        if hsrp_add.status_code == 200:
            print(f"hsrp group {hsrp_grp} with the address of {hsrp} added to Vlan{vlan_num}")
        else:
            print("Error")
        
        ospf_add = add_OSPF(device,token,vlan_num,ospf_ID,area_ospf)
        if ospf_add.status_code == 200:
            print(f"Vlan{vlan_num} added to area {area_ospf} with a proc ID of {ospf_ID}")
        else:
            print("Error")
    count = count+1

if __name__== "__main__" :
    main()

# _________            .___       ___.                ____.            .__      __________         __         .__     
# \_   ___ \  ____   __| _/____   \_ |__ ___.__.     |    | ____  _____|  |__   \______   \_____ _/  |_  ____ |  |__  
# /    \  \/ /  _ \ / __ |/ __ \   | __ <   |  |     |    |/  _ \/  ___/  |  \   |     ___/\__  \\   __\/ ___\|  |  \ 
# \     \___(  <_> ) /_/ \  ___/   | \_\ \___  | /\__|    (  <_> )___ \|   Y  \  |    |     / __ \|  | \  \___|   Y  \
#  \______  /\____/\____ |\___  >  |___  / ____| \________|\____/____  >___|  /  |____|    (____  /__|  \___  >___|  /
#         \/            \/    \/       \/\/                          \/     \/                  \/          \/     \/ 