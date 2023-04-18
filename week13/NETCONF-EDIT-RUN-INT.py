import xmltodict #this is from chat gtp i wanted well error handling but I have success handleing 

from ncclient import manager


router = {"host": "10.10.20.175", "port" : "830",
          "username":"cisco","password":"cisco"}

### xmlns:xc added for ios xe 17.x and greater

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
#print(xmlInt)




def edit_config(router,xmlInt):
    with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:

        netconf_reply = m.edit_config(target = 'running', config = xmlInt)
        #print(netconf_reply)
        return (netconf_reply)

def edit_xml_for_edit(xmlInt,new_ip,interface_name,interface_number,new_subnet):
    xmlInt = xmlInt.replace("%addr%", new_ip)
    xmlInt = xmlInt.replace("%intName%", interface_name)
    xmlInt = xmlInt.replace("%intNum%", interface_number)
    xmlInt = xmlInt.replace("%mask%", new_subnet)
    #print(xmlInt)
    return xmlInt

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

def main():
    global xmlInt
    global router
    #denny did not ask for interfacename validity checks
    #interface_name = input("what kind of interface are we going to edit? just the name\nlike 'FastEthernet' or 'GigabitEthernet':\t")
    #interface_number= input("and it's number?\t")
    what_interface= input("which interface?")
    #below split back end of numbers off, was concerned for interfaces higher then 9
    interface_number=what_interface[-2:] if what_interface[-2:].isdigit() else what_interface[-1:]
    interface_name=what_interface[:-len(interface_number)]
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
    print(netconf_reply)
    #Dict_respnse =xmltodict.parse(netconf_reply)
    #if Dict_respnse['rpc-reply']['ok']==True:#true because if it isn't there at all thats bad
        #print(" success ")
if __name__== "__main__" :
    main()
# _________            .___       ___.                ____.            .__      __________         __         .__     
# \_   ___ \  ____   __| _/____   \_ |__ ___.__.     |    | ____  _____|  |__   \______   \_____ _/  |_  ____ |  |__  
# /    \  \/ /  _ \ / __ |/ __ \   | __ <   |  |     |    |/  _ \/  ___/  |  \   |     ___/\__  \\   __\/ ___\|  |  \ 
# \     \___(  <_> ) /_/ \  ___/   | \_\ \___  | /\__|    (  <_> )___ \|   Y  \  |    |     / __ \|  | \  \___|   Y  \
#  \______  /\____/\____ |\___  >  |___  / ____| \________|\____/____  >___|  /  |____|    (____  /__|  \___  >___|  /
#         \/            \/    \/       \/\/                          \/     \/                  \/          \/     \/ 
