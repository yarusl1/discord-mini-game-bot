from .db import get_score, set_score
import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    
    def __str__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        for suit in suits:
            for value in values:
                self.cards.append(Card(suit, value))
    
    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
    
    def draw(self, deck):
        self.hand.append(deck.draw_card())
        return self
    
    def show_hand(self):
        for card in self.hand:
            print(card)
    
    def hand_value(self):
        value = 0
        ace = 0
        for card in self.hand:
            if card.value.isnumeric():
                value += int(card.value)
            elif card.value in ["J", "Q", "K"]:
                value += 10
            elif card.value == "A":
                ace += 1
                value += 11
        while value > 21 and ace:
            value -= 10
            ace -= 1
        return value

class Game:
    def __init__(self):
        name = input("What is your name? ")
        self.player = Player(name)
        self.deck = Deck()
        self.deck.shuffle()
        self.playing = True
    
    def play_game(self):
        while self.playing:
            self.player.draw(self.deck)
            self.player.draw(self.deck)
            self.player.show_hand()
            value = self.player.hand_value()
            print(f"Your hand value is {value}")
            choice = input("Do you want to draw another card? (Y/N) ")
            if choice.upper() == "N" or value >= 21:
                self.playing = False
        if value > 21:
            print("You lose!")
        else:
            print(f"Your final hand value is {value}")
            dealer_value = self.dealer_play()
            if value > dealer_value or dealer_value > 21:
                print("You win!")
            elif value < dealer_value:
                print("You lose!")
            else:
                print("It's a tie!")
        
    def dealer_play(self):
        dealer_hand = []
        dealer_hand.append(self.deck.draw_card())
        dealer_value = 0
        ace = 0
        while dealer_value < 17:
            dealer_hand.append(self.deck.draw_card())
            for card in dealer_hand:
                if card.value.isnumeric():
                    dealer_value += int(card.value)
                elif card.value in ["J", "Q", "K"]:
                    dealer_value += 10
                elif card.value == "A":
                    ace += 1
                    dealer_value += 11
            while dealer_value > 21 and ace:
                dealer_value -= 10
                ace -= 1
        print("Dealer's hand:")
        for card in dealer_hand:
            print(card)
        print(f"Dealer's hand value: {dealer_value}")
        return dealer_value