import csv
import os
import pandas as pd

class AI:
    def __init__(self, card_class, history_file='ai_history.csv'):
        self.card_class = card_class
        self.card_counter = None
        self.action_buffer = []  # Correctly name the buffer here
        self.history_file = history_file

        # Initialize the history file if it doesn't exist
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['PlayerSum', 'DealerVisibleCard', 'Decision', 'Outcome'])  # Header row

    def set_card_counter(self, card_counter):
        """
        Set the card counter instance.
        """
        self.card_counter = card_counter

    def decide_action(self, player_hand, dealer_hand, remaining_cards):
        """
        Decide whether to 'hit' or 'stand' using historical data or Minimax algorithm.
        """
        player_sum = sum(card.value for card in player_hand)
        dealer_visible_card = dealer_hand[0] if dealer_hand and isinstance(dealer_hand[0], self.card_class) else None

        if not dealer_visible_card:
            print("ERROR: Dealer visible card is missing or invalid.")
            return "stand"  # Default to 'stand' if dealer card is invalid

        # Predict the best action based on historical data
        best_action = self.predict_from_history(player_sum, dealer_visible_card.value)

        # If no historical data is available, fall back to Minimax
        if not best_action:
            best_action = self.minimax(player_hand, dealer_visible_card, remaining_cards, is_player_turn=True)

        # Add the action to the buffer with a "Pending" outcome
        self.action_buffer.append([player_sum, dealer_visible_card.value, best_action, "Pending"])  # Use action_buffer here

        return best_action




    def predict_from_history(self, player_sum, dealer_visible_card):
        """
        Use historical data from the CSV to predict the best action.
        """
        try:
            data = pd.read_csv(self.history_file)
            relevant_data = data[
                (data["PlayerSum"] == player_sum) &
                (data["DealerVisibleCard"] == dealer_visible_card)
            ]

            if not relevant_data.empty:
                # Find the most common decision with a "Win" outcome
                decision_counts = relevant_data[relevant_data["Outcome"] == "Win"]["Decision"].value_counts()
                if not decision_counts.empty:
                    return decision_counts.idxmax()  # Return the most common successful decision

        except Exception as e:
            print(f"ERROR: Could not read historical data: {e}")

        return None  # No prediction available

    def minimax(self, player_hand, dealer_visible_card, remaining_cards, is_player_turn, depth=0, alpha=float('-inf'), beta=float('inf')):
        """
        Minimax algorithm with Alpha-Beta Pruning.
        """
        player_sum = sum(card.value for card in player_hand)

        # Terminate if the player busts, stands, or reaches the maximum depth
        if player_sum > 21 or depth == 3 or not remaining_cards:
            return self.evaluate_hand(player_hand, dealer_visible_card)

        # Player's turn: Maximize the score
        if is_player_turn:
            max_value = float('-inf')
            best_action = "stand"

            for card in remaining_cards:
                new_hand = player_hand + [card]
                new_remaining_cards = remaining_cards.copy()
                new_remaining_cards.remove(card)

                # If the current hand is already good enough to stand, prioritize standing
                if player_sum >= 17:
                    max_value = self.evaluate_hand(player_hand, dealer_visible_card)
                    best_action = "stand"
                    break

                value = self.minimax(new_hand, dealer_visible_card, new_remaining_cards, is_player_turn=False, depth=depth + 1, alpha=alpha, beta=beta)

                if value > max_value:
                    max_value = value
                    best_action = "hit" if depth == 0 else best_action

                alpha = max(alpha, value)
                if beta <= alpha:
                    break

            return best_action if depth == 0 else max_value

        # Dealer's turn: Minimize the player's score
        else:
            min_value = float('inf')

            for card in remaining_cards:
                new_hand = [dealer_visible_card] + [card]
                new_remaining_cards = remaining_cards.copy()
                new_remaining_cards.remove(card)

                value = self.minimax(player_hand, dealer_visible_card, new_remaining_cards, is_player_turn=True, depth=depth + 1, alpha=alpha, beta=beta)
                min_value = min(min_value, value)

                beta = min(beta, value)
                if beta <= alpha:
                    break

            return min_value

    def evaluate_hand(self, player_hand, dealer_visible_card):
        """
        Evaluate the current hand's score.
        """
        player_sum = sum(card.value for card in player_hand)

        # Penalize busting
        if player_sum > 21:
            return -float('inf')  # Bust: Worst possible score

        # Reward standing when the score is close to 21
        score = player_sum
        if player_sum >= 17:
            score += 10  # Reward standing for a safe score

        # Penalize lower scores to encourage hitting
        if player_sum < 17:
            score -= 5

        # Consider the dealer's visible card
        if isinstance(dealer_visible_card, self.card_class):
            if dealer_visible_card.value >= 7 and player_sum < 17:
                score -= 5  # Strong dealer card penalizes weak hands

        return score

    def update_outcome_in_buffer(self, outcome):
        """Update the outcome for the last logged action in the buffer."""
        for entry in self.action_buffer:  # Updated to use action_buffer
            if entry[-1] == "Pending":  # Find the last pending entry
                entry[-1] = outcome

    def flush_buffer_to_csv(self, csv_file):
        """Write all buffered actions to the CSV."""
        try:
            if not self.action_buffer:
                print("DEBUG: No actions in buffer to write.")  # Debug statement
            else:
                print(f"DEBUG: Writing actions to {csv_file}: {self.action_buffer}")  # Debug statement

            with open(csv_file, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(self.action_buffer)  # Write from action_buffer
                self.action_buffer.clear()  # Clear the buffer after writing
        except IOError as e:
            print(f"ERROR: Could not write to {csv_file}: {e}")
