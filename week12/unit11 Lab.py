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

def modify_interfaces_whichINT(interface,intnamechange):
    for item in interface:
            if item == intnamechange:
                
                if intnamechange != "GigabitEthernet1":
                    #print("IF YOU MODIFY THAT INTERFACE WE'RE GONNA HAVE A BAD TIME")
                    validbool = True
                else:
                    #print("yay")
                    validbool = False
                #break#sorry denny couldn't get it to not print invalid interface w/out this
    #else:
                #print("Inavlaid Interface\n")
                #validbool = False
    #print(intname)
    return validbool

def main():
    interfaces = denny()
    show_ip_int_yang(interfaces)
    valBool_intchange= False
    while valBool_intchange == False:
       intname_change = input("what interface would you like to change?\n")
       for interface in interfaces:
        if interface['name'] != 'Loopback0':
            current_int = interface['name']
            valBool_intchange = modify_interfaces_whichINT(current_int,intname_change)
    valBool_IP = False
    while valBool_IP == False:
        ip_change= input("new ip?\n")
        valBool_IP = new_ip(ip_change)
    valbool_sub=False
    while valbool_sub == False:
        sub_change = input("and the new subnet")
        valbool_sub = new_ip(sub_change)
    print(intname_change,ip_change,sub_change)

if __name__== "__main__" :
    main()