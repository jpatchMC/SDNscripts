# Josh Patch, ChatGPT was consulted....alot

router1 = {
    "brand": "Cisco",
    "model": "1941",
    "mgmtIP": "10.0.0.1",
    "G0/0" : "10.0.1.1 /24",
    "G0/1" : "10.0.2.1 /24",
    "G0/2" : "10.0.3.1 /24",
    "hostname" : "r1"
}
  # question 1 part e and f
router1["G0/2"] = "10.1.3.1 /24"
router1["model"] = "2901"

  #print(router1)
  #print(router1.items())
  #print(router1.keys())
  #print(router1.values())

  #question 2
for items in router1.items():
    print(f"Key = {items[0]} \t \t Value = {items[1]}")

  #question 3

  #top part of table there has to be an easier....there is
def rtrtable(router):
   
  header =""
  value = ""
  for key in router.keys():
    header = header + key
    if len(key) >= 8:
      header = header + "\t"
    else:
      header = header + "\t\t"
    value = value + router[key]
    value =value.replace(" /24","")
    if len(router[key]) >= 8:
      value = value + "\t"
    else:
      value = value + "\t\t"
  print(header)
  print("-"*200)
  print(value)

#question 4
def main():
  global router1
  while True:
    print(rtrtable(router1))
    
    change_affirmation = input("would you like to change the managment IP? y/n: ")

    if change_affirmation == "y":
      new_ip = input("what will the new IP be?: ")
      check_number =new_ip.replace(".","")
      if check_number.isnumeric(): 
        IP_check = new_ip.split(".") #i need to check them individually
      
      #print(IP_check)
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
            router1["mgmtIP"] = new_ip
            
            
            print(rtrtable(router1))
            #uggg close enough
            break
          else:
            print("needs to be a valid IP address")
            continue
        else:
          print("need to be a properly formatted IP address(numbers)")
      else:
        print("needs to be a valid IP address")
        continue
    if change_affirmation == "n":
      print(f"NO CHANGES")
      print(rtrtable(router1))
      
      break

if __name__ =="__main__":
    main()
