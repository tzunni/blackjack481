class Card:

    # this class contains all attributes of a playing card
    def __init__(self, suit, color, label, value):
        self.suit = suit
        self.color = color
        self.label = label
        self.value = value

    def get_hi_lo_value(self):
            if self.label in ['2', '3', '4', '5', '6']:
                return 1
            elif self.label in ['7', '8', '9']:
                return 0
            elif self.label in ['10', 'J', 'Q', 'K', 'A']:
                return -1
            return 0