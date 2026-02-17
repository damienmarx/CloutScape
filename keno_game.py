import random
import hashlib

class KenoGame:
    def __init__(self):
        self.drawn_numbers = []
        self.total_numbers = 80  # Keno has 80 numbers
        self.max_squares = 10
        self.bets = []  # To store player bets

    def draw_numbers(self):
        self.drawn_numbers = random.sample(range(1, self.total_numbers + 1), 20)
        return self.drawn_numbers

    def place_bet(self, numbers):
        if len(numbers) > self.max_squares:
            raise ValueError(f'You can only choose up to {self.max_squares} squares.')
        self.bets.append(numbers)

    def calculate_payout(self, bet):
        hits = len(set(bet) & set(self.drawn_numbers))
        multiplier = self.get_multiplier(len(bet))
        return hits * multiplier

    def get_multiplier(self, squares):
        return squares if squares > 0 else 1

    def is_fair(self, secret):
        # Provably fair check
        hash_input = ''.join(map(str, sorted(self.drawn_numbers))) + secret
        hash_output = hashlib.sha256(hash_input.encode()).hexdigest()
        return hash_output

    def play(self, bet_numbers, secret):
        self.draw_numbers()
        self.place_bet(bet_numbers)
        payout = self.calculate_payout(bet_numbers)
        fair_hash = self.is_fair(secret)
        return self.drawn_numbers, payout, fair_hash

# Example usage
if __name__ == '__main__':
    game = KenoGame()
    bet = [5, 13, 24, 36, 45]  # Example bet
    secret = 'my_secret_value'  # A secret value for fairness
    drawn_numbers, payout, fair_hash = game.play(bet, secret)
    print(f'Drawn Numbers: {drawn_numbers}')
    print(f'Payout: {payout}')
    print(f'Fairness Hash: {fair_hash}')