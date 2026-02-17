import random
import hashlib
import json

class SlotsGame:
    def __init__(self):
        self.holiday_items = ["party hat", "santa hat", "easter ears", "magic wand", "ancient book", "dragon ring", "crown", "christmas tree", "goat"]
        self.seed = self.generate_seed()
        self.history = []
        self.statistics = {"total_games": 0, "wins": 0, "losses": 0}

    def generate_seed(self):
        return random.randint(0, 1000000)

    def verify_seed(self, seed):
        return self.seed == seed

    def spin(self):
        if self.verify_seed(self.seed):
            result = random.choices(self.holiday_items, k=3)
            self.log_history(result)
            return result
        else:
            raise ValueError("Invalid seed")

    def log_history(self, result):
        self.history.append(result)
        self.statistics["total_games"] += 1
        if self.is_win(result):
            self.statistics["wins"] += 1
        else:
            self.statistics["losses"] += 1

    def is_win(self, result):
        return result[0] == result[1] == result[2]

    def get_statistics(self):
        return self.statistics

    def get_history(self):
        return self.history

    def hash_transaction(self):
        transaction_data = json.dumps(self.history) + str(self.seed)
        return hashlib.sha256(transaction_data.encode()).hexdigest() 

# Example usage
slots_game = SlotsGame()
print("Spin result:", slots_game.spin())
print("Game Statistics:", slots_game.get_statistics())
print("Game History:", slots_game.get_history())
print("Transaction Hash:", slots_game.hash_transaction())
