#!/usr/bin/env python3
#written by Josh Patch....i'm sure there are some issues with this but i didn't consult chatgtp or anything else so pretty proud of this
import requests

#url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"
payload ={}
headers ={}
def main():
    
    #rules="ok so the game is cpu draws card and you draw cards\nyou can choose the number of cards drawn (between 1 and 5)\nthen the cards are totaled up and whoever\nhas the most wins\noh almost forgot face cards are worth 10 points."
    cardsREQ= "how many card would you like us both to draw for our war?\n0-5 (0 means quit btw): "
    asking_num_decks="how many Decks? "
    #print(rules)
    printrulez()
    #ask number of decks
    askdecks = input(asking_num_decks)
    deck_number=get_many_deck(askdecks,asking_num_decks)
    response_MAIN=shuffle_deck(deck_number)
    deck = response_MAIN.json()
    
    deck_ID=deck['deck_id']
    #print(f"Deck ID is {deck_ID}\n")
    
    #ask number of cards
    draw_cnt = input(cardsREQ)
    enforceCARD(draw_cnt,cardsREQ)

    #draw cards
    responsecpu = drawing_of_cards(deck_ID,draw_cnt)
    drewcpu = responsecpu.json()

    #draw and add up cpu cards
    print("the computer draws:")
    cpupoints = score(drewcpu)
    print(f"and got {cpupoints} points\n")

    #draw and add up usr cards
    print("you draw:")
    usrresponse = drawing_of_cards(deck_ID,draw_cnt)
    drewusr =usrresponse.json()
    usrpoints = score(drewusr)
    print(f"and got {usrpoints} points\n")

    who_won(cpupoints,usrpoints)

def score(player):
    points = 0
    for card in player['cards']:
        print(f"{card['value']} of {card['suit']}")
        card_NUM_conv(card)
        points = points + int(card['value'])
    return points

def who_won(cpu,user): #run compare logic against cpu and usr point totals
    if int(cpu) > int(user):
        winna = int(cpu) - int(user)
        print(f"the computer won by {winna} points!\nyou suck with buttons I guess.")
    elif int(cpu) < int(user):
        winna = int(user) - int(cpu)
        print(f"You won by {winna} points!")
    elif int(cpu) == int(user):
        print("a damn tie")   


def shuffle_deck(deckcnt): #makes new deck, shuffles, 
    url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=" + deckcnt
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

def card_NUM_conv(card):# this boi checks to see if a card is a face card and coverts to 10, USE WITHIN FOR LOOP
    if card['value'] == "KING":
            card['value'] = "10"
    elif card['value'] == "QUEEN":
            card['value'] = "10"
    elif card['value'] == "JACK":
            card['value'] = "10"
    elif card['value'] == "ACE":
            card['value'] = "10"
    

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
def printrulez():
    rules ="ok so the game is cpu draws card and you draw cards\nyou can choose the number of cards drawn (between 1 and 5)\nthen the cards are totaled up and whoever\nhas the most wins\noh almost forgot face cards are worth 10 points."
    print(rules)
if __name__== "__main__" :
    main()

#https://github.com/jpatchMC/SDNscripts/tree/main/week4