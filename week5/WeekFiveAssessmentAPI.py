#josh patch chat gpt for the range contribution to make moving though the list not dependant on me knowing how long the list is
import requests
import json

"""
Be sure to run feature nxapi first on Nexus Switch

"""
#i left your code as my main i suppose i should change that ill ask


def main():

  response = DennyBase()
  #made empty list to pass value into also to pass in and out of func below
  intlist = []
  protolist =[]
  link_state_list =[]
  ip_add_list=[]
  linkstatelist(response,intlist,protolist,link_state_list,ip_add_list)
  linkstatetable(intlist,protolist,link_state_list,ip_add_list)
def DennyBase():
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

  '''

  verify=False below is to accept untrusted certificate

  '''
  response = requests.post(url,data=json.dumps(payload), verify=False,headers=myheaders,auth=(switchuser,switchpassword)).json()
  return response
#i create 4 lists far within the json output
def linkstatelist(response,intlist,protolist,link_state_list,ip_add_list):
  for MEATY_result in response['result']['body']['TABLE_intf']['ROW_intf']:#
    #print (result)
    intlist.append(MEATY_result['intf-name'])
    protolist.append(MEATY_result['proto-state'])  
    link_state_list.append(MEATY_result['link-state'])
    ip_add_list.append(MEATY_result['prefix'])

#i print lists one slice at a time per list to make a formatted table
def linkstatetable(intlist,protolist,link_state_list,ip_add_list):
  print(f"Name\t\tProto\t\tLink\t\tAddress")
  print("-"*100)
  for count in range(len(intlist)):#chat gtp for the save with range
    print(f"{intlist[count]}\t\t{protolist[count]}\t\t{link_state_list[count]}\t\t{ip_add_list[count]}")
  print(f"\nName\t\tProto\t\tLink\t\tAddress")
  print("-"*75)
  for interface, protocol, state, ip in zip(intlist,protolist,link_state_list,ip_add_list):# lol this is from tiktok
    print(interface, protocol, state, ip, sep="\t\t")
  #print(f"{intlist[count]}\t\t{protolist[count]}\t\t{link_state_list[count]}\t\t{ip_add_list[count]}")
  #print(f"{intlist[1]}\t\t{protolist[1]}\t\t{link_state_list[1]}\t\t{ip_add_list[1]}")
  #print(f"{intlist[2]}\t\t{protolist[2]}\t\t{link_state_list[2]}\t\t{ip_add_list[2]}")
  #print(f"{intlist[3]}\t\t{protolist[3]}\t\t{link_state_list[3]}\t\t{ip_add_list[3]}")
  #print(f"{intlist[4]}\t\t{protolist[4]}\t\t{link_state_list[4]}\t\t{ip_add_list[4]}")
  #print(f"{intlist[5]}\t\t{protolist[5]}\t\t{link_state_list[5]}\t\t{ip_add_list[5]}")  
  #print(f"{intlist[6]}\t\t{protolist[6]}\t\t{link_state_list[6]}\t\t{ip_add_list[6]}")
  #i left the other brittle stuff so you know what i mean for the range save 
if __name__== "__main__" :
    main()