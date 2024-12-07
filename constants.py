import pygame
from pygame.locals import *
import sys
from dealer import Dealer

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

# Logo
logo = pygame.image.load("Resources/Icons/BlackJack.png")

# Global Variables listed
# dealer = Dealer()

# Function to draw buttons
def draw_button(screen, rect, text, font_size):
    font = pygame.font.Font(None, font_size)
    mouse_pos = pygame.mouse.get_pos()
    color = (0, 120, 215) if rect.collidepoint(mouse_pos) else (200, 200, 200)
    pygame.draw.rect(screen, color, rect, border_radius=10)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

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
  title_logo = pygame.transform.scale(logo, (900, 800))
  logo_x = title_logo.get_width()
  logo_y = title_logo.get_height()
  screen.blit(title_logo, (half_width - (0.5 * logo_x), half_height - (0.5 * logo_y) - 25))
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
def showInstructions():
    pygame.init()
    pygame.display.set_caption("How to Play")
    screen.fill(green)
    add_text("Goal of the Game:", font, screen, half_width, 50, white)
    add_text("To get the closest to 21 without going over in order for you to make money.", font, screen, half_width, 80, white)
    add_text("Basic Rules:", font, screen, half_width, 130, white)
    add_text("Cards 2 - 10 = face value        Jack, Queen, King = 10        Ace = 1 or 11", font, screen, half_width, 160, white)
    add_text("Press H to Hit (Gets a card)        Press P to Pass (Finishes turn)", font, screen, half_width, 210, white)
    add_text("You may hit as much as you want, however, once you pass 21, you bust and your turn is over.", font, screen, half_width, 260, white)
    add_text("If you get to 21 with your first two cards, you blackjack, and you sit out for that round.", font, screen, half_width, 300, white)
    pygame.display.update()
    instructions = True
    while instructions:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                instructions = False

# Function that will set the coordinates for the dealer and AI agent

# Main loop
game_over = False
while game_over is False:
    start_game()
    showInstructions()

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
