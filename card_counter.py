class CardCounter:
    def __init__(self):
        self.running_count = 0
        self.seen_cards = 0

    def update_count(self, card):
        # Extract the card value (first character of the card string)
        value = card[0]
        if value in '23456':
            self.running_count += 1
        elif value in 'XJQKA':
            self.running_count -= 1
        self.seen_cards += 1

    def get_true_count(self, remaining_cards):
    # Normalize the running count for a single deck
        return self.running_count / (remaining_cards / 52)

