#!/usr/bin/env python3

import json


def add_to_device(device):
    #this will add / append to device inventory
    name= input("what is the name of the device?\t")
    valbool = False
    while valbool==False:
        dev_type= input("what kind of device is this? nxos or iosxe\t")
        valbool=type_enforce(dev_type)    
    valboo=False
    while valboo == False:
        mang_IP=input("what is the management IP address?\t")
        valboo=IPchecker(mang_IP)
    device.append({"hostname":name,"type":dev_type,"managementIP":mang_IP})
    return device
def type_enforce(type):
    print (type)
    if type == "nxos" or type == "iosxe":
        valbool=True
    else:
        valbool=False
    return valbool
def remove_device(device,dev_del):
    #deletes device based on hostname
    for item in device:
        if item["hostname"] == dev_del:
            device.remove(item)
    return device
def Mod_Device(device,dev_to_mod,key_to_mod,new_value):
    #modify a device based on hostname and supplied key
    for item in device:
        if item["hostname"] == dev_to_mod:
            item[key_to_mod]=new_value
    return device
def write_to_file(device):
    #writes(save) to a .json file
    file = open("devices.json","w")
    file.write(json.dumps(device))
    file.close()
def read_file():
    #opens and reads .json file
    with open("devices.json","r")as file:
        device = json.load(file)
    return device

def IPchecker(ip_ask): #ip ask is a string thats a question define in main
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
        #print("needs to be a valid IP address(with numbers)")
        valid_bool = False
    return valid_bool
def main():
    #part 1###############################################
    device=read_file()
    #print(device)
    checkbool = ""
    while checkbool != "done":
        #while loop to keep it going until done if statements to be specific about what to do with a given input, this would be better as an argpars but whatever
        print(device)#will might turn this into a table later
        checkbool =input("what would you like to do?:\nadd delete modify done\t")
        if checkbool=="add":
            device=add_to_device(device)
        if checkbool == "delete":
            dev_del=input("what host?" )
            device=remove_device(device,dev_del)
        if checkbool == "modify":
            dev_to_mod = input("which hostname are we modifing?\t")
            key_to_mod= input("and what are we changing?\t")           
            if key_to_mod == "managementIP":
                valbool=False
                while valbool == False:
                    new_value=input("what will the new Value be?\t")
                    valbool=IPchecker(new_value)
            if key_to_mod == "type":
                valuebool=False
                while valuebool==False:
                    new_value=input("what will the new Value be?\t")
                    valuebool=type_enforce(new_value)
            else:
                new_value=input("what will the new Value be?\t")
            device=Mod_Device(device,dev_to_mod,key_to_mod,new_value)
    
    write_to_file(device)
    #part 2#########################3
    device_now_mod=read_file()



    

if __name__== "__main__" :
    main()
#  ______                       __             __            __                        __                                                                  
# /      \                     |  \           |  \          |  \                      |  \                                                                 
#|  $$$$$$\  _______   ______   \$$  ______  _| $$_         | $$____   __    __       | $$       ______   __    __   ______    ______   _______            
#| $$___\$$ /       \ /      \ |  \ /      \|   $$ \        | $$    \ |  \  |  \      | $$      |      \ |  \  |  \ /      \  /      \ |       \           
# \$$    \ |  $$$$$$$|  $$$$$$\| $$|  $$$$$$\\$$$$$$        | $$$$$$$\| $$  | $$      | $$       \$$$$$$\| $$  | $$|  $$$$$$\|  $$$$$$\| $$$$$$$\          
# _\$$$$$$\| $$      | $$   \$$| $$| $$  | $$ | $$ __       | $$  | $$| $$  | $$      | $$      /      $$| $$  | $$| $$   \$$| $$    $$| $$  | $$          
#|  \__| $$| $$_____ | $$      | $$| $$__/ $$ | $$|  \      | $$__/ $$| $$__/ $$      | $$_____|  $$$$$$$| $$__/ $$| $$      | $$$$$$$$| $$  | $$ __       
# \$$    $$ \$$     \| $$      | $$| $$    $$  \$$  $$      | $$    $$ \$$    $$      | $$     \\$$    $$ \$$    $$| $$       \$$     \| $$  | $$|  \      
#  \$$$$$$   \$$$$$$$ \$$       \$$| $$$$$$$    \$$$$        \$$$$$$$  _\$$$$$$$       \$$$$$$$$ \$$$$$$$  \$$$$$$  \$$        \$$$$$$$ \$$   \$$| $$      
#                                  | $$                               |  \__| $$                                                                  \$       
#                                  | $$                                \$$    $$                                                                           
#                                   \$$                                 \$$$$$$                                                                            
#    _____                      __               ______                                   __           _____                      __              _______  
#   |     \                    |  \             /      \                                 |  \         |     \                    |  \            |       \ 
#    \$$$$$  ______    _______ | $$____        |  $$$$$$\        ______   _______    ____| $$          \$$$$$  ______    _______ | $$____        | $$$$$$$\
#      | $$ /      \  /       \| $$    \       | $$__| $$       |      \ |       \  /      $$            | $$ /      \  /       \| $$    \       | $$__/ $$
# __   | $$|  $$$$$$\|  $$$$$$$| $$$$$$$\      | $$    $$        \$$$$$$\| $$$$$$$\|  $$$$$$$       __   | $$|  $$$$$$\|  $$$$$$$| $$$$$$$\      | $$    $$
#|  \  | $$| $$  | $$ \$$    \ | $$  | $$      | $$$$$$$$       /      $$| $$  | $$| $$  | $$      |  \  | $$| $$  | $$ \$$    \ | $$  | $$      | $$$$$$$ 
#| $$__| $$| $$__/ $$ _\$$$$$$\| $$  | $$      | $$  | $$      |  $$$$$$$| $$  | $$| $$__| $$      | $$__| $$| $$__/ $$ _\$$$$$$\| $$  | $$      | $$      
# \$$    $$ \$$    $$|       $$| $$  | $$      | $$  | $$       \$$    $$| $$  | $$ \$$    $$       \$$    $$ \$$    $$|       $$| $$  | $$      | $$      
#  \$$$$$$   \$$$$$$  \$$$$$$$  \$$   \$$       \$$   \$$        \$$$$$$$ \$$   \$$  \$$$$$$$        \$$$$$$   \$$$$$$  \$$$$$$$  \$$   \$$       \$$      