import json


def add_to_device(device):
    #this will add / append to device inventory
    name= input("what is the name of the device?\t")
    dev_type= input("what kind of device is this?\t")
    mang_IP=input("what is the management IP address?\t")
    device.append({"hostname":name,"type":dev_type,"managementIP":mang_IP})
    return device
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

def main():
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
            key_to_mod= input("and what are we changing?")
            new_value=input("what will the new Value be?")
            device=Mod_Device(device,dev_to_mod,key_to_mod,new_value)
    
    write_to_file(device)



    

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