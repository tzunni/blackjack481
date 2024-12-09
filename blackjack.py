import pygame
from dealer import Dealer
from ai import AI
from deck import Deck


class Blackjack:
    START = "START"
    PLAYER_TURN = "PLAYER_TURN"
    DEALER_TURN = "DEALER_TURN"
    GAME_OVER = "GAME_OVER"

    def __init__(self):
        pygame.init()
        self.dealer = Dealer()
        self.deck = Deck()
        self.ai = AI("historical_data.csv", self.calculate_hand_value)
        self.ai.set_card_counter(self.dealer.card_counter)
        self.state = Blackjack.START
        self.player_hand = []
        self.dealer_hand = []

    def start_game(self):
        print("Starting Blackjack game...")
        self.deck.reset_deck()
        self.player_hand = [self.deck.deal_card(), self.deck.deal_card()]
        self.dealer_hand = [self.deck.deal_card(), self.deck.deal_card()]
        print(f"Your hand: {self.player_hand}")
        print(f"Dealer's visible card: {self.dealer_hand[0]}")
        self.state = Blackjack.PLAYER_TURN

    def player_turn(self):
        print(f"Player's hand: {self.player_hand}")
        while True:
            action = self.ai.decide_action(self.player_hand, self.dealer_hand, remaining_decks=1)
            print(f"AI chose to: {action}")

            if action == "hit":
                self.player_hand.append(self.deck.deal_card())
                print(f"Player's hand: {self.player_hand}")
                if self.calculate_hand_value(self.player_hand) > 21:
                    print("Bust!")
                    self.state = Blackjack.GAME_OVER
                    break
            elif action == "stand":
                self.state = Blackjack.DEALER_TURN
                break

    def dealer_turn(self):
        print(f"Dealer's hand: {self.dealer_hand}")
        while self.calculate_hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.deal_card())
            print(f"Dealer's hand: {self.dealer_hand}")
        self.state = Blackjack.GAME_OVER

    def game_over(self):
        player_total = self.calculate_hand_value(self.player_hand)
        dealer_total = self.calculate_hand_value(self.dealer_hand)
        print(f"Player: {player_total}, Dealer: {dealer_total}")

        if player_total > 21:
            print("Player busts! Dealer wins.")
            win_rate = 0
        elif dealer_total > 21:
            print("Dealer busts! Player wins.")
            win_rate = 1
        elif player_total > dealer_total:
            print("Player wins!")
            win_rate = 1
        elif player_total < dealer_total:
            print("Dealer wins!")
            win_rate = 0
        else:
            print("It's a tie!")
            win_rate = 0.5

        dealer_visible_card = self.dealer_hand[0]
        action_taken = "stand" if self.state == Blackjack.DEALER_TURN else "hit"
        self.ai.log_game_result(
            player_total,
            self.deck.card_values(dealer_visible_card),
            action_taken,
            win_rate
        )
        self.state = Blackjack.START

    def calculate_hand_value(self, hand):
        return self.deck.calculate_hand_value(hand)

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


if __name__ == "__main__":
    game = Blackjack()
    game.run()
