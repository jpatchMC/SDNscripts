import requests
import json
# josh patch
#this is alot like the assesment only you're explaining more of the inputs so I can manipulate them
def main():
    command_response = api_command()
    #print(command_response)
    table=create_table(command_response)
    print(table)
def api_command():


    """
    Modify these please
    """
    switchuser='cisco'
    switchpassword='cisco'

    url='https://10.10.20.177/ins' #dosen't gen as https, need to change to that from http
    myheaders={'content-type':'application/json-rpc'}
    payload=[
    {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
        "cmd": "show version",
        "version": 1
        },
        "id": 1
    }
    ]
    response = requests.post(url,data=json.dumps(payload), verify=False , headers=myheaders,auth=(switchuser,switchpassword)).json() #add verify=False after payload to ignore cert warnings
    return response
def create_table(info):
    #stupid interating strings printing one letter at a time
    memory =""
    mem_type =""
    Host_name=""
    for memory_info in str(info['result']['body']['memory']):
        memory = memory + (memory_info)
        #print(memory)
    for memory_type_info in info['result']['body']['mem_type']:
        mem_type= mem_type + memory_type_info
    memory = memory +" "+mem_type  
    #print (memory)
    for name in info['result']['body']['host_name']:
        Host_name=Host_name + name
    #print(Host_name)
    table_response= "HostName ="+ Host_name +"\t\t"+"Memory ="+memory
    return table_response
if __name__== "__main__" :
    main()