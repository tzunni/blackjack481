# This file represents our first version of our AI, which incorporates our hi-lo card counting algorithm.


class AI:
    def __init__(self):
        self.card_counter = None  # Reference to the card counter

    def set_card_counter(self, card_counter):
        self.card_counter = card_counter

    def decide_action(self, player_hand, dealer_hand, remaining_cards):
        # Convert remaining cards to a single-deck true count
        true_count = self.card_counter.get_true_count(remaining_cards)
        player_sum = sum(card.value for card in player_hand)
        if true_count > 1 and player_sum < 17:
            return "hit"
        return "stand"
