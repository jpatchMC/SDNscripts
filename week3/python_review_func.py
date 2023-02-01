#josh Patch. chatgpt was asked how to fix my while loop to stop printing errors over and over
def namecheck(name):
    #while True:
        if name.replace(" ","").isalpha():
            name = name.title()
            namelst = name.split()
            if len(namelst) != 2:
                    print("really just a first and last name, not 3 names. not one name. TWO NAMES. sorry if you got one of them hyphenated guys.")
                    return False
            else: #len(name) == 2:
                    first_name = namelst[0]
                    last_name = namelst[1]
                    #annoyed that i can't get capitalize to work in one line
                    print(f"Welcome to Python, {first_name}. {last_name} is a really interesting surname! Are you related to the famous Victoria {last_name}?")
                    return True
        else:
            print("letters only")
            return False
            #continue #start over at begin while



def main():
    while True:
        #start while so i keep asking for input
        name = input("enter your full name without your middle name or initial:") 
        if namecheck(name):
            break

if __name__ =="__main__":
    main()
