import random

class Card:
    def __init__(self, suit, color, label, value):
        self.suit = suit
        self.color = color
        self.label = label
        self.value = value


class Deck:
  def __init__(self):
    self.cards = []
    self.discarded = []

  # this method simply creates a deck using the Card class above
  def create_deck(self):
      suits = ["Clover", "Spade", "Heart", "Diamond"]
      for symbol in suits:
          number = 2
          while number < 15:
              if symbol == "Clover" or symbol == "Spade":
                  suitColor = "Black"
              else:
                  suitColor = "Red"
              value = number
              if number > 10:
                  value = 10
              if number == 14:
                  value = 1
              letter = number
              if number == 11:
                  letter = "J"
              elif number == 12:
                  letter = "Q"
              elif number == 13:
                  letter = "K"
              elif number == 14:
                  letter = "A"
              newCard = Card(symbol, suitColor, letter, value)
              self.cards.append(newCard)
              number += 1


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
      if self.value == 11:
        aces += 1
      total += self.value

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
    self.cards = self.load_deck
    self.shuffle_deck
