from shared import Card


class AI:
    def __init__(self, card_class):
        self.card_class = card_class
        self.card_counter = None

    def set_card_counter(self, card_counter):
        """
        Set the card counter instance.
        """
        self.card_counter = card_counter

    def decide_action(self, player_hand, dealer_hand, remaining_cards):
        """
        Use the Minimax algorithm to decide whether to 'hit' or 'stand'.
        """
        print(f"DEBUG: Remaining cards at start of decision: {[f'{card.label} of {card.suit}' for card in remaining_cards]}")  # Debug print
        player_sum = sum(card.value for card in player_hand)
        dealer_visible_card = dealer_hand[0]  # Dealer's visible card

        # If the player's current sum is already 21 or above, stand
        if player_sum >= 21:
            return "stand"

        # Perform the Minimax search to determine the best action
        best_action = self.minimax(player_hand, dealer_visible_card, remaining_cards, is_player_turn=True)
        return best_action


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
