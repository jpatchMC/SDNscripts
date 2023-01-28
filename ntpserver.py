#josh patch
def main():
    ntpserver = {"Server1" : "221.100.250.75",
    "Server2" : "201.0.113.22",
    "Server3" : "58.23.191.6"
    }
    IPs = []
    report(ntpserver,IPs)
        
        
    #print (IPs)
    PingPrep(IPs)
def report(wut,IPs):

     #could be a problem later
    print(f"Server \t\t Address")
    print("-"*50)
    for item in wut.items():
        print(f"{item[0]} \t {item[1]}")
        IPs.append(item[1])
        #return IPs

def PingPrep(ipList):
    for addy in ipList:
        print(f"Ping {addy}")

if __name__ =="__main__":
    main()
