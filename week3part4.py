#josh patch
devices = {"R1": {"type" : "router","hostname" : "R1","mgmtIP" : "10.0.0.1"},"R2":{"type" : "router","hostname" : "R2","mgmtIP" : "10.0.0.2"},"S1":{"type" : "switch","hostname" : "S1","mgmtIP" : "10.0.0.3"},"S2":{"type" : "switch","hostname" : "S2","mgmtIP" : "10.0.0.4"}}

#print(devices)
def ping(wut):#ping table
    for items in wut.values():
        #print (items)
        print(f"ping {items['mgmtIP']}")
        #for address in items['mgmtIP']:
        #print(items['mgmtIP']) 
def main():
    global devices
    ping(devices)
    #while True:
    change_affirm =input("want to add a new device? y/n: ")
    change_affirm = change_affirm.lower()
    if change_affirm == "n":
        print("alright no changes made")
    elif change_affirm == "y":
        hostname = input_check("what will the hostname be?: ")
        dev_Type = input_check("what kind of device?: ")
            
        #while True:
        #IP = input_check("what will its management IP be?: ")
        #IPchecker(IP)
        IP = IPchecker("what will the management IP be?: ")
        devices[hostname] = {"type": dev_Type, "hostname": hostname, "mgmtIP": IP}
        print("checking known Management IPs")
        ping(devices)
    else:
        print("incorrect input, exiting")

def input_check(ask):#this is to enforce that questions are answered, dosen't check for null values in actual Dict
    while True:
        input_cont = input(ask)
        if input_cont == "":
            print("I Need something here.")
        else:
            return input_cont

def IPchecker(new):
    while True:
        new = input("what will the management IP be?: ")
        check_number =new.replace(".","")
        if check_number.isnumeric(): 
            IP_check = new.split(".") #i need to check them individually
            if len(IP_check) == 4:
                A = IP_check[0]
                B = IP_check[1]
                C = IP_check[2]
                D = IP_check[3]
                A = int(A)
                B = int(B)
                C = int(C)
                D = int(D)
                if A <= 255 and B <= 255 and C <= 255 and D <= 254:
                    print(f"{new} is valid")
                    #break
                    return new
                else:
                    print("needs to be a valid IP address")
                    continue
                    #new = input("what will its management IP be?: ")
                    #return new #something is up with my elses not "pinging" correct input, using old even if wrong
            else:
                print("need to be a properly formatted IP address(3 digets, dot 3 more. 4 groups total)")
                #new = input("what will its management IP be?: ")
                #return new
                continue
        else:
            print("needs to be a valid IP address(with numbers)")
            #new = input("what will its management IP be?: ")
            #return new
            continue
    #return new
if __name__ =="__main__":
    main()
