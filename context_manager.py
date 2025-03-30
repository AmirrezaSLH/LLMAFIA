class ContextManager:
    def __init__(self):
        self.rules = self.load_rules()
        self.game_history = []

    def load_rules(self):
        """Loads and returns game rules from a file."""
        try:
            with open('context/game_rules.txt', 'r') as file:
                rules = file.read()

        except FileNotFoundError:
            rules = "Rules file not found."

        return rules

    def get_rules(self):
        """Returns the game rules."""
        return self.rules

    def update_game_history(self, update):
        """Updates the game history with new information."""
        self.game_history.append(update)

    def get_game_history(self):
        """Returns the game history."""
        return self.game_history
