import random

class Card:
    def __init__(self, suit, color, label, value):
        self.suit = suit
        self.color = color
        self.label = label
        self.value = value


class Deck:
    def __init__(self, card_file='cards.txt'):
        """
        Initialize the deck using a card file.
        - card_file (str): The name of the file containing the card list (default: 'cards.txt').
        """
        self.card_file = card_file
        self.cards = self.initialize_deck()
        self.discarded = []
        
    def sanitize_card(card):
        """
        Sanitize a card string by removing extraneous characters.
        Args:
            card (str): The card string (e.g., '["AH"', '"XH"').
        Returns:
            str: The sanitized card string (e.g., 'AH', 'XH').
        """
        return card.strip('[]"')

    def initialize_deck(self):
        """
        Initialize the deck of cards from the specified card file.
        Reads the card file & creates a deck of cards by splitting them into a list.
        If the file cannot be found, a FileNotFoundError will be raised.

        Returns: A list of card strings (e.g., ["1H", "2D", "JC"]).
        """
        try:
            with open(self.card_file, "r") as file:
                # Ensure no extraneous characters are included in the cards
                return [card.strip() for card in file.read().split(",")]
        except FileNotFoundError:
            raise FileNotFoundError("Card file 'cards.txt' not found.")


    def shuffle_deck(self):
        """
        Shuffle the deck to randomize the order of the cards.
        This function uses Python's random.shuffle() to shuffle the deck in place.
        """
        random.shuffle(self.cards)
        print("Deck shuffled.")

    def deal_card(self):
      """Deal a single sanitized card from the deck."""
      if not self.cards:
          raise IndexError("The deck is empty. There are no cards to deal.")
      card = self.cards.pop()
      return sanitize_card(card)  # Or Deck.sanitize_card(card) if inside Deck


    def card_values(self, card):
        """
        Get the value of a card based on its rank.

        - card (str): The card string (e.g., "1H", "JS", "KD").
        Returns: (int) The value of the card (10 for face cards, 11 for Ace).
        """
        rank = card[:-1]

        if rank in ['X', 'J', 'Q', 'K']:
            return 10
        elif rank == 'A':
            return 11
        else:
            return int(rank)

    def calculate_hand_value(self, hand):
        """
        Calculate the total value of a hand, with special handling for Aces.

        - hand (list): A list of card strings in the hand (e.g., ["1H", "KD", "7S"]).
        Returns: (int) The total hand value.
        """
        total = 0
        aces = 0

        for card in hand:
            value = self.card_values(card)
            if value == 11:
                aces += 1
            total += value

        # Adjust for Aces if total exceeds 21
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    def remaining_cards(self, remaining_decks=1):
        """
        Return cards available based on the number of remaining decks.

        - remaining_decks (int): Number of decks to simulate.
        Returns: A list of cards for the remaining decks.
        """
        return self.initialize_deck() * remaining_decks

    def reset_deck(self):
        """
        Reset the deck to its original state and shuffle it.

        This function reinitializes the deck from the card file and shuffles it to restore the deck to a randomized state.
        """
        self.cards = self.initialize_deck()  # Ensure parentheses for method call
        self.shuffle_deck()
        print("Deck reset and shuffled.")
