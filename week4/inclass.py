import requests


payload ={}
headers ={}
def main():
    asking_num_decks="how many Decks? "
    askdecks = input(asking_num_decks)
    deck_number=get_many_deck(askdecks,asking_num_decks)
    response_MAIN=shuffle_deck(deck_number)
    responseDeckID=(response_MAIN.json())
    print(responseDeckID)
    DeckID= responseDeckID['deck_id']
    print(DeckID)




def get_many_deck(askdecks,querynum):
    chk_bool = True
    while chk_bool == True:
        if int(askdecks)  <= 3:
            #print(askdecks)
            chk_bool = False
            return askdecks   
        else:
            print("needs to be less then 3")
            askdecks=input(querynum)
            #print(askdecks)
            chk_bool = True

def shuffle_deck(deckcnt): #makes new deck, shuffles, 
    url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=" + deckcnt
    global payload 
    global headers
    response = requests.request("GET", url, headers=headers, data=payload)
    return response


if __name__== "__main__" :
    main()