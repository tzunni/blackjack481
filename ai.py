import csv
import os
import pandas as pd

class AI:
    def __init__(self, card_class, history_file='ai_history.csv'):
        self.card_class = card_class
        self.card_counter = None
        self.action_buffer = []
        self.history_file = history_file

        # Initialize the history file if it doesn't exist
        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['PlayerSum', 'DealerCard', 'Decision', 'Outcome'])  # Header row

    def set_card_counter(self, card_counter):
        """
        Set the card counter instance.
        """
        self.card_counter = card_counter

    def decide_action(self, player_hand, dealer_hand, remaining_cards):
        player_sum = sum(card.value for card in player_hand)
        dealer_visible_card = dealer_hand[0] if dealer_hand else None

        # 1. Try Historical Data
        best_action = self.predict_from_history(player_sum, dealer_visible_card.value) if dealer_visible_card else None
        if best_action:
            print(f"AI is using historical data: {best_action}")
            return best_action

        # 2. Use Hi-Lo Card Counting
        if self.card_counter:
            true_count = self.card_counter.get_true_count(len(remaining_cards))  # Pass the number of remaining cards
            best_action = self.strategy_based_on_hi_lo(player_sum, dealer_visible_card, true_count)
            if best_action:
                print(f"AI is using Hi-Lo card counting (True Count: {true_count:.2f}): {best_action}")
                return best_action

        # 3. Fallback to Minimax
        print("AI is using Minimax as a fallback.")
        return self.minimax(player_hand, dealer_visible_card, remaining_cards, is_player_turn=True)



    def predict_from_history(self, player_sum, dealer_visible_card):
        """
        Use historical data to predict the best action.
        """
        try:
            data = pd.read_csv(self.history_file)
            relevant_data = data[
                (data["PlayerSum"] == player_sum) &
                (data["DealerCard"] == dealer_visible_card)
            ]
            if not relevant_data.empty:
                # Find the most common decision with a "Win" outcome
                decision_counts = relevant_data[relevant_data["Outcome"] == "Win"]["Decision"].value_counts()
                if not decision_counts.empty:
                    return decision_counts.idxmax()  # Return the most common successful decision
        except Exception as e:
            print(f"ERROR: Could not read historical data: {e}")
        return None  # No prediction available

    def strategy_based_on_hi_lo(self, player_sum, dealer_visible_card, true_count):
        """
        Adjust strategy based on the Hi-Lo true count.
        """
        if true_count > 2:  # Favorable for the player
            return "stand" if player_sum >= 12 else "hit"
        elif true_count < -2:  # Favorable for the dealer
            return "stand" if player_sum >= 16 else "hit"
        return None  # No clear decision based on Hi-Lo

    def minimax(self, player_hand, dealer_visible_card, remaining_cards, is_player_turn, depth=0, alpha=float('-inf'), beta=float('inf')):
        """
        Minimax algorithm with Alpha-Beta Pruning.
        """
        player_sum = sum(card.value for card in player_hand)
        if player_sum > 21 or depth == 3 or not remaining_cards:
            return self.evaluate_hand(player_hand, dealer_visible_card)

        if is_player_turn:
            max_value = float('-inf')
            best_action = "stand"
            for card in remaining_cards:
                new_hand = player_hand + [card]
                new_remaining_cards = remaining_cards.copy()
                new_remaining_cards.remove(card)

                value = self.minimax(new_hand, dealer_visible_card, new_remaining_cards, is_player_turn=False, depth=depth + 1, alpha=alpha, beta=beta)
                if value > max_value:
                    max_value = value
                    best_action = "hit" if depth == 0 else best_action

                alpha = max(alpha, value)
                if beta <= alpha:
                    break

            return best_action if depth == 0 else max_value
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
        if player_sum > 21:
            return -float('inf')
        score = player_sum
        if player_sum >= 17:
            score += 10
        if player_sum < 17:
            score -= 5
        return score


    def update_outcome_in_buffer(self, outcome):
        """Update the outcome for the last logged action in the buffer."""
        for entry in self.action_buffer:
            if entry[-1] == "Pending":  # Find the last pending entry
                entry[-1] = outcome

    def flush_buffer_to_csv(self, csv_file):
        """Write all buffered actions to the CSV."""
        try:
            if not self.action_buffer:
                print("DEBUG: No actions in buffer to write.")
            else:
                print(f"DEBUG: Writing actions to {csv_file}: {self.action_buffer}")

            with open(csv_file, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(self.action_buffer)
                self.action_buffer.clear()
        except IOError as e:
            print(f"ERROR: Could not write to {csv_file}: {e}")
