import csv
import os
from shared import Card
import pandas as pd

class AI:
    def __init__(self, card_class, history_file='ai_history.csv'):
        self.card_class = card_class
        self.card_counter = None
        self.history_file = history_file

        # Initialize the history file if it doesn't exist
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["PlayerSum", "DealerVisibleCard", "Decision", "Outcome"])  # Header row

    def set_card_counter(self, card_counter):
        """
        Set the card counter instance.
        """
        self.card_counter = card_counter

    def decide_action(self, player_hand, dealer_hand, remaining_cards):
        """
        Use historical data and the Minimax algorithm to decide whether to 'hit' or 'stand'.
        """
        player_sum = sum(card.value for card in player_hand)
        dealer_visible_card = dealer_hand[0] if dealer_hand and isinstance(dealer_hand[0], self.card_class) else None

        if not dealer_visible_card:
            print("ERROR: Dealer visible card is missing or invalid.")
            return "stand"  # Default to 'stand' if dealer card is invalid

        # Predict the best action based on historical data
        best_action = self.predict_from_history(player_sum, dealer_visible_card.value)

        # If no historical data is available, fall back to the Minimax algorithm
        if not best_action:
            best_action = self.minimax(player_hand, dealer_visible_card, remaining_cards, is_player_turn=True)

        # Log the decision
        self.log_to_csv(player_sum, dealer_visible_card.value, best_action, "Pending")  # Outcome will be updated later

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


    def log_to_csv(self, player_sum, dealer_visible_card, decision, outcome):
        """
        Log the player's sum, dealer's visible card, decision, and outcome to a CSV file.
        """
        with open(self.history_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([player_sum, dealer_visible_card, decision, outcome])


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

    def update_outcome_in_csv(self, player_sum, dealer_visible_card, decision, outcome, history_file="ai_history.csv"):
            """
            Updates the outcome of the most recent Pending record in the CSV.
            """
            try:
                # Ensure the file exists before reading
                if not os.path.exists(history_file):
                    print(f"ERROR: History file '{history_file}' does not exist.")
                    return

                # Load the historical data
                data = pd.read_csv(history_file)

                # Ensure necessary columns are in the data
                if not {"PlayerSum", "DealerVisibleCard", "Decision", "Outcome"}.issubset(data.columns):
                    raise ValueError("Missing required columns in historical data.")

                # Find the most recent row with a matching Pending entry
                pending_rows = data[(data["PlayerSum"] == player_sum) &
                                    (data["DealerVisibleCard"] == dealer_visible_card) &
                                    (data["Decision"] == decision) &
                                    (data["Outcome"] == "Pending")]

                if not pending_rows.empty:
                    index_to_update = pending_rows.index[0]
                    data.at[index_to_update, "Outcome"] = outcome
                    print(f"Updated outcome to {outcome} for PlayerSum {player_sum}, DealerVisibleCard {dealer_visible_card}, Decision {decision}")
                else:
                    print(f"No matching 'Pending' row found for PlayerSum {player_sum}, DealerVisibleCard {dealer_visible_card}, Decision {decision}")

                # Write updated data back to the CSV
                data.to_csv(history_file, index=False)

            except Exception as e:
                print(f"ERROR: Could not update outcome in CSV: {e}")