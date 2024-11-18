import sys
import pygame
from dealer import Dealer

class Blackjack:
    def __init__(self):
        pygame.init()
        self.dealer = Dealer()