while True:
    #start while so i keep asking for input
    name = input("enter your full name without your middle name or initial:") 
    if name.replace(" ","").isalpha(): #check for letters but not toss the space

    #get ready to split needs to be "global" although since its in the loop it reall isn't but it still needs to be before my ifs
        name = name.split()


        if len(name) != 2:
            print("really just a first and last name, not 3 names. not one name. TWO NAMES. sorry if you got one of them hyphenated guys.")
            #name = input("enter your full name without your middle name or initial:")

        else: #len(name) == 2:
            first_name = name[0]
            last_name = name[1]
            #annoyed that i can't get capitalize to work in one line
            first_name = first_name.capitalize()
            last_name = last_name.capitalize()
            print(f"Welcome to Python, {first_name}. {last_name} is a really interesting surname! Are you related to the famous Victoria {last_name}?")
            break
    else:
        print("letters only")
        continue #start over at begin while