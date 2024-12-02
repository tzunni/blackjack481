import pygame
import json
import random
from card_counter import CardCounter


class Dealer:
    def __init__(self):
        with open('cards.txt', 'r') as file:
            self.deck = json.load(file) # load the deck of cards
        random.shuffle(self.deck)
        self.temp_deck = self.deck.copy()
        self.hand = self.draw(2) # draw two cards to start
        self.card_counter = CardCounter() # ai will begin card counting
        while sum(self.hand) < 17:
            self.hand.append(self.draw(1)[0]) # draw until hand is at least 17, dealer rules
    def draw(self, n):
        cards_drawn = []
        for _ in range(n):
            card = random.choice(self.temp_deck)
            self.temp_deck.remove(card)
            cards_drawn.append(card)
            self.card_counter.update_count(card)  # Update count here
        return cards_drawn
        pass