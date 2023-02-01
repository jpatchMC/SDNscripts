name = input("enter your first name:") 
age = input(f"hello {name} pleased to meet cha, how old are you? :")
addto_age = int(age) + 5
#DENNY why are you asking me to convert back to string for next statement?
print(f"in five years you'll be {addto_age}!")
if addto_age >= 38:
    print("your back must hurt, maybe lay on the floor or something")