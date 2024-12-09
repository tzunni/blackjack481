import pygame
import sys
from pygame.locals import *

class Player:
  def __init__(self, name):
    self.name = name
    self.hand = []
    self.count = 0
    self.blackjack = False
    self.bust = False
    self.rounds_won = 0
    self.x = 0
    self.y = 0
    self.current_turn = False

  # Function asks the player for their choice of action when it is their turn
  def ask_choice(self):
    player_input = 0
    answered = False
    while answered is False:
      for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
          pygame.quit()
          sys.exit()
        if event.type == KEYDOWN and event.key == K_h:
          player_input = 1
          answered = True
        if event.type == KEYDOWN and event.key == K_s:
          player_input = 2
          answered = True
      return player_input

  # Function that adds a card provided by the dealer to the player's hand
  def add_card(self, card):
    self.hand.append(card)
    self.count_cards()
    print(str(self.name) + "'s Count: " + str(self.count))

  # Function prints the player's hand
  def print_hand(self):
    print("")
    print(str(self.name) + "'s Hand: ")
    for playerCard in self.hand:
      print("Suit - " + playerCard.suit + "\nLabel - " + str(playerCard.label))

  # Function prints the player's count
  def printCount(self):
    print("")
    print(str(self.name) + "'s Count: " + str(self.count))

  # Function resets the player's hand
  def resetHandAndCount(self):
    self.hand = []
    self.count = 0

  # Function considers all aces in aces in a player's hand to give them the cloest count under 21
  def count_cards(self):
    self.count = 0
    for card in self.hand:
      self.count += card.value
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
    name_color = (255, 255, 255)
    if self.current_turn:
      name_color = (51, 235, 255)
      add_text("Hit(H) or Pass(P)", font, screen, self.x, self.y - (0.75 * card_height), name_color)
    if self.bust:
      bust = pygame.image.load("Assets/Icons/Bust.png")
      bust_width = bust.get_width()
      bust_height = bust.get_height()
      surface.blit(bust, (self.x - (0.5 * bust_width), self.y - (0.5 * bust_height)))
      if self.blackjack:
        blackjack = pygame.image.load("Assets/Icons/BlackJack.png")
        bj_width = blackjack.get_width()
        bj_height = blackjack.get_height()
        surface.blit(blackjack, (self.x - (0.5 * bj_width), self.y - (0.5 * bj_height)))
      add_text(str(self.name) + "   $" + str(self.bank), font, screen, name_x, name_y, name_color)

  # Function resets everything for the next round
  def resetState(self):
    self.bust = False
    self.blackjack = False
