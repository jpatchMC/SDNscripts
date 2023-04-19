
import xmltodict #this is from chat gtp i wanted well error handling but I have success handleing 
from ncclient import manager
#import xml.etree.ElementTree as ET
import xml.dom.minidom
from lxml import etree
from collections import OrderedDict


router2={"host": "10.10.20.176", "port" : "830","username":"cisco","password":"cisco"}


###EDIT INTERFACES GROUP
def edit_xml_for_edit(xmlInt,new_ip,interface_name,interface_number,new_subnet):
    #adds values into xml scaffoling code
    xmlInt = xmlInt.replace("%addr%", new_ip)
    xmlInt = xmlInt.replace("%intName%", interface_name)
    xmlInt = xmlInt.replace("%intNum%", interface_number)
    xmlInt = xmlInt.replace("%mask%", new_subnet)
    #print(xmlInt)
    return xmlInt
def edit_config(router,xmlInt):
    #edit the config of a router api call
    with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:

        netconf_reply = m.edit_config(target = 'running', config = xmlInt)
        #print(netconf_reply)
        return (netconf_reply)
    

def get_int_call(router):
    netconf_filter = """

    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface></interface>
    </interfaces>
    
    """

    with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:
        netconf_reply = m.get_config(source = 'running', filter = ("subtree",netconf_filter))
    netconf_data = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]
    interfaces = netconf_data["interfaces"]["interface"]
    return interfaces

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
def isolate_int_name(what_interface,interface_number):
    interface_name=what_interface[:-len(interface_number)]
    return interface_name
def isolate_int_number(what_interface):
    interface_number=what_interface[-2:] if what_interface[-2:].isdigit() else what_interface[-1:]
    return interface_number

##show group
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



def ins_new_info(interfaces,intname_change,ip_change,sub_change):
    #copied but not needed
    #changes information in original dict with new values based on what int we've already defined to change and out new ip and subnet
    for interface in interfaces:
        if interface['name'] == intname_change:
            interface['ipv4']['address']['ip']=ip_change
            interface['ipv4']['address']['netmask']=sub_change
    return interfaces

def verify_valid_ip(ip_ask):
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

def main(routers,xmlInt):
    which_device = input("which router? R1 or R2?\n")
    router = routers[which_device]
    interfaces = get_int_call(router)
    #print(interfaces)
    show_ip_int_yang(interfaces)
    #interfaces2 = get_int_call(router2)
    #show_ip_int_yang(interfaces2)
    valBool_intchange= False
    while valBool_intchange == False:
        what_interface = input("what interface would you like to change?\n")#"GigabitEthernet2"
        valBool_intchange = modify_interfaces_whichINT(valBool_intchange,interfaces,what_interface)
    interface_number=isolate_int_number(what_interface)
    interface_name=isolate_int_name(what_interface,interface_number)
    Ip_bool= False
    while Ip_bool == False:
        new_ip = input("what will the NEW IP address be?\n")
        Ip_bool= verify_valid_ip(new_ip)
    sub_bool=False
    while sub_bool ==False:
       new_subnet = input("what will the new subnetmask be?\n")
       sub_bool =verify_valid_ip(new_subnet) 
    xmlInt=edit_xml_for_edit(xmlInt,new_ip,interface_name,interface_number,new_subnet)
    netconf_reply=edit_config(router,xmlInt)
    interfaces = get_int_call(router)
    #print(interfaces)
    show_ip_int_yang(interfaces)



if __name__== "__main__" :
    router = {"R1":{"host": "10.10.20.175", "port" : "830","username":"cisco","password":"cisco"},
              "R2":{"host": "10.10.20.176", "port" : "830","username":"cisco","password":"cisco"}}
    

    xmlInt = """<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns = "urn:ietf:params:xml:ns:netconf:base:1.0">  
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <interface>
                                <%intName%>
                    <name>%intNum%</name>
                    
                    <ip>                                    
                                        <address>
                                            <primary>
                                                <address>%addr%</address>
                                                <mask>%mask%</mask>
                                            </primary>
                                        </address>                                   
                    </ip>				
                    </GigabitEthernet>
                </interface>
                
                    </native>
            </config>"""
    main(router,xmlInt)
# _________            .___       ___.                ____.            .__      __________         __         .__     
# \_   ___ \  ____   __| _/____   \_ |__ ___.__.     |    | ____  _____|  |__   \______   \_____ _/  |_  ____ |  |__  
# /    \  \/ /  _ \ / __ |/ __ \   | __ <   |  |     |    |/  _ \/  ___/  |  \   |     ___/\__  \\   __\/ ___\|  |  \ 
# \     \___(  <_> ) /_/ \  ___/   | \_\ \___  | /\__|    (  <_> )___ \|   Y  \  |    |     / __ \|  | \  \___|   Y  \
#  \______  /\____/\____ |\___  >  |___  / ____| \________|\____/____  >___|  /  |____|    (____  /__|  \___  >___|  /
#         \/            \/    \/       \/\/                          \/     \/                  \/          \/     \/ 
