#!/usr/bin/env python3
#josh patch

import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #shut those warnings up, not a good idea in prod

#just show ip in br command
def show_ip_int(mgmtIP):
    switchuser='cisco'
    switchpassword='cisco'
    url='https://'+mgmtIP+'/ins'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
        {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
            "cmd": "show ip interface brief",
            "version": 1
        },
        "id": 1
        }
    ]
    response = requests.post(url,data=json.dumps(payload), verify=False ,headers=myheaders,auth=(switchuser,switchpassword)).json()
    #print(response)
    return response

#clean resonse from ip int command
def clean_json(raw_json,intlist,protolist,link_state_list,ip_add_list):
  for create_lists in raw_json['result']['body']['TABLE_intf']['ROW_intf']:
    intlist.append(create_lists['intf-name'])
    protolist.append(create_lists['proto-state'])  
    link_state_list.append(create_lists['link-state'])
    ip_add_list.append(create_lists['prefix'])

#create formated table from clean json
def create_linkstatetable(intlist,protolist,link_state_list,ip_add_list):
  print(f"\nName\t\tProto\t\tLink\t\tAddress")
  print("-"*100)
  for count in range(len(intlist)):#chat gtp for the save with range
    print(f"{intlist[count]}\t\t{protolist[count]}\t\t{link_state_list[count]}\t\t{ip_add_list[count]}")

#stacks show int br, and the json cleaning func and the table creation functions, returns a list of interface for later validation if needed
def ADDY_table_return_interfaceIP(url):
    response = show_ip_int(url)
    intlist = []
    protolist =[]
    link_state_list =[]
    ip_add_list=[]
    clean_json(response,intlist,protolist,link_state_list,ip_add_list)
    create_linkstatetable(intlist,protolist,link_state_list,ip_add_list)
    #return [intlist,ip_add_list]
    interfaceKEY_ipaddyVALUE = intKEY_IPvalue_dict(intlist,ip_add_list)
    return interfaceKEY_ipaddyVALUE

#i will want interface names directly associated with their IP addresses this function will reassociate them back together again in a new dictionary, i thought this would be easier then recleaning my command return for different information    
def intKEY_IPvalue_dict(interfaceLIST,ipLIST):
   #intIP = [interfaceLIST,ipLIST]
   #intIPdict = {intIP[0][i]:intIP[1][i] for i in range(len(interfaceLIST))}
   intIPdict = {key:value for key, value in zip(interfaceLIST,ipLIST)}
   return intIPdict

#return only items in my interface:ip dictionary who's keys start with "V"
def vlans_only(dictionary):
    vlans_dict = {}
    for key,value in dictionary.items():
       if key.startswith('V'):
          vlans_dict[key]=value
    return vlans_dict

#separates passed in dictionary values into lists and adds 5 to fourth octet
def IP_add_5(IP_to_change):
    #proof print(IP_to_change)
    IPs_broken_asLIST = IP_to_change.split(".")
    #proof print(f"4TH OCT {IPs_broken_asLIST[3]}")
    oct_to_change = IPs_broken_asLIST[3]
    #for fourth_oct in IPs_broken_asLIST[3]: leaving this for me....i was iterating over each digit which was giving me bad results when the old ip 4th oct had two digits, basically i didn't need a for loop here
        #print(f"OLD {fourth_oct}")
    fourth_oct = str(int(oct_to_change)+5)
        #print(f"NEW {fourth_oct}")
    IPs_broken_asLIST[3]=fourth_oct
    #print(IPs_broken_asLIST)
    new_IP = ".".join(IPs_broken_asLIST)
    #proof print(f"NEW IP {new_IP}")
    return new_IP

#takes in new IP values and changes the dictionary to new values while keeping that same keys
def Change_vlansIP_new_IP(Vlans,newIPlist):   
    #for replacement_value , key in enumerate(vlan_only_ipddy_dict.keys()):#use the enumerate() function to get the index of the current key CHATGPT
       #vlan_only_ipddy_dict[key] = newIPlist[replacement_value]
    new_IP_dict = intKEY_IPvalue_dict(Vlans,newIPlist)
    return new_IP_dict

#takes in dict separates IPs by split, adds 5 then updates said dict with new values    
def IP_change(vlan_only_ipddy_dict):
    ip_to_change = vlan_only_ipddy_dict.values()
    Vlans = vlan_only_ipddy_dict.keys()
    newIP_list =[]
    for item in ip_to_change:
        newIP = IP_add_5(item)
        newIP_list.append(newIP)

    #proof print(f"new list {newIP_list}")
    updated_intIP_dict =Change_vlansIP_new_IP(Vlans,newIP_list)
    return updated_intIP_dict

#changes IP on cisco device    
def command_to_change_IP_on_device(int_name,ip,Mgmt_IP):
    switchuser='cisco'
    switchpassword='cisco'
    url='https://'+Mgmt_IP+'/ins'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
    {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
        "cmd": "configure terminal",
        "version": 1
        },
        "id": 1
    },
    {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
        "cmd": "interface "+int_name,
        "version": 1
        },
        "id": 2
    },
    {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
        "cmd": "ip address "+ip +" 255.255.255.0",
        "version": 1
        },
        "id": 3
    }
    ]
    response = requests.post(url,data=json.dumps(payload), verify=False, headers=myheaders,auth=(switchuser,switchpassword)).json()
    return








def main():
    devices = {"dist-sw01" : "10.10.20.177","dist-sw02" : "10.10.20.178"}

    #Mgmt_IP = ['10.10.20.177']
    for items in devices.items():# I want both items for different reasons, mostly print clairity on what device this is happening to, otherwise i could just use other version
        Mgmt_IP= items[1]
        dev_name = items[0]
        print("for device:\n"+ (dev_name+" ")*8)
    #for Mgmt_IP in devices.values():#other version
        response = ADDY_table_return_interfaceIP(Mgmt_IP)
        #print(response)
        vlan_IP_dict=vlans_only(response)
        #proof rint(vlan_IP_dict)
        NEWvlan_IP_dict =IP_change(vlan_IP_dict)
        #proof print(NEWvlan_IP_dict)
        for interface in NEWvlan_IP_dict.items():
            int_name= (interface[0])
            IP_addy = (interface[1])
            command_to_change_IP_on_device(int_name,IP_addy,Mgmt_IP)
        print("NEW IP LIST")
        ADDY_table_return_interfaceIP(Mgmt_IP)

if __name__== "__main__" :
    main()

# _________            .___       ___.                ____.            .__      __________         __         .__     
# \_   ___ \  ____   __| _/____   \_ |__ ___.__.     |    | ____  _____|  |__   \______   \_____ _/  |_  ____ |  |__  
# /    \  \/ /  _ \ / __ |/ __ \   | __ <   |  |     |    |/  _ \/  ___/  |  \   |     ___/\__  \\   __\/ ___\|  |  \ 
# \     \___(  <_> ) /_/ \  ___/   | \_\ \___  | /\__|    (  <_> )___ \|   Y  \  |    |     / __ \|  | \  \___|   Y  \
#  \______  /\____/\____ |\___  >  |___  / ____| \________|\____/____  >___|  /  |____|    (____  /__|  \___  >___|  /
#         \/            \/    \/       \/\/                          \/     \/                  \/          \/     \/ 