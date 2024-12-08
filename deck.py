import random

class Deck:
  def __init__(self, card_file = 'cards.txt'):
    """
    Initialize the deck using a card file
    - card_file (str): The name of the file containing the card list (cards.txt)
    """
    self.card_file = card_file
    self.cards = self.initialize_deck()
    self.discarded = []

  def initialize_deck(self):
    """
    Initialize the deck of cards from the specified card file.
    Reads the card file & creates a deck of cards by splitting them into a list.
    If the file cannot be found, a FileNotFoundError will be raised.

    Returns: A list of card strings (e.g., ["1H", "2D", "JC"])
    """
    try:
      with open(self.card_file, "r") as file:
        # returns a list of card strings from the file
        return [card.strip() for card in file.read().split(",")]
    except FileNotFoundError:
      # raise error if the card file cannot be found
      raise FileNotFoundError("Card file cards.txt not found.")

  def shuffle_deck(self):
    """
    Shuffle the deck to randomize the order of the cards.
    This function uses Python's random.shuffle() to shuffle the deck in place.
    """
    random.shuffle(self.cards)

  def deal_card(self):
    """
    Deal a single card from the deck.
    This function pops a card from the deck list and returns it.
    If the deck is empty, a ValueError will be raised.

    Returns: The card string ("AH", "KD", "JC")
    """
    if not self.cards:
      raise IndexError("The deck is empty. There are no cards to deal.")
    # returns the dealt card (top card)
    return self.cards.pop()

  def card_values(self, card):
    """
    Get the value of a card based on its rank.

    This function extracts the rank of the card & returns the corresponding card value.
    For face cards (Jack, Queen, King), it returns 10.
    For Ace, it returns 11. For other cards, it returns the numeric value.

    - card (str): The card string (e.g., "1H", "JS", "KD")
    Returns: (int) The value of the card (10 for "JH", 11 for "AS")
    """
    rank = card[:-1]

    if rank in ['X','J', 'Q', 'K']:
      return 10
    elif rank in ['A']:
      return 11
    else:
      return int(rank)

  def calculate_hand_value(self, hand):
    """
    Calculate the total value of a hand, special handling for Aces

    - hand (list): A list of card strings in the hand (["1H", "KD", "7S"])
    Returns: (int) The total hand value
    """
    total = 0
    aces = 0

    # Calculate the total value & count Aces
    for card in hand:
      value = self.card_values(card)
      if value == 11:
        aces += 1
      total += value

    # Special handling for Aces , when the total exceeds 21
    while total > 21 and aces > 0:
      # Convert one Ace value from 11 to 1
      total -= 10
      aces -= 1

    return total

  def remaining_cards(self):
    """
    This function returns the count of the remaining cards in the deck.

    Returns: (int) The number of cards left in the deck.
    """
    return len(self.cards)

  def reset_deck(self):
    """
    Reset the deck to its original state and shuffle it.

    This function reinitializes the deck from the card file and shuffles it to restore the deck to randomized state.
    """
    self.cards = self.initialize_deck
    self.shuffle_deck
