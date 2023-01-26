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
header =""
value = ""
for key in router1.keys():
  header = header + key
  if len(key) >= 8:
    header = header + "\t"
  else:
    header = header + "\t\t"
  value = value + router1[key]
  value =value.replace(" /24","")
  if len(router1[key]) >= 8:
    value = value + "\t"
  else:
    value = value + "\t\t"
print(header)
print("-"*200)
print(value)
"""  
formated_key = []
for tableitems in router1:
    #print(tableitems)
    formated_key.append(tableitems)
    #tableitems = [tableitems]
#formated_items = str(formated_items)#replace(" ","\t")
host= formated_key.pop()
  #pull the last item because i want it 1st
formated_key.insert(0, host)
  #rejoin last item (hostname)
  #print((formated_items))
formated_items_string = '\t\t'.join(str(itemkey) for itemkey in formated_key)
  #print(formated_items_string)
formated_value=[]
  #value part of the table arg
for value in router1.values():
    #print(value)
  formated_value.append(value)
    #print(formated_value)
hostname = formated_value.pop()
formated_value.insert(0, hostname)
formated_value_string = '\t\t'.join(str(itemval) for itemval in formated_value)
formated_value_string = formated_value_string.replace(" /24","")
table=(f"{formated_items_string}\n{formated_value_string}")
print(table) #uggg close enough
"""
#question 4
while True:
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
          """
          for tableitems in router1:
            formated_key.append(tableitems)
            host= formated_key.pop()
            formated_key.insert(0, host)
            formated_items_string = '\t\t'.join(str(itemkey) for itemkey in formated_key)
            formated_value=[]
            for value in router1.values():
              formated_value.append(value)
            hostname = formated_value.pop()
            formated_value.insert(0, hostname)
            formated_value_string = '\t\t'.join(str(itemval) for itemval in formated_value)
            formated_value_string = formated_value_string.replace(" /24","")
            table=(f"{formated_items_string}\n{formated_value_string}")
          """
          header = "" 
          value=""
          for key in router1.keys():
            header = header + key
            if len(key) >= 8:
              header = header + "\t"
            else:
              header = header + "\t\t"
            value = value + router1[key]
            value =value.replace(" /24","")
            if len(router1[key]) >= 8:
              value = value + "\t"
            else:
              value = value + "\t\t"
          print(f"ok changing IP")
          print(header)
          print("-"*200)
          print(value)
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
    print(header)
    print("-"*200)
    print(value)
    break


