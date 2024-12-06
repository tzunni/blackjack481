import pygame
import sys

pygame.init()  # Initialize pygame

# Screen dimensions
screen_w = 900
screen_h = 700
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Blackjack")

# Colors
black = (0, 0, 0)
green = (34, 139, 34)

# Font
font = pygame.font.SysFont("Times New Roman", 25)

# Function to draw buttons
def draw_button(screen, rect, text, font_size):
    font = pygame.font.Font(None, font_size)
    mouse_pos = pygame.mouse.get_pos()
    color = (0, 120, 215) if rect.collidepoint(mouse_pos) else (200, 200, 200)
    pygame.draw.rect(screen, color, rect, border_radius=10)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# Main loop
running = True
while running:
    screen.fill(black)

    # Create button frame
    frame_rect = pygame.Rect(200, 150, 500, 300)
    pygame.draw.rect(screen, green, frame_rect, border_radius=15)

    # Create buttons
    draw_button(screen, pygame.Rect(220, 200, 120, 50), "Shuffle", 24)
    draw_button(screen, pygame.Rect(380, 200, 120, 50), "Card", 24)
    draw_button(screen, pygame.Rect(540, 200, 120, 50), "Stand", 24)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
