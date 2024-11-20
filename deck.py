import random


class Deck:
  def __init__(self, card_file = 'cards.txt'):
    # initialized a deck of cards from cards.txt
    self.card_file = card_file
    self.cards = self.initialize_deck()
    self.discarded = []

  def initialize_deck(self):
    # load the deck of cards from card_file

    try:
      with open(self.card_file, "r") as file:
        # returns a list of card strings from the file
        return file.read().replace("\n", "").split(",")
    except FileNotFoundError:
      # raise error if the card file cannot be found
      raise FileNotFoundError("Card file cards.txt not found.")

  def shuffle_deck(self):
    random.shuffle(self.cards)

  def deal_card(self):
    # remove & return the top card from the deck

    # raise error if the deck is empty
    if not self.cards:
      raise IndexError("The deck is empty. There are no cards to deal.")
    # returns the dealt card (top card)
    return self.cards.pop()

  def remaining_cards(self):
    # return the number of cards left in the deck
    return len(self.cards)

  def reset_deck(self):
    # reset the deck to the original state in cards.txt & (randomly) shuffle
    self.cards = self.initialize_deck
    self.shuffle_deck


deck = Deck()
deck.shuffle_deck
print(deck.deal_card())
