class AI:
    def __init__(self):
        self.card_counter = None  # Reference to the card counter

    def set_card_counter(self, card_counter):
        self.card_counter = card_counter

    def decide_action(self, player_hand, dealer_hand, remaining_decks):
        # Example: Use Minimax and card counting to decide the best action
        true_count = self.card_counter.get_true_count(remaining_decks)
        if true_count > 1 and sum(player_hand) < 17:
            return "hit"
        return "stand"
