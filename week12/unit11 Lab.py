import xml.etree.ElementTree as ET
import xmltodict
import xml.dom.minidom
from lxml import etree
from ncclient import manager
from collections import OrderedDict

router = {"host": "10.10.20.175", "port" : "830",
          "username":"cisco","password":"cisco"}

def denny():
    netconf_filter = """

    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface></interface>
    </interfaces>
    
    """

    with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:

        netconf_reply = m.get_config(source = 'running', filter = ("subtree",netconf_filter))

    #print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

    #print("#" * 40)

    #Parse returned XML to Dictionary

    netconf_data = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]

    #print(netconf_data)

    #print("d" *40)

    #Create List of Interfaces

    interfaces = netconf_data["interfaces"]["interface"]
    return interfaces

#print(interfaces)

#print("I" * 40)
def show_ip_int_yang(interfaces):
    #take in dict and makes a table
    print("Name\t\t\tip\t\t\tsubnet")
    for interface in interfaces:
        #print(interface)
        if interface['name'] != 'Loopback0':
        #print(type(interface))
        #print("Name\tip\tsubnet\t")
            ip = interface['ipv4']['address']['ip']
            sub = interface['ipv4']['address']['netmask']
        
            print(interface['name']+"\t"+ip+ "\t"+sub)
def new_ip(ip_ask):
    #checks to make sure input is formated correctly for an ip address
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

def modify_interfaces_whichINT(validbool,interfaces,intnamechange):
    # takes interface dict and input from main checks to make sure they arn't ints we don't want to mod and then also check to make sure its a valid interface in kind of a goofy order 
    if intnamechange == "GigabitEthernet1" or intnamechange == "Loopback0":
        print("IF YOU MODIFY THAT INTERFACE WE'RE GONNA HAVE A BAD TIME")
        validbool = False
    else:
        for interface in interfaces:
            if interface['name'] == intnamechange:
                #print("yay")
                validbool = True            
            
    return validbool

def ins_new_info(interfaces,intname_change,ip_change,sub_change):
    #changes information in original dict with new values based on what int we've already defined to change and out new ip and subnet
    for interface in interfaces:
        if interface['name'] == intname_change:
            interface['ipv4']['address']['ip']=ip_change
            interface['ipv4']['address']['netmask']=sub_change
    return interfaces


def main():
    interfaces = denny()
    print(interfaces)
    show_ip_int_yang(interfaces)
    valBool_intchange= False
    while valBool_intchange == False:
        intname_change = input("what interface would you like to change?\n")#"GigabitEthernet2"
        valBool_intchange = modify_interfaces_whichINT(valBool_intchange,interfaces,intname_change)
    valBool_IP = False
    while valBool_IP == False:
        ip_change= input("new ip?\n")
        valBool_IP = new_ip(ip_change)
    valbool_sub=False
    while valbool_sub == False:
        sub_change = input("and the new subnet")
        valbool_sub = new_ip(sub_change)
    #print(intname_change,ip_change,sub_change)
    interfaces = ins_new_info(interfaces,intname_change,ip_change,sub_change)
    show_ip_int_yang(interfaces)




if __name__== "__main__" :
    main()
# _________            .___       ___.                ____.            .__      __________         __         .__     
# \_   ___ \  ____   __| _/____   \_ |__ ___.__.     |    | ____  _____|  |__   \______   \_____ _/  |_  ____ |  |__  
# /    \  \/ /  _ \ / __ |/ __ \   | __ <   |  |     |    |/  _ \/  ___/  |  \   |     ___/\__  \\   __\/ ___\|  |  \ 
# \     \___(  <_> ) /_/ \  ___/   | \_\ \___  | /\__|    (  <_> )___ \|   Y  \  |    |     / __ \|  | \  \___|   Y  \
#  \______  /\____/\____ |\___  >  |___  / ____| \________|\____/____  >___|  /  |____|    (____  /__|  \___  >___|  /
#         \/            \/    \/       \/\/                          \/     \/                  \/          \/     \/ 
