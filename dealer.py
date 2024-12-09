from deck import Deck
from card_counter import CardCounter
import json
import random

class Dealer:
    def __init__(self):
        with open('cards.txt', 'r') as file:
            self.deck = json.load(file)  # Load the deck of cards
        random.shuffle(self.deck)  # Shuffle the deck
        self.temp_deck = self.deck.copy()  # Create a temporary deck copy
        self.card_counter = CardCounter()  # Initialize the CardCounter
        self.hand = self.draw(2)  # Draw two cards to start
        self.deck_helper = Deck()  # Instance of Deck for value calculations
        while self.calculate_hand_value(self.hand) < 17:
            self.hand.append(self.draw(1)[0])  # Draw until hand is at least 17, per dealer rules

    def draw(self, n):
        if len(self.temp_deck) < n:
            print("No cards left in the deck.")
            self.handle_empty_deck()  # Handle empty deck scenario
        
        cards_drawn = []
        for _ in range(n):
            card = random.choice(self.temp_deck)
            self.temp_deck.remove(card)
            cards_drawn.append(card)
            self.card_counter.update_count(card)  # Update count here
        return cards_drawn

    def calculate_hand_value(self, hand):
        """Calculate the total value of a hand."""
        return self.deck_helper.calculate_hand_value(hand)  # Delegate to Deck class

    def handle_empty_deck(self):
        """Ask the user if they want to reset the deck or end the game."""
        while True:
            choice = input("The deck is empty. Would you like to reset the deck or end the game? (reset/end): ").strip().lower()
            if choice == "reset":
                self.reset_deck()
                print("The deck has been reset. Let's continue!")
                return
            elif choice == "end":
                print("Thank you for playing! Goodbye.")
                exit()  # Exit the program
            else:
                print("Invalid choice. Please type 'reset' or 'end'.")

    def reset_deck(self):
        """Reset the deck to its initial state."""
        self.temp_deck = self.deck.copy()
        random.shuffle(self.temp_deck)
        self.card_counter = CardCounter()  # Reset the card counter
        print("The deck has been reset.")
