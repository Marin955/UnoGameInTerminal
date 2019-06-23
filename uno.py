import random as rd

gameOver = False
direction_switch = False

#defining players, 5 of them

players = [[], [], [], [], []]

#this is later used to know which players turn is it

turn_number = -1

played_cards = []

#       rd9 is RED 9, bl3 is BLUE 3 and so on...
#       +4_ is +4,  blk is a blank black card, 
#       r+2 is RED +2 card, bsk is BLUE SKIP card, 
#       ysw is the YELLOW SWITCH DIRECTION card

all_cards = ["rd0", "rd1", "rd2", "rd3", "rd4", "rd5", "rd6", "rd7", "rd8", "rd9", "rd1", "rd2", "rd3", "rd4", "rd5", "rd6", "rd7", "rd8", "rd9",
        "gr0", "gr1", "gr2", "gr3", "gr4", "gr5", "gr6", "gr7", "gr8", "gr9", "gr1", "gr2", "gr3", "gr4", "gr5", "gr6", "gr7", "gr8", "gr9",
        "yl0", "yl1", "yl2", "yl3", "yl4", "yl5", "yl6", "yl7", "yl8", "yl9", "yl1", "yl2", "yl3", "yl4", "yl5", "yl6", "yl7", "yl8", "yl9",
        "bl0", "bl1", "bl2", "bl3", "bl4", "bl5", "bl6", "bl7", "bl8", "bl9", "bl1", "bl2", "bl3", "bl4", "bl5", "bl6", "bl7", "bl8", "bl9",
        "+4_", "+4_", "+4_", "+4_", "blk", "blk", "blk", "blk", "r2+", "r2+", "y2+", "y2+", "b2+", "b2+", "g2+", "g2+",
        "bsk", "bsk", "gsk", "gsk", "rsk", "rsk", "ysk", "ysk", "bsw", "bsw", "gsw", "gsw", "rsw", "rsw", "ysw", "ysw"]

deck = list.copy(all_cards)

colors = ["g", "r", "y", "b"]

#draw a random card from the deck

def draw_card():
    
    global deck
    
    card_index = rd.randint(0, len(deck) - 1 )
    return deck.pop(card_index)

#in case the deck becomes too small, refill it with cards that were already played

def refill():
    
    global players
    global deck
    global all_cards
    global played_cards
    
    last_card = played_cards[-1]
    new_deck = list.copy(all_cards)
    for i in range(3):
        for card in players[i]:
            new_deck.remove(card)
    deck = new_deck
    played_cards.clear()
    played_cards.append(last_card)

#   Method which essentially "reads" the last card that was played, retrieves the color and the number 
#   and checks if it's one of the special cards like +4

def play(player):
    
    global played_cards
    global deck
    
    last_card_played = played_cards[-1]
    
    # player sees the +4 card without the "f" on the end of it, player draws the 4 cards and adds the "f" to the last position
    # to let the next player know that he doesn't need to draw the 4 cards again
    
    if(last_card_played[0:3] == "+4_" and last_card_played[len(last_card_played) - 1] != "f"):
        if(len(deck) < 10):
            refill()
        for i in range(4):
            player.append(draw_card())
        played_cards[-1] = "" + played_cards[-1] + "f"
    
    elif(last_card_played[0:3] == "+4_" and last_card_played[len(last_card_played) - 1] == "f"):
        color = last_card_played[3]
        throw_a_card(player, color)
    
    # if the card was blank black card, then check which color was defined by the player who threw the card
    # the information about the color is located after the card name, for example "blky" means yellow
    
    elif(last_card_played[0:3] == "blk"):
        color = last_card_played[3]
        throw_a_card(player, color)
    
    # +2, works similarly to +4
    elif(last_card_played[1:3] == "2+" and last_card_played[len(last_card_played) - 1] != "f"):
        if(len(deck) < 10):
            refill()
        for i in range(2):
            player.append(draw_card())
        played_cards[-1] = "" + played_cards[-1] + "f"
    
    elif(last_card_played[1:3] == "2+" and last_card_played[len(last_card_played) - 1] == "f"):
        color = last_card_played[0]
        throw_a_card(player, color)
    
    # the skip card, player who sees it just adds the "f" to the end of the card and that's all he does that turn
    
    elif(last_card_played[1:3] == "sk" and last_card_played[len(last_card_played) - 1] != "f"):
        played_cards[-1] = "" + played_cards[-1] + "f"
    
    elif(last_card_played[1:3] == "sk" and last_card_played[len(last_card_played) - 1] == "f"):
        color = last_card_played[0]
        throw_a_card(player, color)
    
    # direction switch is handled later, in the method where the card is being thrown
    
    elif(last_card_played[1:3] == "sw"):
        color = last_card_played[0]
        throw_a_card(player, color)
    
    # if it's not a special card, then find which of the numbered cards it is
    
    else:
        for i in range(76):
            if(last_card_played == all_cards[i]):
                color = last_card_played[0]
                number = last_card_played[2]
                throw_a_card(player, color, number)
                break

def throw_a_card(player, color = "", number = ""):
    
    global direction_switch
    global played_cards
    global colors
    global gameOver
    global deck
    
    need_to_draw_a_card = True
    
    # Go through all of the cards in the players deck
    # if a playable card is found, then it is played
    # if not, then the player has to draw a card
    
    for card in player:
        if(card[0] == color or card[2] == number or card == "+4_" or card == "blk"):
            if(card[1:3] == "sw"):
                
                # direction switch
                direction_switch = not direction_switch
                
                index = player.index(card)
                played_cards.append(player.pop(index))
                
                need_to_draw_a_card = False
                if(len(player) == 0):
                    gameOver = True
                break
            
            elif(card == "+4_"):
                index = player.index(card)
                played_cards.append(player.pop(index))
                
                # if the player plays a black card, then he adds a random color to the end of it
                played_cards[-1] = "" + played_cards[-1] + colors[rd.randint(0,3)]
                
                need_to_draw_a_card = False
                if(len(player) == 0):
                    gameOver = True
                break
            
            elif(card == "blk"):
                index = player.index(card)
                played_cards.append(player.pop(index))
                
                played_cards[-1] = "" + played_cards[-1] + colors[rd.randint(0,3)]
                
                need_to_draw_a_card = False
                if(len(player) == 0):
                    gameOver = True
                break
            
            else:
                index = player.index(card)
                played_cards.append(player.pop(index))
                
                if(len(player) == 0):
                    gameOver = True
                need_to_draw_a_card = False
                break
    
    if(need_to_draw_a_card):
        if(len(deck) < 10):
            refill()
        player.append(draw_card())
        
# Printing the instructions to the terminal screen
print("###################################################")
print("#    WATCH THE COMPUTER PLAY UNO WITH HIMSELF!    #")
print("#                                                 #")
print("#    Press Enter to continue to the next move     #")
print("#                                                 #")
print("#    Numbered cards are labeled as \"gr8\"          #")
print("#    which just means GREEN 8                     #")
print("#                                                 #")
print("#    \"blk\" --- BLANK BLACK CARD                   #")
print("#    \"gsw\" --- GREEN SWITCH CARD                  #")
print("#    \"+4_\" --- +4 CARD                            #")
print("#    \"ysk\" --- YELLOW SKIP CARD                   #")
print("#    \"r2+\" --- RED +2 CARD                        #")
print("#                                                 #")
print("###################################################")

#dealing 7 cards to all 5 players

for i in range(5):
    for j in range(7):
        players[i].append(draw_card())

# set one card "on the table" to begin the game

played_cards.append(draw_card())

#   MAIN GAME LOOP
#   players alternate and play the game
#------------------------------

while(not(gameOver)):
    
    # if the direction switch card was played, then the players start playing in the opposite direction
    
    if(direction_switch):
        turn_number -= 1
    else:
        turn_number += 1
    
    # Printing the game state
    
    print("------------------------------")
    print("Player " + str(turn_number%5+1 ) + "'s turn!")
    print("------------------------------\n")
    print("Player " + str(turn_number%5+1 ) + ": " + str(players[turn_number%5]))
    print("Player " + str((turn_number+1)%5+1) + ": " + str(players[(turn_number+1)%5]))
    print("Player " + str((turn_number+2)%5+1) + ": " + str(players[(turn_number+2)%5]))
    print("Player " + str((turn_number+3)%5+1) + ": " + str(players[(turn_number+3)%5]))
    print("Player " + str((turn_number+4)%5+1) + ": " + str(players[(turn_number+4)%5]) + "\n\n")
    print("Cards that were played: \n" + str(played_cards) + "")
    
    # Waiting for the Enter key to be pressed
    input()
    
    # calling the method to make the player play the next move
    play(players[turn_number%5])
    
#------------------------------

