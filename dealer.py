import pygame
import json
import random
import sys
from pygame.locals import *
from card_counter import CardCounter
from deck import Deck


class Dealer:
  def __init__(self):
    self.deck = Deck()
    # self.temp_deck = self.deck.copy()
    self.deck.create_deck()
    self.deck.shuffle_deck()
    self.hand = []
    self.card_counter = CardCounter() # ai will begin card counting
    self.count = 0
    self.x = 400
    self.y = 100
    # while sum(self.hand) < 17:
    #   self.hand.append(self.draw(1)[0]) # draw until hand is at least 17, dealer rules

  # Function to create two card hard for the dealer to start with
  def create_dealer_hand(self):
      for i in range(1, 3):
          self.add_card()

  # Function uses the deal_card() to deal a card to a player
  def dealt_card(self):
    return self.deck.deal_card()

  # Function that allows the dealer to deal itself a card and also account for the dealer's count
  def add_card(self):
      dealer_card = self.dealt_card()
      self.hand.append(dealer_card)
      self.count += dealer_card.value
      self.count_ace()

# Function prints the dealer's hand
  def print_dealer_hand(self):
     print("")
     print("Dealer's Hand: ")
     for dealer_card in self.hand:
        print("Suit: " + dealer_card.suit + "\nLabel: " + str(dealer_card.label))

# Function will print the dealer's count
  def print_dealer_count(self):
    print("")
    print("Dealer's Count: " + str(self.count))

# Function to consider all aces in a dealer's hand to give them the closest count under 21
  def count_ace(self):
     if self.count <= 21:
      for card in self.hand:
         if card.label == "A":
            self.count += 10
            if self.count > 21:
               self.count -= 10
               break

# Function will draw all the cards in a hand
  def draw_hand(self, surface):
     from constants import add_text, font, screen, white
     card_width, card_height = 78, 120
     card_gap = 20
     player_box_length, player_box_height = card_width + (card_gap * (len(self.hand) - 1)), card_height
     player_top_left_x = self.x - (0.5 * player_box_length)
     player_top_left_y = self.y - (0.5 * player_box_height)

     for card in self.hand:
        if card == self.hand[1]:
           draw_card = pygame.image.load("Assets/Cards/Back/red_design_back.png")
        else:
           draw_card = pygame.image.load("Assets/Cards/" + str(card.suit) + "/" + str(card.label) + ".png")
        resized_card = pygame.transform.scale(draw_card, (card_width, card_height))
        surface.blit(resized_card, (player_top_left_x, player_top_left_y))
        pygame.display.update()
        player_top_left_x += card_gap
     name_x = self.x
     name_y = self.y
     add_text("DEALER", font, screen, name_x, name_y, white)
     deck_x = 400 - (0.5 * card_width)
     deck_y = 100 - (0.5 * card_height)
     for card in range(1, 7):
        deck_card = pygame.image.load("Assets/Cards/Back/red_design_back.png")
        back_card = pygame.transform.scale(deck_card, (card_width, card_height))
        surface.blit(back_card, (deck_x, deck_y))
        deck_x += card_gap
