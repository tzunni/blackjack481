class CardCounter:
    def __init__(self):
        self.running_count = 0
        self.seen_cards = 0

    def update_count(self, card):
        # Update the running count based on the card's value
        value = card[0]  # Example: first character of the card string
        if value in '23456':
            self.running_count += 1
        elif value in 'XJQKA':  # X for 10
            self.running_count -= 1
        self.seen_cards += 1

    def get_true_count(self, remaining_cards):
        return self.running_count 
