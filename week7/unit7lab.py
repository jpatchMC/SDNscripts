#josh patch
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #shut those warnings up, not a good idea in prod

def cmmd():
    switchuser='cisco'
    switchpassword='cisco'
    url='https://10.10.20.177/ins'
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
    response = requests.post(url,data=json.dumps(payload), verify=False,headers=myheaders,auth=(switchuser,switchpassword)).json()
    print(response)
    return response
#i'm doing three command at once for one operation, i suppose i could've made a bunch or arguments, hard coded the strings and go from there but this is a touch easier
def cmmd_three_parts(int_name,ip,sub):
    switchuser='cisco'
    switchpassword='cisco'
    url='https://10.10.20.177/ins'
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
        "cmd": "ip address "+ip +" /"+sub,
        "version": 1
        },
        "id": 3
    }
    ]
    response = requests.post(url,data=json.dumps(payload), verify=False, headers=myheaders,auth=(switchuser,switchpassword)).json()
    return

def linkstatelist(response,intlist,protolist,link_state_list,ip_add_list):
  for MEATY_result in response['result']['body']['TABLE_intf']['ROW_intf']:#
    #print (result)
    intlist.append(MEATY_result['intf-name'])
    protolist.append(MEATY_result['proto-state'])  
    link_state_list.append(MEATY_result['link-state'])
    ip_add_list.append(MEATY_result['prefix'])

def linkstatetable(intlist,protolist,link_state_list,ip_add_list):
  print(f"Name\t\tProto\t\tLink\t\tAddress")
  print("-"*100)
  for count in range(len(intlist)):#chat gtp for the save with range
    print(f"{intlist[count]}\t\t{protolist[count]}\t\t{link_state_list[count]}\t\t{ip_add_list[count]}")

#checks to see if an interface is present on device
def define_interface(intlist,interface_present):
   #chkBOOL = True    
   #while chkBOOL == True:
    #    #new_present_int= input("what interface's IP would you like to change?:\n")#I know you said for this to be in main but I'm putting it here
    #    if any(inlist_item == interface_present for inlist_item in intlist): # for tiktok again woot
    #        chkBOOL = False
    #        return chkBOOL#interface_present    
    #    else:
    #        #print("the interface should be entered as it appears in the above table\nand need to exist in said table kay thanks")
    #        chkBOOL = True
    if interface_present in intlist:
       chkBOOL =True
    else:
       chkBOOL=False
    return chkBOOL

def IPchecker(ip_ask): #ip ask is a string thats a question define in main the argument is the sting of the input line, not the actual IP
    #valid_bool = True
    #while valid_bool == True:
    #while True:
        #ip_check = input(ip_ask)
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
        #print("needs to be a valid IP address(with numbers)")
        valid_bool = False
    return valid_bool

#not used anymore
def change_IP(verified_int,NEW_IP):
   #NEW_IP = "ok what is the new ip?\n"
   checkedIP=IPchecker(NEW_IP)#new var incase 1st entered ip isn't good
   cmmd_three_parts(verified_int,checkedIP)

#stacks show int br, and the json cleaning func and the table creation functions, returns a list of interface for later validation if needed
def ADDY_table():
    response = cmmd()
    intlist = []
    protolist =[]
    link_state_list =[]
    ip_add_list=[]
    linkstatelist(response,intlist,protolist,link_state_list,ip_add_list)
    linkstatetable(intlist,protolist,link_state_list,ip_add_list)
    return intlist  

#this was not used
def Get_change_info():
    Interface_name=input("what interface?\n")
    New_IP=input("what will the new IP be?\n")
    changes= {Interface_name.capitalize(): New_IP}
    return changes

def subnet_validation(CIDR):
    validBOOL = False
    if int(CIDR) <= 32 and int(CIDR) >=1 :
        validBOOL = True
    else:
        validBOOL = False
    return validBOOL



def main():
    current_response = ADDY_table()
    print(current_response)

    Valid_interface=False
    
    while Valid_interface == False:
        Interface_name=input("what interface?\n")
        Interface_name=Interface_name.capitalize()
        Valid_interface=define_interface(current_response,Interface_name)
        #if continue1 == True:

    #print(Interface_name) 
    valid_ip = False  
    while valid_ip == False:
        int_addy_change= input("what IP?\n")
        valid_ip=IPchecker(int_addy_change)
    #print(int_addy_change, Interface_name)
    valid_sub = False
    while valid_sub == False:
        int_subnet_change = input ("what Subnet CIDR?\n")
        valid_sub= subnet_validation(int_subnet_change)
    cmmd_three_parts(Interface_name,int_addy_change,int_subnet_change)
    ADDY_table()

    #change_response = ADDY_table()

if __name__== "__main__" :
    main()