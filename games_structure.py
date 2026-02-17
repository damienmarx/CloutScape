# Base Game Class and Game Manager

class BaseGame:
    def __init__(self, name):
        self.name = name
        self.is_running = False

    def start_game(self):
        self.is_running = True
        print(f"{self.name} has started.")

    def end_game(self):
        self.is_running = False
        print(f"{self.name} has ended.")


class GameManager:
    def __init__(self):
        self.games = {}

    def add_game(self, game):
        self.games[game.name] = game

    def start_game(self, game_name):
        if game_name in self.games:
            self.games[game_name].start_game()
        else:
            print(f"Game {game_name} not found.")

    def end_game(self, game_name):
        if game_name in self.games:
            self.games[game_name].end_game()
        else:
            print(f"Game {game_name} not found.")

# Specific Games
class Keno(BaseGame):
    def __init__(self):
        super().__init__("Keno")

class Slots(BaseGame):
    def __init__(self):
        super().__init__("Slots")

class Crash(BaseGame):
    def __init__(self):
        super().__init__("Crash")


# Example usage
if __name__ == '__main__':
    manager = GameManager()
    keno = Keno()
    slots = Slots()
    crash = Crash()
    manager.add_game(keno)
    manager.add_game(slots)
    manager.add_game(crash)

    manager.start_game("Keno")
    manager.start_game("Slots")
    manager.end_game("Keno")
    manager.end_game("Slots")
    manager.start_game("Crash")  
    
