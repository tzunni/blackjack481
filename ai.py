import csv
from collections import Counter

class AI:
    def __init__(self):
        self.card_counter = None  # Reference to the card counter
        self.card_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]  # Card values in a single deck
        self.deck_count = Counter(self.card_values * 4)  # Counter for single deck

    def set_card_counter(self, card_counter):
        self.card_counter = card_counter

    def decide_action(self, player_hand, dealer_hand):
        """
        Decide the best action using minimax for a single deck.
        :param player_hand: List of the player's card values.
        :param dealer_hand: List of the dealer's card values.
        :return: "hit" or "stand"
        """
        best_action = "stand"
        best_score = float("-inf")

        # Simulate hitting
        for card in self.get_remaining_cards():
            new_hand = player_hand + [card]
            self.update_deck(card, remove=True)  # Temporarily remove card
            score = self.minimax(new_hand, dealer_hand, depth=3, is_maximizing=False)
            self.update_deck(card, remove=False)  # Restore card
            if score > best_score:
                best_score = score
                best_action = "hit"

        # Evaluate standing (evaluate current state without hitting)
        stand_score = self.evaluate_state(player_hand, dealer_hand)
        if stand_score > best_score:
            best_action = "stand"

        return best_action

    def minimax(self, player_hand, dealer_hand, depth, is_maximizing):
        """
        Minimax algorithm for evaluating the game state.
        :param player_hand: List of the player's card values.
        :param dealer_hand: List of the dealer's card values.
        :param depth: Depth of the decision tree to explore.
        :param is_maximizing: Boolean indicating if it's the maximizing player's turn.
        :return: A score representing the desirability of the state.
        """
        player_total = sum(player_hand)
        dealer_total = sum(dealer_hand)

        # Base cases
        if player_total > 21:  # Player bust
            return -1
        if dealer_total > 21:  # Dealer bust
            return 1
        if depth == 0 or dealer_total >= 17:  # Terminal conditions
            return self.evaluate_state(player_hand, dealer_hand)

        if is_maximizing:
            best_score = float("-inf")
            for card in self.get_remaining_cards():
                self.update_deck(card, remove=True)
                new_hand = player_hand + [card]
                score = self.minimax(new_hand, dealer_hand, depth - 1, False)
                best_score = max(best_score, score)
                self.update_deck(card, remove=False)
            return best_score
        else:
            best_score = float("inf")
            for card in self.get_remaining_cards():
                self.update_deck(card, remove=True)
                new_hand = dealer_hand + [card]
                score = self.minimax(player_hand, new_hand, depth - 1, True)
                best_score = min(best_score, score)
                self.update_deck(card, remove=False)
            return best_score

    def evaluate_state(self, player_hand, dealer_hand):
        """
        Evaluate the desirability of the current state.
        :param player_hand: List of the player's card values.
        :param dealer_hand: List of the dealer's card values.
        :return: A score representing the state.
        """
        player_total = sum(player_hand)
        dealer_total = sum(dealer_hand)

        if player_total > 21:  # Player bust
            return -1
        if dealer_total > 21:  # Dealer bust
            return 1
        if player_total > dealer_total:  # Player wins
            return 1
        if player_total < dealer_total:  # Dealer wins
            return -1
        return 0  # Draw

    def get_remaining_cards(self):
        """
        Get the remaining cards in the deck as a flat list.
        :return: List of remaining card values.
        """
        return [card for card, count in self.deck_count.items() if count > 0 for _ in range(count)]

    def update_deck(self, card, remove=True):
        """
        Update the deck count for a card.
        :param card: The card value to update.
        :param remove: Whether to remove or restore the card.
        """
        if remove:
            if self.deck_count[card] > 0:
                self.deck_count[card] -= 1
        else:
            self.deck_count[card] += 1

    def log_game_result(self, player_total, dealer_card, action, win_rate):
        """
        Log the result of a game to a CSV file.
        :param player_total: Total value of the player's hand.
        :param dealer_card: The dealer's visible card value.
        :param action: The action taken ("hit" or "stand").
        :param win_rate: The calculated win rate for the action.
        """
        with open("historical_data.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([player_total, dealer_card, action, win_rate])
