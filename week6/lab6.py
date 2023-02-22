import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #shut those warnings up, not a good idea in prod
# josh patch

def api_command(IP,cmd):#take device mangip and a command as arguments
    switchuser='cisco'
    switchpassword='cisco'
    
    url='https://'+IP+'/ins' 
    myheaders={'content-type':'application/json-rpc'}
    payload=[
    {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
        "cmd": cmd,
        "version": 1
        },
        "id": 1
    }
    ]
    response = requests.post(url,data=json.dumps(payload), verify=False , headers=myheaders,auth=(switchuser,switchpassword)).json() #add verify=False after payload to ignore cert warnings
    return response

def showospf(response,where):#makes my show tables, takes the the "show ip ospf" response json and parses and trims it, "where" is just what device hostname directly from primary dictionary
    print(f"\nShow ospf neighbors of {where}")
    print(f"Router-ID\t\tNeighbor-IP\t\tInt")
    print('-'*50)
    for trim in response['result']['body']['TABLE_ctx']['ROW_ctx']['TABLE_nbr']['ROW_nbr']:
        #print(trim)
        #print(type(trim))
        R_ID= trim['rid']
        Nei_ID =trim['addr']
        Interface=trim['intf']
        print(f"{R_ID}\t\t{Nei_ID}\t\t{Interface}")

#the table of our dictionary we're insturcted to create, i'm being facetious 
def silly_table(devices):
    print(f"Host     \t\tType     \t\tMgmtIP")
    print("-"*50)
    for stuff in devices.values():
        print(f"{stuff['hostname']}\t\t{stuff['deviceType']}\t\t{stuff['MgmtIP']}")
#def dev_Mgmt(devices):
#    for device in devices:
 #       print(device)
  #      mgmtIP= str(device['MgmtIP'])
   #     print(mgmtIP)
        #ospf_nei = api_command(mgmtIP)
        #sprint(ospf_nei)
        

def main():
    cmd = "show ip ospf neighbor"
    devices = {'sw1':{'hostname':'dist-sw01','deviceType':'switch','MgmtIP':'10.10.20.177'},'sw2':{'hostname':'dist-sw02','deviceType':'switch','MgmtIP':'10.10.20.178'}}
    silly_table(devices)
    print("="*50)
    
    for device in devices.values():
        #print(device['MgmtIP'])
        api_response = api_command(device['MgmtIP'],cmd)
        showospf(api_response,device['hostname'])
    #sw1_response=api_command(devices['sw1']['MgmtIP'])
    #sw2_response=api_command(devices['sw2']['MgmtIP'])
    
    #showospf(sw1_response,devices['sw1']['hostname'])
    #showospf(sw2_response,devices['sw2']['hostname'])
    #dev_Mgmt(devices)
    #showospf(denresponse,devices['sw1']['hostname'])

    


if __name__== "__main__" :
    main()