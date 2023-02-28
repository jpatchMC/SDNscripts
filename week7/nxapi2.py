#josh patch
import requests
import json
import urllib3
#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #shut those warnings up, not a good idea in prod

def commands(name):
    switchuser='cisco'
    switchpassword='cisco'

    url='https://10.10.20.177/ins'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
    {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
        "cmd": "config t",
        "version": 1
        },
        "id": 1
    },
    {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
        "cmd": "hostname "+ name,
        "version": 1
        },
        "id": 2
    }
    ]
    response = requests.post(url,data=json.dumps(payload),verify=False, headers=myheaders,auth=(switchuser,switchpassword)).json()
    return
def isnamegud():
    checkif = True
    while checkif == True:
        host_name= input("change host name to what?:\n")
        if host_name.isalnum() and host_name[0].isalpha():#isalnum from w3schools
                        
            checkif = False

        else:
            print("ERROR: needs to alphanumeric")
            checkif = True
    return host_name
#just adds 2 to the 3rd oct after being validated in another func
def IP_add(IP_as_list):
    IP_as_list[2]= str(int(IP_as_list[2]) + 2)
    new_IP = '.'.join(IP_as_list)
    return new_IP
    

#checks for valid IP but since the 3rd oct is being added 2 to, i can't be 255, has to be 253 or it won't be valid later
def IP_check():#notice: at the the return of this is still a list
    valid_bool = True
    while valid_bool == True:
        #while True:
        ip_check = input("enter an IP address to be changed:\n")
        check_number =ip_check.replace(".","")
        if check_number.isnumeric(): 
            IP_check_splitlist = ip_check.split(".") #i need to check them individually
            if len(IP_check_splitlist) == 4:
                A = int(IP_check_splitlist[0])
                B = int(IP_check_splitlist[1])
                C = int(IP_check_splitlist[2])
                D = int(IP_check_splitlist[3])
                if A <= 255 and B <= 255 and C <= 253 and D <= 254:
                    print(f"{ip_check} is valid")
                    return IP_check_splitlist
                else:
                    print("ERROR: needs to be a valid IP address")
                    valid_bool = True


def main():
    name_change = isnamegud()
    commands(name_change)
    IP_change = IP_check() 
    newIP = IP_add(IP_change)
    print(f"new IP adress is {newIP}")




if __name__== "__main__" :
    main()