#josh patch
import requests
import json
import urllib3
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #shut those warnings up, not a good idea in prod

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
    return response
#i'm doing three command at once for one operation, i suppose i could've made a bunch or arguments, hard coded the strings and go from there but this is a touch easier
def cmmd_three_parts(int_name,ip):
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
        "cmd": "ip address "+ip +" 255.255.255.0",
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
def define_interface(intlist):
   chkBOOL = True    
   while chkBOOL == True:
        new_ip_present_int= input("what interface's IP would you like to change?:\n")#I know you said for this to be in main but I'm putting it here
        if any(inlist_item == new_ip_present_int for inlist_item in intlist):
            return new_ip_present_int    
        else:
            print("the interface should be entered as it appears in the above table\nand need to exist in said table kay thanks")
            chkBOOL = True

def IPchecker(ip_ask): #ip ask is a string thats a question define in main the argument is the sting of the input line, not the actual IP
    valid_bool = True
    while valid_bool == True:
    #while True:
        ip_check = input(ip_ask)
        check_number =ip_check.replace(".","")
        if check_number.isnumeric(): 
            IP_check = ip_check.split(".") #i need to check them individually
            if len(IP_check) == 4:
                A = int(IP_check[0])
                B = int(IP_check[1])
                C = int(IP_check[2])
                D = int(IP_check[3])
                if A <= 255 and B <= 255 and C <= 255 and D <= 254:
                    print(f"{ip_check} is valid")
                    return ip_check
                else:
                    print("needs to be a valid IP address")
                    valid_bool = True
            else:
                print("need to be a properly formatted IP address(3 digets, dot 3 more. 4 groups total)")                
                valid_bool = True
        else:
            print("needs to be a valid IP address(with numbers)")
            valid_bool = True

def change_IP(verified_int):
   NEW_IP = "ok what is the new ip?\n"
   checkedIP=IPchecker(NEW_IP)#new var incase 1st entered ip isn't good
   cmmd_three_parts(verified_int,checkedIP)







def main():
    response = cmmd()
    #made empty list to pass value into also to pass in and out of func below
    intlist = []
    protolist =[]
    link_state_list =[]
    ip_add_list=[]
    linkstatelist(response,intlist,protolist,link_state_list,ip_add_list)
    linkstatetable(intlist,protolist,link_state_list,ip_add_list)
    #print(intlist)
    

    int_return=define_interface(intlist)
    change_IP(int_return)

    response2 = cmmd()
    intlist = []
    protolist =[]
    link_state_list =[]
    ip_add_list=[]
    linkstatelist(response2,intlist,protolist,link_state_list,ip_add_list)
    linkstatetable(intlist,protolist,link_state_list,ip_add_list)

if __name__== "__main__" :
    main()