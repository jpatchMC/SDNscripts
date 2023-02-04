#!/usr/bin/env python3
#written by Josh Patch....i'm sure there are some issues with this but i didn't consult chatgtp or anything else so pretty proud of this
import requests

#url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"
payload ={}
headers ={}
def main():
    #url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"
    

    responsem = deal()

    deck = responsem.json()
    print("ok so the game is cpu draws card and you draw cards\nyou can choose the number of cards drawn (between 1 and 5)\nthen the cards are totaled up and whoever\nhas the most wins\noh almost forgot face cards are worth 10 points.")
    print(f"Deck ID is {deck['deck_id']}\n")
    if deck['shuffled'] == True:
        print("deck is shuffled\n")
    deck_ID=deck['deck_id']
    cardsREQ= "how many card would you like us both to draw for our war?\n0-5 (0 means quit btw): "
    draw_cnt = input(cardsREQ)
    enforceCARD(draw_cnt,cardsREQ)




    responsecpu = drawing_of_cards(deck_ID,draw_cnt)
    drewcpu = responsecpu.json()
    #draw and add up cpu cards
    cpupoints=0
    print("the computer draws:")
    for cardcpu in drewcpu['cards']:
        print(f"{cardcpu['value']} of {cardcpu['suit']}")
        card_NUM_conv(cardcpu)
        cpupoints = cpupoints + int(cardcpu['value'])
    print(f"and got {cpupoints} points\n")
    #draw and add up usr cards
    print("you draw:")
    usrresponse = drawing_of_cards(deck_ID,draw_cnt)
    drewusr =usrresponse.json()
    usrpoints=0
    for cardusr in drewusr['cards']:
        print(f"{cardusr['value']} of {cardusr['suit']}")
        card_NUM_conv(cardusr)
        usrpoints = usrpoints + int(cardusr['value'])
    print(f"and got {usrpoints} points\n")

    who_won(cpupoints,usrpoints)


def who_won(CPU,USER): #run compare logic against cpu and usr point totals
    if int(CPU) >= int(USER):
        winna = int(CPU) - int(USER)
        print(f"the computer won by {winna} points!\nyou suck with buttons I guess.")
    elif int(CPU) <= int(USER):
        winna = int(USER) - int(CPU)
        print(f"You won by {winna} points!")
    elif int(CPU) == int(USER):
        print("a damn tie")   

def deal(): #makes new deck, shuffles, single deck
    url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"
    global payload 
    global headers
    response = requests.request("GET", url, headers=headers, data=payload)
    return response

def drawing_of_cards(deck_ID,draw_cnt):#for draw X number of cards
    global payload
    global headers
    url="https://deckofcardsapi.com/api/deck/"+ deck_ID + "/draw/?count="+draw_cnt
    response = requests.request("GET", url, headers=headers, data=payload)
    return response

def card_NUM_conv(card):#fucking this shit up! this little boi check to see if a card is a face card and coverts to 10, USE WITHIN FOR LOOP
    #points=0
    #for cardcpu in drawncards['cards']:
        #print(f"{cardcpu['value']} of {cardcpu['suit']}")
    if card['value'] == "KING":
            #print("face")
            card['value'] = "10"
    elif card['value'] == "QUEEN":
            #print("face")
            card['value'] = "10"
    elif card['value'] == "JACK":
            #print("face")
            card['value'] = "10"
    elif card['value'] == "ACE":
            #print("face")
            card['value'] = "10"
    #points = points + int(card['value'])
    #return points

def enforceCARD(draw_cnt,cardsREQ):
    enforce = True
    while enforce == True:
        if draw_cnt.isnumeric():
            if int(draw_cnt) >= 6:
                draw_cnt=input(cardsREQ)
                enforce=True
            else:
                enforce = False
        else:
            draw_cnt=input(cardsREQ)
            enforce=True


if __name__== "__main__" :
    main()