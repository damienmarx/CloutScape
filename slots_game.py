import random

class SlotsGame:
    def __init__(self):
        self.slots = ["🍒", "🍋", "🍉", "🍇", "🍊", "🍀", "🍍", "🔔", "💰"]
        self.balance = 100
        self.multiplier = 1

    def spin(self):
        return [random.choice(self.slots) for _ in range(3)]

    def calculate_win(self, spin_result):
        if spin_result[0] == spin_result[1] == spin_result[2]:
            if spin_result[0] == "🍒":
                return 10 * self.multiplier
            elif spin_result[0] == "🍋":
                return 20 * self.multiplier
            elif spin_result[0] == "🍉":
                return 30 * self.multiplier
            elif spin_result[0] == "🍇":
                return 40 * self.multiplier
            elif spin_result[0] == "🍊":
                return 50 * self.multiplier
            elif spin_result[0] == "🍀":
                return 60 * self.multiplier
            elif spin_result[0] == "🍍":
                return 70 * self.multiplier
            elif spin_result[0] == "🔔":
                return 80 * self.multiplier
            elif spin_result[0] == "💰":
                return 100 * self.multiplier
        return 0

    def play(self):
        print("Welcome to the Slots Game!")
        while True:
            print(f"Current balance: {self.balance}")
            input("Press enter to spin...")
            spin_result = self.spin()
            print(f"Spin result: {' - '.join(spin_result)}")
            win = self.calculate_win(spin_result)
            if win > 0:
                print(f"You win: {win}")
                self.balance += win
            else:
                print("No win this time.")
                self.balance -= 10

            if self.balance <= 0:
                print("Game over! You've run out of balance.")
                break

            self.check_multiplier()

    def check_multiplier(self):
        if random.random() < 0.1:  # 10% chance to increase multiplier
            self.multiplier += 1
            print(f"Multiplier increased! Current multiplier: {self.multiplier}")

if __name__ == '__main__':
    game = SlotsGame()
    game.play()