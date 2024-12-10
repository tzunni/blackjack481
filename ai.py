class AI:
    def __init__(self):
        self.card_counter = None  # Reference to the card counter

    def set_card_counter(self, card_counter):
        self.card_counter = card_counter

    def decide_action(self, player_hand, dealer_hand, remaining_cards):
        """
        Use the Minimax algorithm to decide whether to 'hit' or 'stand'.
        """
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
        if depth == 3 or not remaining_cards:
            return self.evaluate_hand(player_hand, dealer_visible_card)

        if is_player_turn:
            # Player's turn: Maximize the score
            max_value = float('-inf')
            best_action = "stand"
            player_sum = sum(card.value for card in player_hand)

            # Evaluate the 'hit' action
            if player_sum < 21:
                for card in remaining_cards:
                    new_hand = player_hand + [card]
                    new_remaining_cards = remaining_cards.copy()
                    new_remaining_cards.remove(card)

                    value = self.minimax(new_hand, dealer_visible_card, new_remaining_cards, is_player_turn=False, depth=depth + 1, alpha=alpha, beta=beta)
                    if value > max_value:
                        max_value = value
                        best_action = "hit"

                    alpha = max(alpha, value)
                    if beta <= alpha:
                        break

            # Evaluate the 'stand' action
            value = self.evaluate_hand(player_hand, dealer_visible_card)
            if value > max_value:
                max_value = value
                best_action = "stand"

            return best_action if depth == 0 else max_value

        else:
            # Dealer's turn: Minimize the player's score
            min_value = float('inf')

            for card in remaining_cards:
                new_hand = player_hand + [card]  # Add the card to the player's hand
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
        Evaluate the player's hand to estimate the score.
        """
        player_sum = sum(card.value for card in player_hand)

        # Penalize if the player's sum exceeds 21 (bust)
        if player_sum > 21:
            return -float('inf')  # Bust: Worst possible score

        # Reward higher scores closer to 21
        return player_sum
