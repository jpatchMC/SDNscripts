#!/usr/bin/env python3

import json
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #shut those warnings up, not a good idea in prod
from ncclient import manager
import xmltodict
import os

def check_file_exists():
    #checks if devices.json exists in current directory, if no make empty list if yes opens file, passes to varible
    file_path = "devices.json"
    if os.path.isfile(file_path):
        device=read_file()
        print(f"The file '{file_path}' exists.")
    else:
        device = []
        print(f"The file '{file_path}' does not exist.")
    return device
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

def getCookie(mgmt_IP) :

#NX REST API Authen See REST API Reference for format of payload below

    url = "https://"+ mgmt_IP + "/api/aaaLogin.json"
 
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
def create_vlan(addr,vlan_numb,cookie):
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
                      "name": "projectTest"
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

#From the TurnipTheBeet git. swapped in variables for the mgmtIP, interface to change, and new ip. note, subnet is hard coded since for our current devices all of them are point to point networks
def ChangeAddressYang(ipAddr,new_ip,interface):
    url = "https://"+ipAddr+":443/restconf/data/ietf-interfaces:interfaces/interface="+interface
    username = 'cisco'
    password = 'cisco'
    payload={"ietf-interfaces:interface": {
                        "name": interface,
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

def generate_new_hsrp_IP(vlan_interface):
    #we know all the addresses are 172.31.something.1 and something is always the vlan number, maybe using naming conventions to figure this out is iffy but then why use naming conventions
    vlan_number=break_num_out_int(vlan_interface) 
    #vlan_number = vlan_interface[4:]
    new_hsrp= "172.31."+vlan_number+".1"
    return new_hsrp

def add_new_vlan(nxosChangeCount,cookie,mngmtIP):
  #we know all the addresses are 172.31.vlan. something depending on the switch and if its hsrp , maybe using naming conventions to figure this out is iffy but then why use naming conventions
  #anyway this adds a new vlan with IP and hsrp and ospf based on HOW MANY TIMES WE'VE INTERATED THROUGH NXOS SWITCHES
  vlan_svi_IP = "172.31.120."+str(nxosChangeCount)+"/24"
  #print(vlan_svi_IP)
  interface_ID = "vlan120"
  vlan_numb= "vlan-120"
  HSRP_IP_addy = "172.31.120.1"
  hsrp_group = "10"
  ospf_id = "1"
  ospf_area = "0.0.0.0"
  create_vlan(mngmtIP,vlan_numb,cookie)
  create_svi(mngmtIP,interface_ID,vlan_svi_IP,cookie)
  hsrp_config(mngmtIP,interface_ID,hsrp_group,HSRP_IP_addy,cookie)
  ospf_config(mngmtIP,interface_ID,ospf_id,ospf_area,cookie)

def get_int_call(router):
    #gets info about interfaces in use, their names and IP
    netconf_filter = """

    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface></interface>
    </interfaces>
    
    """

    with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:
        netconf_reply = m.get_config(source = 'running', filter = ("subtree",netconf_filter))
    netconf_data = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]
    interfaces = netconf_data["interfaces"]["interface"]
    return interfaces
#Function to take an IP address as an argument and retrieve the IP address and subnet masks of the interfaces on a device.
def get_interfaces(ip_address):
  url = f"https://{ip_address}:443/restconf/data/ietf-interfaces:interfaces"
  username = 'cisco'
  password = 'cisco'
  payload={}
  headers = {
  'Content-Type': 'application/yang-data+json',
  'Accept': 'application/yang-data+json',
  'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm'
  }

  #Function sends an HTTP GET request to RESTCONF API
  response = requests.request("GET", url, auth = (username,password), verify = False, headers=headers, data=payload)
  response_dict = json.loads(response.text) #Response from device is in JSON format (parsed here by the .loads() method)
  return response_dict

def main():
    #part 1###############################################
    device =check_file_exists()
    #device=read_file()
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
    nxosChangeCount = 2
    
    for ind_dev_nxos in device_now_mod:
        if  'nxos'==ind_dev_nxos['type'] :#DME
            #print(ind_dev_nxos)
            nxosIP=(ind_dev_nxos['managementIP'])
            #print(nxosIP)
            #print(nxosChangeCount)
            nxoscookie=getCookie(nxosIP)
            nxosints=interface_ip4(nxosIP,nxoscookie)
            for interfaces in nxosints['imdata']:
                individual_int=(interfaces['ipv4If']['attributes']['id'])
                indi_IP_per_int= individual_interface_ip4(nxosIP,nxoscookie,individual_int)
                #print(indi_IP_per_int)
                New_int_ip= IP_changer(indi_IP_per_int)
                #print(New_int_ip)
                actually_change_interface_ip(nxosIP,nxoscookie,individual_int,New_int_ip)
                #verify vlan and not something else
                if individual_int[:4] == "vlan":
                  nxos_hsrp_address = generate_new_hsrp_IP(individual_int)
                  hsrp_group= "10"
                  hsrp_config(nxosIP,individual_int,hsrp_group,nxos_hsrp_address,nxoscookie)#whats the group?
                ospf_id = "1"
                ospf_area = "0.0.0.0"
                ospf_config(nxosIP,individual_int,ospf_id,ospf_area,nxoscookie) # whats the id and area?
            #add the vlan120
            add_new_vlan(nxosChangeCount,nxoscookie,nxosIP)
            nxosChangeCount = nxosChangeCount +1
            #print(nxosChangeCount)


    for ind_dev_iosxe in device_now_mod:
        if 'iosxe' == ind_dev_iosxe['type']:#yang? netconf restconf
            #print(ind_dev_iosxe)
            iosxeIP=(ind_dev_iosxe['managementIP'])
            print(iosxeIP)
            router = {"host": iosxeIP, "port" : "830","username":"cisco","password":"cisco"}
            IOSXE_interfaces = get_int_call(router)
            #print(IOSXE_interfaces)
            #IOSXE_int_IP_list=[]
            for interface in IOSXE_interfaces:
                if interface['name'] != "Loopback0":
                  if interface['name'] !="GigabitEthernet1":
                    IOSXE_interface_name=interface['name']
                    ISOSXE_interface_ip = interface['ipv4']['address']['ip']
                    NEW_IOS_int_ip = IP_changer(ISOSXE_interface_ip)
                    #print(IOSXE_interface_name)
                    #print(NEW_IOS_int_ip)
                    ChangeAddressYang(iosxeIP,NEW_IOS_int_ip,IOSXE_interface_name)
                    #response =get_interfaces(iosxeIP)
                    #print(response)
            


                
            

    

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