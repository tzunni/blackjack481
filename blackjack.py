import sys
import pygame
from dealer import Dealer
from ai import AI

class Blackjack:
    START = "START"
    PLAYER_TURN = "PLAYER_TURN"
    DEALER_TURN = "DEALER_TURN"
    GAME_OVER = "GAME_OVER"

    def __init__(self):
        self.ai = AI()
        pygame.init()
        self.dealer = Dealer()
        self.state = Blackjack.START  # Initial state

    def player_turn(self):
        print(f"Your hand: {self.player_hand}")
        while True:
            action = input("Choose action (hit/stand): ").lower()
            if action == "hit":
                self.player_hand.append(self.dealer.draw(1)[0])
                print(f"Your hand: {self.player_hand}")
                if sum(self.player_hand) > 21:
                    print("Bust!")
                    self.state = Blackjack.GAME_OVER
                    break
            elif action == "stand":
                self.state = Blackjack.DEALER_TURN
                break
            else:
                print("Invalid action. Please choose 'hit' or 'stand'.")

    def dealer_turn(self):
        while sum(self.dealer_hand) < 17:
            self.dealer_hand.append(self.dealer.draw(1)[0])
        self.state = Blackjack.GAME_OVER

    def game_over(self):
        player_total = sum(self.player_hand)
        dealer_total = sum(self.dealer_hand)
        print(f"Player: {player_total}, Dealer: {dealer_total}")
        if player_total > 21:
            print("Player busts! Dealer wins.")
        elif dealer_total > 21 or player_total > dealer_total:
            print("Player wins!")
        else:
            print("Dealer wins!")
        self.state = Blackjack.START

    def run(self):
        while True:
            if self.state == Blackjack.START:
                self.start_game()
            elif self.state == Blackjack.PLAYER_TURN:
                self.player_turn()
            elif self.state == Blackjack.DEALER_TURN:
                self.dealer_turn()
            elif self.state == Blackjack.GAME_OVER:
                self.game_over()