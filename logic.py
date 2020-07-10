#!/usr/bin/env python
import random
import Copy

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def points(self):
        if self.suit == "H" or self.suit == "D" and self.rank == "3":
            return 100
        elif self.rank == "2" or self.rank == "A":
            return 20
        elif self.rank == "Joker":
            return 50
        elif self.rank in "8910JQK":
            return 10
        else:
            return 5

    def __repr__(self):
        if(self.rank == "J"):
            r = "Jack"
        elif(self.rank == "Q"):
            r = "Queen"
        elif(self.rank == "K"):
            r = "King"
        elif(self.rank == "A"):
            r = "Ace"
        elif(self.rank == "Joker"):
            return "Joker"
        else:
            r = str(self.rank)

        if(self.suit == "H"):
            s = "Hearts"
        elif(self.suit == "D"):
            s = "Diamonds"
        elif(self.suit == "S"):
            s = "Spades"
        elif(self.suit == "C"):
            s = "Clubs"

        result = r + " of " + s
        return result


class Player:
    def __init__(self, hand, team_num):
        self.hand = hand
        self.team_num = team_num

class Team:
    def __init__(self, members, cards_played, red_threes, canastas, naturals, score):
        self.members = members
        self.score = score
        self.cards_played = cards_played
        self.red_threes = red_threes
        self.canastas = canastas
        self.naturals = naturals
        self.table = [ [], #Red threes (0)
                       [], #Black threes (1) (Only playable when going out)
                       [], #Fours (2)
                       [], #Fives (3)
                       [], #Sixes (4)
                       [], #Sevens (5)
                       [], #Eights (6)
                       [], #Nines (7)
                       [], #Tens (8)
                       [], #Jacks (9)
                       [], #Queens (10)
                       [], #Kings (11)
                       [] ] #Aces (12)

    def count_points(self):
        for c in self.cards_played:
            self.score += c.points()

class Deck:
    def __init__(self, contents, frozen):
        self.contents = contents
        self.frozen = frozen

######################################################################################################    

def init_deck():
    deck = Deck([], False)
    for i in range(2, 11):
        for j in "HHDDSSCC":    
            deck.contents.append(Card(j, str(i)))
    for i in "JQKA":
        for j in "HHDDSSCC": 
            deck.contents.append(Card(j, i))
    deck.contents.append(Card("X", "Joker"))
    deck.contents.append(Card("X", "Joker"))
    random.shuffle(deck.contents)
    return deck

######################################################################################################        

def deal(teams, deck):
    for i in range(0, 11):
        for t in teams:
            for m in t.members:
                m.hand.append(deck.contents.pop())

######################################################################################################    

def take_turn(player, player_turn, pile, deck, team):
    done = "no"
    print("Player " + str(player_turn) + ", your hand is: ")
    hand_count = 1
    for c in player.hand:
        print(str(hand_count) + ".) " + str(c))
        hand_count += 1
    move = input("Draw a card or pick up the pile?")

    if(move == "draw"):
        player.hand.append(deck.contents.pop())
        
    elif(move == "pick"):
        card_count = 0
        wild_count = 0
        top_card = pile.pop()
        if(top_card.rank != "2" and top_card.rank != "3" and top_card.rank != "Joker"):
            for c in player.hand:
                if(c.rank == top_card.rank):
                    card_count += 1
                if(c.rank == "2" or c.rank == "Joker"):
                    wild_count += 1
            
            if(deck.frozen):
                if(card_count >= 2):
                    player.hand = player.hand + Copy.copy(pile)
                    pile = []
            
            else:
                if(card_count >= 2 or (card_count >= 1 and wild_count >= 1)):
                    player.hand = player.hand + Copy.copy(pile)
                    pile = []
        
        else:
            print("Invalid selection")

    #PLAY STAGE

    ##############################################
    ############### TODO #########################
    ##############################################

    while(done == "no"):
        selection = input("Select a card to play")
        in_hand = false

        for c in player.hand:
            if(c.rank == selection):
                in_hand = true
        if(in_hand == false):
            print("Invalid selection")


        done = input("Are you done?")
    

    #DISCARD STAGE
    discard = int(input("Choose a discard"))
    discarded_card = player.hand.pop(discard - 1)
    #If a wild is played, freeze the deck
    if(discarded_card.rank == "2" or discarded_card.rank == "Joker"):
        deck.frozen = True
    pile.append(discarded_card)

######################################################################################################    

def play_game():
    #Essential flags
    player_turn = 0
    game_over = False

    #Initializing players, teams, and deck
    num_players = int(input("How many players? (2, 4, or 6): "))
    teams = []
    for i in range(0, 2):
        if(num_players >= 2):
            teams.append(Team([Player([], 0)], [], 0, 0, 0, 0))
            teams.append(Team([Player([], 1)], [], 0, 0, 0, 0))
        elif(num_players == 4):
            teams.append(Team([Player([], 0), Player([], 0)], [], 0, 0, 0, 0))
            teams.append(Team([Player([], 1), Player([], 1)], [], 0, 0, 0, 0))
        elif(num_players == 6):
            teams.append(Team([Player([], 0), Player([], 0), Player([], 0)], [], 0, 0, 0, 0))
            teams.append(Team([Player([], 1), Player([], 1), Player([], 1)], [], 0, 0, 0, 0))
    deck = init_deck()
    pile = []

    deal(teams, deck)

    #FIRST CARD
    pile.append(deck.contents.pop())

    #OVERALL GAMEPLAY LOOP
    while(not game_over):
        if(player_turn % 2 == 0):
            team_num = 0
        else:
            team_num = 1
        take_turn(teams[team_num].members[player_turn // 2], player_turn, pile, deck, teams[team_num])
        player_turn += 1
        if(player_turn > num_players - 1):
            player_turn = 0


        #End Game conditions
        for t in teams:
            for p in t.members:
                if(len(p.hand) <= 0 and t.canastas >= 1):
                    game_over = True
        if(len(deck.contents) <= 0):
            game_over = True







    
