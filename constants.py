import pygame as pygame 

pygame.init() #initialize pygame

screen_w = 900
screen_h = 700
pygame.display.set_mode((screen_w,screen_h)) #screen dimensions

background_color = (255,0,0)

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	pygame.display.flip()