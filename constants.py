import pygame
from pygame.locals import *
import sys
from dealer import Dealer
from player import Player

pygame.init()  # Initialize pygame

# Screen dimensions
screen_w = 900
screen_h = 700
half_width, half_height = screen_w // 2, screen_h // 2
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Blackjack")

# Colors
black = (0, 0, 0)
green = (34, 139, 34)
white = (255, 255, 255)

# Font
font = pygame.font.SysFont("Poppins", 25)
large_font = pygame.font.SysFont("Poppins", 60)  # Larger font
medium_font = pygame.font.SysFont("Poppins", 36)  # Medium font

# Logo
logo = pygame.image.load("Assets/Icons/BlackJack.png")

# Global Variables listed
player = []
which_player = 1
dealer = Dealer()
start_y = 50

# win, loss, draw/push
round = 0
records = [0, 0, 0]
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
outcome = 0
add_score = False
results = ['', 'PLAYER BUSTED o_O', 'Player WINS! :)', 'DEALER WINS :(', 'TIE GAME...']



# Function to add text to the game
def add_text(text, font, surface, x, y, text_color):
  text_object = font.render(text, False, text_color)
  text_width = text_object.get_rect().width
  text_height = text_object.get_rect().height
  surface.blit(text_object, (x - (text_width / 2), y - (text_height / 2)))
# Function to create start screem
def start_game():
  pygame.init()
  screen.fill(green)
  pygame.display.set_caption("Welcome")
  add_text("Blackjack Minimax", font, screen, half_width, half_height, white)
  add_text("PRESS SPACE TO CONTINUE", font, screen, half_width, half_height + 100, white)
  pygame.display.update()

  beginning = True
  while beginning:
    for event in pygame.event.get():
      if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
        pygame.quit()
        sys.exit()
      if event.type == KEYDOWN and event.key == K_SPACE:
        beginning = False

# Function to display the user instructions & rules to our game
# def showInstructions():
#     pygame.init()
#     pygame.display.set_caption("How to Play")
#     screen.fill(green)
#     add_text("Goal of the Game:", font, screen, half_width, 50, white)
#     add_text("To get the closest to 21 without going over in order for you to make money.", font, screen, half_width, 80, white)
#     add_text("Basic Rules:", font, screen, half_width, 130, white)
#     add_text("Cards 2 - 10 = face value        Jack, Queen, King = 10        Ace = 1 or 11", font, screen, half_width, 160, white)
#     add_text("Press H to Hit (Gets a card)        Press P to Pass (Finishes turn)", font, screen, half_width, 210, white)
#     add_text("You may hit as much as you want, however, once you pass 21, you bust and your turn is over.", font, screen, half_width, 260, white)
#     add_text("If you get to 21 with your first two cards, you blackjack, and you sit out for that round.", font, screen, half_width, 300, white)
#     pygame.display.update()
#     print("Inside 2")
#     instructions = True
#     while instructions:
#         for event in pygame.event.get():
#             if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
#                 pygame.quit()
#                 sys.exit()
#             if event.type == KEYDOWN and event.key == K_SPACE:
#                 print("Inside 2")
#                 instructions = False


# Function to determine if it wil be AI Agent against dealer or two AI agents against dealer
# def get_which_agent():
#   global which_player
#   pygame.init()
#   screen.fill(green)
#   user_input = 0
#   answered = False
#   print("Inside 3")
#   while answered is False:
#     pygame.display.set_caption("Which AI Agent")
#     button_1 = pygame.Rect(150, 400, 250, 100)
#     draw_button(screen, button_1, "Press 1 for AI Minimax Agent", 24)
#     button_2 = pygame.Rect(500, 400, 250, 100)
#     text = "Press 2 for Regular AI Agent"
#     draw_button(screen, button_2, text, 24)
#     add_text("Choose which AI Agent is going to be playing.", font, screen, half_width, half_height - 50, white)
#     pygame.display.update()
#     for event in pygame.event.get():
#       if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
#         pygame.quit()
#         sys.exit()
#       if event.type == KEYDOWN and event.key == K_SPACE:
#         print("Inside 3")
#         answered = True
    #   if event.type == KEYDOWN and event.key == K_1:
    #     user_input = 1
    #     answered = True
    #   if event.type == KEYDOWN and event.key == K_2:
    #     user_input = 2
    #     which_player = user_input
    #     answered = True
    # return user_input

# Function to set the names of the AI Agent(s)
def get_player_names():
  global player, which_player
  print("Inside 4")
  player_1 = "AI Agent Minimax"
  player_2 = "Other AI Agent"
  if which_player == 1:
    player.append(Player(player_1))
  if which_player == 2:
    player.append(Player(player_2))

# Function that will set the coordinates for the dealer and AI agent
def player_coordinates():
  global player, which_player
  print("Inside 5")
  if which_player == 1 or which_player == 2:
    player[0].x = half_width
    player[0].y = 650

# Function that will let the player start the game
# def deal():

# Function to restore all the cards to the deck for a new round
def new_deck():
   global dealer
   print("Inside 6")
   dealer = Dealer()

# Function to create the hands of the dealer and all the players
def create_hands():
   global dealer
   print("Inside 7")
   dealer.create_dealer_hand()
   for i in range(1, 3):
      agent = player[0]
      card = dealer.dealt_card()
      agent.add_card(card)

# Function to check for blackjacks
def check_blackjack():
  print("Inside 8")
  agent = player[0]
  if agent.count == 21:
    print("")
    print(agent.name + ", you got a BLACKJACK!")
    agent.blackjack = True

#Function to run the turns of the agent and dealer, allowing to hit or pass
def play_turns():
  global round
  print("Inside 9")
  pygame.init()
  round += 1
  pygame.display.set_caption("Play Round " + str(round))
  draw_turn()
  agent = player[0]
  agent.print_hand()
  dealer.print_dealer_count()
  end_turn()

  # choice = agent.ask_choice()
  # if choice == 1:
  #   keep_hitting = True
  #   while keep_hitting:
  #     hit_card = dealer.dealt_card()
  #     agent.add_card(hit_card)
  #     draw_turn(screen)
  #     agent.print_hand()
  #     if agent.count > 21:
  #       print("")
  #       print(str(player.name) + ", you busted. The Dealer gets your bet.")
  #       player.bust = True
  #       player.resetBet()
  #       break
  #     choice = agent.ask_choice()
  #     if choice != 1:
  #       keep_hitting = False

# Function to draw the screen every time an action is conducted in the playing of the game
def draw_turn():
    global players, dealer
    print("Inside 10")
    screen.fill(green)
    dealer.draw_hand(screen)
    for agent in player:
        agent.draw_hand(screen)
    pygame.display.update()

# function to reveal the face down card of the dealer, and if the dealer has to force hit he will do so
def revealDealerHand(surface):
    global dealer, start_y
    dealer_bust = False
    while dealer.count <= 16:
        dealer.add_card()
    if dealer.count > 21:
        print("")
        print("The Dealer busted. You all got double your bets.")
        start_y += 50
        add_text("The Dealer busted. You all got double your bets.", font, screen, half_width, start_y, white)
        dealer_bust = True
    dealer.print_dealer_hand()
    dealer.print_dealer_count()
    return dealer_bust

# function to see how the bets are retrieved based on counts
def compare_counts(surface):
    global players, dealer, start_y
    print("Inside 12")
    no_counts = True
    highest_count = 0
    for agent in player:
        if 21 >= agent.count > highest_count:
            highest_count = agent.count
            no_counts = False
    if no_counts is False:
        for agent in player:
            if agent.count == highest_count and highest_count > dealer.count and agent.blackjack is False:
                print("")
                print(str(agent.name) + ", you won twice your bet")
                start_y += 50
                add_text(str(agent.name) + ", you won twice your bet.", font, surface, half_width, start_y, white)
            elif agent.count == dealer.count and agent.blackjack is False:
                print("")
                print(str(agent.name) + ", you got your bet back.")
                start_y += 50
                add_text(str(agent.name) + ", you got your bet back.", font, surface, half_width, start_y, white)
            elif agent.count < dealer.count and agent.blackjack is False:
                print("")
                print(str(agent.name) + ", the dealer took your bet.")
                start_y += 50
                add_text(str(agent.name) + ", the dealer took your bet.", font, surface, half_width, start_y, white)
            elif agent.bust:
                start_y += 50
                add_text(str(agent.name) + " busted.", font, surface, half_width, start_y, white)
            elif agent.blackjack:
                start_y += 50
                add_text(str(agent.name) + " got a blackjack.", font, surface, half_width, start_y, white)
    else:
        start_y += 50
        add_text("You all busted.", font, surface, half_width, start_y, white)

# # function to check for a winner, basically when a person reaches a certain target amount of money
# def checkWinner(surface):
#     global round_over, game_over, start_y
#     highest_bank = 0
#     winner_present = False
#     for agent in player:
#         if agent.bank > highest_bank and agent.bank >= 200:
#             highest_bank = agent.bank
#             winner_present = True
#     if winner_present:
#         for agent in player:
#             if agent.bank == highest_bank:
#                 print("")
#                 print(str(agent.name) + ", YOU WON THE GAME.")
#                 startY += 50
#                 add_text(str(agent.name) + ", YOU WON THE GAME.", font, surface, half_width, start_y, white)
#             roundOver = True
#         gameOver = True


def end_turn():
   round_over = True


# Main loop
game_started = False
instructions_shown = False
game_over = False

while not game_over:
  # start_game()  # Show start screen
  # showInstructions()  # Show instructions once
  # get_which_agent()

  get_player_names()
  player_coordinates()
  round_over = False
  while round_over is False:
    new_deck()
    create_hands()
    # check_blackjack()
    play_turns()
    round_over = True
    # compare_counts(screen)

    # # Create button frame
    # frame_rect = pygame.Rect(200, 150, 500, 300)
    # # pygame.draw.rect(screen, green, frame_rect, border_radius=15)

    # # Create buttons
    # draw_button(screen, pygame.Rect(220, 200, 120, 50), "Shuffle", 24)
    # draw_button(screen, pygame.Rect(380, 200, 120, 50), "Card", 24)
    # draw_button(screen, pygame.Rect(540, 200, 120, 50), "Stand", 24)

    # # Event handling
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         running = False

    # pygame.display.flip()

# pygame.quit()
# sys.exit()
