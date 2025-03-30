class ContextManager:
    def __init__(self):
        self.rules = self.load_rules()
        self.game_history = []
        self.player_roles = {}  # Initialize a dictionary to store player roles

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

    def set_player_role(self, player_name, role):
        """Sets the role for a given player."""
        self.player_roles[player_name] = role

    def get_player_role(self, player_name):
        """Returns the role of a given player."""
        return self.player_roles.get(player_name, "Role not found.")

    def get_final_game_log(self):
        """Returns the final game log starting with roles and appending game history."""
        final_log = ["Game Roles:"]
        for player, role in self.player_roles.items():
            final_log.append(f"{player}: {role}")
        final_log.append("Game History:")
        final_log.extend(self.game_history)
        return "\n \n".join(final_log)
