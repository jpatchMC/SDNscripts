#!/usr/bin/env python3

import json
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #shut those warnings up, not a good idea in prod

def add_to_device(device):
    #this will add / append to device inventory
    name= input("what is the name of the device?\t")
    valbool = False
    while valbool==False:
        dev_type= input("what kind of device is this? nxos or iosxe\t")
        dev_type=dev_type.lower()
        valbool=type_enforce(dev_type)    
    valboo=False
    while valboo == False:
        mang_IP=input("what is the management IP address?\t")
        valboo=IPchecker(mang_IP)
    device.append({"hostname":name,"type":dev_type,"managementIP":mang_IP})
    return device
def type_enforce(type):
    #enforce the only two types we want with the same formatting
    #print (type)
    if type == "nxos" or type == "iosxe":
        valbool=True
    else:
        valbool=False
    return valbool
def remove_device(device,dev_del):
    #deletes device based on hostname
    for item in device:
        if item["hostname"] == dev_del:
            device.remove(item)
    return device
def Mod_Device(device,dev_to_mod,key_to_mod,new_value):
    #modify a device based on hostname and supplied key
    for item in device:
        if item["hostname"] == dev_to_mod:
            item[key_to_mod]=new_value
    return device
def write_to_file(device):
    #writes(save) to a .json file as json
    file = open("devices.json","w")
    file.write(json.dumps(device))
    file.close()
def read_file():
    #opens and reads .json file
    with open("devices.json","r")as file:
        device = json.load(file)
    return device

def IPchecker(ip_ask): #ip ask is a string thats a question define in main
    check_number =ip_ask.replace(".","")
    if check_number.isnumeric(): 
        IP_check = ip_ask.split(".") 
        if len(IP_check) == 4:
            A = int(IP_check[0])
            B = int(IP_check[1])
            C = int(IP_check[2])
            D = int(IP_check[3])
            if A <= 255 and B <= 255 and C <= 255 and D <= 255: 
                    valid_bool=True
            else:
                valid_bool = False
        else:            
            valid_bool = False
    else:
        valid_bool = False
    return valid_bool

def getCookie(addr) :

#NX REST API Authen See REST API Reference for format of payload below

    url = "https://"+ addr + "/api/aaaLogin.json"
 
    payload= {"aaaUser" :
              {"attributes" :
                   {"name" : "cisco",
                    "pwd" : "cisco"}
               }
          }

    response = requests.post(url,json=payload,verify=False)
    #print(response.json())
    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]

#Uses NAXPI DME model to take a mgmtIP, cookie and VLAN info. Creates and names a VLAN
def create_vlan(addr,vlan_numb,vlan_name,cookie):
    url = "https://"+addr+"/api/node/mo/sys.json"
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'APIC-Cookie='+cookie
    }
    payload ={
      "topSystem": {
        "children": [
          {
            "bdEntity": {
              "children": [
                {
                  "l2BD": {
                    "attributes": {
                      "fabEncap": vlan_numb,
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
    response = requests.request("POST",url,verify=False,headers=headers,data=json.dumps(payload))
    return response.json()

#Uses NAXPI DME model to take a mgmtIP, cookie and interface info. Creates and assigns an ip to an int.
def create_svi(addr,int_name,new_ip,cookie):
    url = "https://"+addr+"/api/node/mo/sys.json"
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'APIC-Cookie='+cookie
    }
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
                                  "id": int_name
                                },
                                "children": [
                                  {
                                    "ipv4Addr": {
                                      "attributes": {
                                        "addr": new_ip
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
                      "id": int_name
                    }
                  }
                }
              ]
            }
          }
        ]
      }
    }
    response = requests.request("POST",url,verify=False,headers=headers,data=json.dumps(payload))
    return response.json()

#Uses NAXPI DME model to take a mgmtIP, cookie and HSRP info. Configures HSRP on an interface.

def hsrp_config(addr,int_name,hsrp_group,hsrp_addr,cookie):
    url = "https://"+addr+"/api/node/mo/sys.json"
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'APIC-Cookie='+cookie
    }
    payload ={
      "topSystem": {
        "children": [
          {
            "interfaceEntity": {
              "children": [
                {
                  "sviIf": {
                    "attributes": {
                      "id": int_name
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
                            "id": int_name
                          },
                          "children": [
                            {
                              "hsrpGroup": {
                                "attributes": {
                                  "af": "ipv4",
                                  "id": hsrp_group,
                                  "ip": hsrp_addr,
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
    response = requests.request("POST",url,verify=False,headers=headers,data=json.dumps(payload))
    return response.json()

#Uses NAXPI DME model to take a mgmtIP, cookie and OSPF info. Configures OSPF on an interface.
def ospf_config(addr,int_name,ospf_id,ospf_area,cookie):
    url = "https://"+addr+"/api/node/mo/sys.json"
    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'APIC-Cookie='+cookie
    }
    payload ={
      "topSystem": {
        "children": [
          {
            "ospfEntity": {
              "children": [
                {
                  "ospfInst": {
                    "attributes": {
                      "name": ospf_id
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
                                  "id": int_name
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
                      "id": "vlan110"
                    }
                  }
                }
              ]
            }
          }
        ]
      }
    }
    response = requests.request("POST",url,verify=False,headers=headers,data=json.dumps(payload))
    return response.json()

#From the TurnipTheBeet git. swapped in variables for the mgmtIP, interface to change, and new ip.
def ChangeAddressYang(ipAddr,intf_to_change,new_ip):
    url = "https://"+ipAddr+":443/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet2"
    username = 'cisco'
    password = 'cisco'
    payload={"ietf-interfaces:interface": {
                        "name": intf_to_change,
                        "description": "Configured by RESTCONF",
                        "type": "iana-if-type:ethernetCsmacd",
                        "enabled": "true",
                                         "ietf-ip:ipv4": {
                                                                "address": [{
                                                                    "ip": new_ip,
                                                                    "netmask": "255.255.255.252"
                                                                    
                                                                            }   ]
                                                            }
                                            }
             }

    headers = {
      'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm',
      'Accept': 'application/yang-data+json',
      'Content-Type': 'application/yang-data+json'
    }

    response = requests.request("PUT", url, auth=(username,password),headers=headers, verify = False, data=json.dumps(payload))

def get_interfaces(mgmt_IP):
    #RESTCONF get ip interfaces for....something
    #url = "https://10.10.20.175:443/restconf/data/ietf-yang-library:modules-state"
    #url = "https://10.10.20.175:443/restconf/tailf/modules/ietf-interfaces/2014-05-08"
    url = "https://"+mgmt_IP+":443/restconf/data/ietf-interfaces:interfaces"#Connectes to a web interface on the device
    username = 'cisco'
    password = 'cisco'
    payload={}
    headers = {
      'Content-Type': 'application/yang-data+json',
      'Accept': 'application/yang-data+json',
      'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm'
    }

    response = requests.request("GET", url, auth = (username,password), verify = False, headers=headers, data=payload)
    #print(response.text)
    #print(str(response["ietf-interfaces:interfaces"]["interface"][0]["ietf-ip:ipv4"]["address"][0]))
    return response.json()

def interface_ip4(addr,cookie):
    #DME get interfaces from nxos devices
    url = "https://"+addr+"/api/node/mo/sys/ipv4/inst/dom-default.json?query-target=children"#
                          
    #auth_cookie={"APIC-cookie" : cookie} can be use interchangable with the "headers" varible format
    payload=None
    headers = {'Content-Type' : 'text/plain','Cookie' : 'APIC-Cookie='+cookie}
    response= requests.request("GET",url,data=json.dumps(payload),headers=headers,verify=False)#cookies=auth_cookie,
    #response = requests.request("GET", url, data=json.dumps(payload), cookies=auth_cookie,verify=False)
    return response.json()

def individual_interface_ip4(addr,cookie,interface):
    #DME get interface IP from specific int
    url = "https://"+addr+"/api/node/mo/sys/ipv4/inst/dom-default/if-["+interface+"].json?query-target=children"#
                          
    #auth_cookie={"APIC-cookie" : cookie} can be use interchangable with the "headers" varible format
    payload=None
    headers = {'Content-Type' : 'text/plain','Cookie' : 'APIC-Cookie='+cookie}
    response= requests.request("GET",url,data=json.dumps(payload),headers=headers,verify=False)#cookies=auth_cookie,
    #response = requests.request("GET", url, data=json.dumps(payload), cookies=auth_cookie,verify=False)
    true_response= response.json()

    return true_response['imdata'][0]['ipv4Addr']['attributes']['addr']

def IP_changer(ip_address):
    #changes the 2nd octet while retaining the other info
    new_oct = "31"
    ipsplit = ip_address.split(".")
    ipsplit[1]=new_oct
    new_IP=".".join(ipsplit)
    return new_IP

def break_num_out_int(vlanint):
    numbers = vlanint[4:]
    return numbers

def actually_change_interface_ip(addr,cookie,interface,New_addy):
    url = "https://"+addr+"/api/node/mo/sys/ipv4/inst/dom-default/if-["+interface+"].json?query-target=children"

    payload = {
    "ipv4Addr": {
        "attributes": {
        "addr": New_addy,
        "type": "primary"
    } }}



    headers = {
    'Content-Type': 'application/json',
    'Cookie': 'APIC-cookie=' + cookie
    }


    response = requests.request("POST", url, headers=headers, verify = False, data=json.dumps(payload))

    #print(response.text)

def set_new_hsrp_IP(vlan_interface):
    #we know all the addresses are 172.32.something.1 and something is always the valn number, maybe using naming conventions to figure this out is iffy but then why use naming conventions
    # UNTESTED 
    vlan_number = vlan_interface[4:]
    new_hsrp= "172.31."+vlan_number+".1"
    return new_hsrp






def main():
    #part 1###############################################
    device=read_file()
    #print(device)
    checkbool = ""
    while checkbool != "done":
        #while loop to keep it going until done if statements to be specific about what to do with a given input, this would be better as an argpars but whatever
        print(device)#will might turn this into a table later
        checkbool =input("what would you like to do?:\nadd delete modify done\t")
        if checkbool=="add":
            device=add_to_device(device)
        if checkbool == "delete":
            dev_del=input("what host?" )
            device=remove_device(device,dev_del)
        if checkbool == "modify":
            dev_to_mod = input("which hostname are we modifing?\t")
            key_to_mod= input("and what are we changing?\t")           
            if key_to_mod == "managementIP":
                valbool=False
                while valbool == False:
                    new_value=input("what will the new Value be?\t")
                    valbool=IPchecker(new_value)
            if key_to_mod == "type":
                valuebool=False
                while valuebool==False:
                    new_value=input("what will the new Value be?\t")
                    new_value=new_value.lower()
                    valuebool=type_enforce(new_value)
            else:
                new_value=input("what will the new Value be?\t")
            device=Mod_Device(device,dev_to_mod,key_to_mod,new_value)
    
    write_to_file(device)
    #part 2#########################3
    device_now_mod=read_file()
    #print(device_now_mod)
    for ind_dev_nxos in device_now_mod:
        if  'nxos'==ind_dev_nxos['type'] :#DME
            #print(ind_dev_nxos)
            nxosIP=(ind_dev_nxos['managementIP'])
            print(nxosIP)
            nxoscookie=getCookie(nxosIP)
            nxosints=interface_ip4(nxosIP,nxoscookie)
            
            #print(nxosints)
            for interfaces in nxosints['imdata']:
                individual_int=(interfaces['ipv4If']['attributes']['id'])
                indi_IP_per_int= individual_interface_ip4(nxosIP,nxoscookie,individual_int)
                #print(indi_IP_per_int)
                New_int_ip= IP_changer(indi_IP_per_int)
                #print(New_int_ip)
                actually_change_interface_ip(nxosIP,nxoscookie,individual_int,New_int_ip)
                #verify vlan and not something else???
                nxos_hsrp_address = set_new_hsrp_IP(individual_int)
                hsrp_config(nxosIP,individual_int,hsrp_group,nxos_hsrp_address,nxoscookie)#whats the group?
                ospf_config(nxosIP,individual_int,ospf_id,ospf_area,nxoscookie) # whats the id and area?



    for ind_dev_iosxe in device_now_mod:
        if 'iosxe' == ind_dev_iosxe['type']:#yang? netconf
            #print(ind_dev_iosxe)
            iosxeIP=(ind_dev_iosxe['managementIP'])


    

if __name__== "__main__" :
    main()
#  ______                       __             __            __                        __                                                                  
# /      \                     |  \           |  \          |  \                      |  \                                                                 
#|  $$$$$$\  _______   ______   \$$  ______  _| $$_         | $$____   __    __       | $$       ______   __    __   ______    ______   _______            
#| $$___\$$ /       \ /      \ |  \ /      \|   $$ \        | $$    \ |  \  |  \      | $$      |      \ |  \  |  \ /      \  /      \ |       \           
# \$$    \ |  $$$$$$$|  $$$$$$\| $$|  $$$$$$\\$$$$$$        | $$$$$$$\| $$  | $$      | $$       \$$$$$$\| $$  | $$|  $$$$$$\|  $$$$$$\| $$$$$$$\          
# _\$$$$$$\| $$      | $$   \$$| $$| $$  | $$ | $$ __       | $$  | $$| $$  | $$      | $$      /      $$| $$  | $$| $$   \$$| $$    $$| $$  | $$          
#|  \__| $$| $$_____ | $$      | $$| $$__/ $$ | $$|  \      | $$__/ $$| $$__/ $$      | $$_____|  $$$$$$$| $$__/ $$| $$      | $$$$$$$$| $$  | $$ __       
# \$$    $$ \$$     \| $$      | $$| $$    $$  \$$  $$      | $$    $$ \$$    $$      | $$     \\$$    $$ \$$    $$| $$       \$$     \| $$  | $$|  \      
#  \$$$$$$   \$$$$$$$ \$$       \$$| $$$$$$$    \$$$$        \$$$$$$$  _\$$$$$$$       \$$$$$$$$ \$$$$$$$  \$$$$$$  \$$        \$$$$$$$ \$$   \$$| $$      
#                                  | $$                               |  \__| $$                                                                  \$       
#                                  | $$                                \$$    $$                                                                           
#                                   \$$                                 \$$$$$$                                                                            
#    _____                      __               ______                                   __           _____                      __              _______  
#   |     \                    |  \             /      \                                 |  \         |     \                    |  \            |       \ 
#    \$$$$$  ______    _______ | $$____        |  $$$$$$\        ______   _______    ____| $$          \$$$$$  ______    _______ | $$____        | $$$$$$$\
#      | $$ /      \  /       \| $$    \       | $$__| $$       |      \ |       \  /      $$            | $$ /      \  /       \| $$    \       | $$__/ $$
# __   | $$|  $$$$$$\|  $$$$$$$| $$$$$$$\      | $$    $$        \$$$$$$\| $$$$$$$\|  $$$$$$$       __   | $$|  $$$$$$\|  $$$$$$$| $$$$$$$\      | $$    $$
#|  \  | $$| $$  | $$ \$$    \ | $$  | $$      | $$$$$$$$       /      $$| $$  | $$| $$  | $$      |  \  | $$| $$  | $$ \$$    \ | $$  | $$      | $$$$$$$ 
#| $$__| $$| $$__/ $$ _\$$$$$$\| $$  | $$      | $$  | $$      |  $$$$$$$| $$  | $$| $$__| $$      | $$__| $$| $$__/ $$ _\$$$$$$\| $$  | $$      | $$      
# \$$    $$ \$$    $$|       $$| $$  | $$      | $$  | $$       \$$    $$| $$  | $$ \$$    $$       \$$    $$ \$$    $$|       $$| $$  | $$      | $$      
#  \$$$$$$   \$$$$$$  \$$$$$$$  \$$   \$$       \$$   \$$        \$$$$$$$ \$$   \$$  \$$$$$$$        \$$$$$$   \$$$$$$  \$$$$$$$  \$$   \$$       \$$      