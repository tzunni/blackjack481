import csv
from deck import Deck


class AI:
    def __init__(self, data_file, hand_value_calculator):
        self.card_counter = None
        self.data = self.load_data(data_file)
        self.calculate_hand_value = hand_value_calculator
        self.deck = Deck()

    def set_card_counter(self, card_counter):
        self.card_counter = card_counter

    def load_data(self, file_path):
        data = []
        try:
            with open(file_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append({
                        "player_total": int(row["player_total"]),
                        "dealer_card": int(row["dealer_card"]),
                        "action": row["action"],
                        "win_rate": float(row["win_rate"])
                    })
        except FileNotFoundError:
            print(f"File {file_path} not found.")
        return data

    def minimax(self, player_hand, dealer_hand, remaining_decks, depth, is_maximizing):
        player_total = self.calculate_hand_value(player_hand)
        dealer_total = self.calculate_hand_value(dealer_hand)

        if player_total > 21:
            return -1
        elif dealer_total > 21:
            return 1
        elif depth == 0 or player_total >= 21 or dealer_total >= 17:
            if player_total > dealer_total:
                return 1
            elif player_total < dealer_total:
                return -1
            else:
                return 0

        if is_maximizing:
            best_score = float("-inf")
            for card in self.deck.remaining_cards(remaining_decks):
                new_hand = player_hand + [card]
                score = self.minimax(new_hand, dealer_hand, remaining_decks - 1, depth - 1, False)
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = float("inf")
            for card in self.deck.remaining_cards(remaining_decks):
                new_hand = dealer_hand + [card]
                score = self.minimax(player_hand, new_hand, remaining_decks - 1, depth - 1, True)
                best_score = min(best_score, score)
            return best_score

    def decide_action(self, player_hand, dealer_hand, remaining_decks):
        best_action = "stand"
        best_score = float("-inf")

        for card in self.deck.remaining_cards(remaining_decks):
            new_hand = player_hand + [card]
            score = self.minimax(new_hand, dealer_hand, remaining_decks - 1, depth=3, is_maximizing=False)
            if score > best_score:
                best_score = score
                best_action = "hit"

        return best_action

    def log_game_result(self, player_total, dealer_card, action, win_rate):
        with open("historical_data.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([player_total, dealer_card, action, win_rate])
