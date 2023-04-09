import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #shut those warnings up, not a good idea in prod

def playaround():
    devices = [
        {
        "hostname":"R1",
        "type":"router",
        "brand":"Cisco",
        "mgmtIP":"10.0.0.1"
        },
        {
        "hostname":"S1",
        "type":"switch",
        "brand":"Cisco",
        "mgmtIP":"10.0.0.2"
        }
    ]
    print(devices)
    def create_list_subset(list_o_devices):
        new_list=[]
        for dev in list_o_devices:
            new_list.append({'hostname': dev['hostname'],'mgmtIP':dev['mgmtIP']})
        return new_list
    modi_list = create_list_subset(devices)
    print(modi_list)
    for individual in modi_list:
        print(individual)
def getIntRestMAC_base(ip):
    #Returns a list of Dictionaries, one for each interface, that contains only an interface 
    # #name and IP address
    url="https://"+ip+":443/restconf/data/interfaces-state"
    username="cisco"
    password="cisco"
    payload={}
    headers={
        'Content-Type':'application/yang-data+json',
        'Accept':'application/yang-data+json',
        'Authorization':'Basic cm9vdDpEX1ZheSFfMTAm'
    }
    response = requests.request("GET",url,auth=(username,password),verify=False,headers=headers,data=payload)
    return response.json()
def sort_for_nam_mac(info):
    #trim return getIntRestMAC_base
    namemac_dict=[]
    sort= info['ietf-interfaces:interfaces-state']['interface']
    for items in sort:
            if items['name'] != "Loopback0":
                namemac_dict.append ({(items['name']):(items['phys-address'])})
    #print(namemac_dict)
    return namemac_dict
def getInts_IP(ip):
    #for getting interfaces info logical
    url = "https://"+ip+":443/restconf/data/ietf-interfaces:interfaces"


    username = 'cisco'
    password = 'cisco'
    payload={}
    headers = {
    'Content-Type': 'application/yang-data+json',
    'Accept': 'application/yang-data+json',
    'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm'
    }

    response = requests.request("GET", url, auth = (username,password), verify = False, headers=headers, data=payload)
    return response.json()
def sort_for_nam_ip(info):
    #trim return from get getInts_IP 
    nameIP_dict = []
    sort = info['ietf-interfaces:interfaces']['interface']
    for item in sort:
        if item['name'] != "Loopback0":
        #print (f"{item['name']}")
            for addresses in item['ietf-ip:ipv4']['address']:
                nameIP_dict.append ({(item['name']):[(addresses['ip']),(addresses['netmask'])]})
    #print(nameIP_dict)
    return nameIP_dict
def combine_lists(maclist,iplist):
    #combine 2 different lists of dict base on interface names, tosses anything that dosen't have item in both lists, place mac and ip in list with interface name as key
    comb_list =[]
    for macs in maclist:
        for ips in iplist:
            if set(macs.keys()) == set(ips.keys()):
                common_int = set(macs.keys()) & set(ips.keys())
                com_dict={}
                for key in common_int:
                    com_dict[key] = [macs[key],ips[key]]
                comb_list.append(com_dict)
    #print(comb_list)
    return comb_list

def combine_lists_intolist(mac,ip):
    #accept list of dict with keys always interface and value being ip or mac depending, turn into list of lists [int,ip,sub,mac]
    result =[]
    for item in range(len(mac)):
        temp = []
        for key, value in mac[item].items():
            temp.append(key)
            temp.append(value)
            for int_name, ip_sub in ip[item].items():
                if key == int_name:
                    temp.extend(ip_sub)
        result.append(temp)
    
    
    #print (result)
    return result


def nice_table(info):
    #just make a pretty table based on return from combined_lists
    print("interface\t\t\tIP\t\t\tSub\t\t\tMAC")
    for item in info:
        print(f"{item[0]}\t\t{item[2]}\t\t{item[3]}\t\t{item[1]}")
        #print(f"{', '.join(item.keys())}\t\t{item[list(item.keys())[0]][1]}\t\t{item[list(item.keys())[0]][0]}")

def modify_interfaces_whichINT(info):
    #ask for input (iknow denny) and (I KNOW) verify  that the interface exists/in our list and isn't ge1 becasue if we mod that we'll have connectivity issues
    validbool= False 
    while validbool == False:
        intname= input ("which interface are we modifying?\nTYPE WHOLE NAME ").strip()
        for item in info:
            if item[0]== intname:
                
                if intname == "GigabitEthernet1":
                    print("IF YOU MODIFY THAT INTERFACE WE'RE GONNA HAVE A BAD TIME")
                else:
                    #print("yay")
                    validbool = True
                break#sorry denny couldn't get it to not print invalid interface w/out this
        else:
                print("Inavlaid Interface\n")
                #validbool = False
    #print(intname)
    return intname

def new_ip(ip_ask):
    check_number =ip_ask.replace(".","")
    if check_number.isnumeric(): 
        IP_check = ip_ask.split(".") #i need to check them individually
        if len(IP_check) == 4:
            A = int(IP_check[0])
            B = int(IP_check[1])
            C = int(IP_check[2])
            D = int(IP_check[3])
            if A <= 255 and B <= 255 and C <= 255 and D <= 255:
                #print(f"{ip_check} is valid")
                    valid_bool=True
                    #return valid_bool
            else:
                #print("needs to be a valid IP address")
                valid_bool = False
        else:
            #print("need to be a properly formatted IP address(3 digets, dot 3 more. 4 groups total)")                
            valid_bool = False
    else:
        valid_bool = False
    return valid_bool
def change_address(ip,interface,newip,sub):
    url = "https://"+ip+":443/restconf/data/ietf-interfaces:interfaces/interface="+interface
    username = 'cisco'
    password = 'cisco'
    payload={"ietf-interfaces:interface": {
                        "name": interface,
                        "description": "Configured by RESTCONF",
                        "type": "iana-if-type:ethernetCsmacd",
                        "enabled": "true",
                                        "ietf-ip:ipv4": {
                                                                "address": [{
                                                                    "ip": newip,
                                                                    "netmask": sub#add subnet
                                                                    
                                                                            }   ]
                                                            }
                                            }
            }

    headers = {
    'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm',
    'Accept': 'application/yang-data+json',
    'Content-Type': 'application/yang-data+json'
    }

    response = requests.request("PUT", url, auth=(username,password),headers=headers, verify = False, data=json.dumps(payload)
    )
    print(response.text)

def main():
    ipAddr = "10.10.20.175"

    int_lst_phys= getIntRestMAC_base(ipAddr)
    int_lst_logic = getInts_IP(ipAddr)
    logic=sort_for_nam_ip(int_lst_logic)
    phys=sort_for_nam_mac(int_lst_phys)
    list_o_list=combine_lists_intolist(phys,logic)
    nice_table(list_o_list)
    int_we_mod = modify_interfaces_whichINT(list_o_list)
    boolchck_ip = False
    while boolchck_ip== False:       
        NewIP= input ("what will the new IP address be?\n")
        boolchck_ip = new_ip(NewIP)
    #print(NewIP)
    boolchcksub = False
    while boolchcksub== False:       
        New_subnet= input ("what will the new subnet address be?\n")
        boolchcksub = new_ip(New_subnet)
    #print(New_subnet)
    change_address(ipAddr,int_we_mod,NewIP,New_subnet)
    afterint_lst_phys= getIntRestMAC_base(ipAddr)
    afterint_lst_logic = getInts_IP(ipAddr)
    afterlogic=sort_for_nam_ip(afterint_lst_logic)
    afterphys=sort_for_nam_mac(afterint_lst_phys)
    afterlist_o_list=combine_lists_intolist(afterphys,afterlogic)
    nice_table(afterlist_o_list)


if __name__== "__main__" :
    playaround()
    main()

# _________            .___       ___.                ____.            .__      __________         __         .__     
# \_   ___ \  ____   __| _/____   \_ |__ ___.__.     |    | ____  _____|  |__   \______   \_____ _/  |_  ____ |  |__  
# /    \  \/ /  _ \ / __ |/ __ \   | __ <   |  |     |    |/  _ \/  ___/  |  \   |     ___/\__  \\   __\/ ___\|  |  \ 
# \     \___(  <_> ) /_/ \  ___/   | \_\ \___  | /\__|    (  <_> )___ \|   Y  \  |    |     / __ \|  | \  \___|   Y  \
#  \______  /\____/\____ |\___  >  |___  / ____| \________|\____/____  >___|  /  |____|    (____  /__|  \___  >___|  /
#         \/            \/    \/       \/\/                          \/     \/                  \/          \/     \/ 
