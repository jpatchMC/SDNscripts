import requests
import json
# josh patch
def api_command(IP):#to be fed into any command api also according to your doc it shoudl be called getOSPFNEIghbor but i thought momentarily that i would need to pass more then one command through
    switchuser='cisco'
    switchpassword='cisco'

    url='https://'+IP+'/ins' 
    myheaders={'content-type':'application/json-rpc'}
    payload=[
    {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
        "cmd": "show ip ospf neighbor",
        "version": 1
        },
        "id": 1
    }
    ]
    response = requests.post(url,data=json.dumps(payload), verify=False , headers=myheaders,auth=(switchuser,switchpassword)).json() #add verify=False after payload to ignore cert warnings
    return response

def showospf(response,where):
    print(f"Show ospf neighbors of {where}")
    print(f"Router-ID\t\tNeighbor-IP\t\tInt")
    print('-'*50)
    for trim in response['result']['body']['TABLE_ctx']['ROW_ctx']['TABLE_nbr']['ROW_nbr']:
        #print(trim)
        #print(type(trim))
        R_ID= trim['rid']
        Nei_ID =trim['addr']
        Interface=trim['intf']
        print(f"{R_ID}\t\t{Nei_ID}\t\t{Interface}")


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
    devices = {'sw1':{'hostname':'dist-sw01','deviceType':'switch','MgmtIP':'10.10.20.177'},'sw2':{'hostname':'dist-sw02','deviceType':'switch','MgmtIP':'10.10.20.178'}}
    
    sw1_response=api_command(devices['sw1']['MgmtIP'])
    sw2_response=api_command(devices['sw2']['MgmtIP'])
    silly_table(devices)
    print("="*50)
    showospf(sw1_response,devices['sw1']['hostname'])
    showospf(sw2_response,devices['sw2']['hostname'])
    #dev_Mgmt(devices)
    #showospf(denresponse,devices['sw1']['hostname'])

    


if __name__== "__main__" :
    main()