
from api_key import get_api_key
from gpt_client import ChatGPTClient
from context_manager import ContextManager
from agent import Agent

import random

def generate_random_names(num_names=10):
    names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", "Ivy", "Jack"]
    return random.sample(names, num_names)

random_names = generate_random_names()
print(random_names)


class init_GAME:
    def __init__(self, num_players=6, num_mafia=2, num_nights=3):
        self.num_players = num_players
        self.num_mafia = num_mafia
        self.num_nights = num_nights
        self.agents = self.create_agents()
        self.context_manager = ContextManager()
        self.context_manager.update_game_history(f"Game started with {self.num_players} players.")
    
    def create_agents(self):
        agents = []
        random_names = generate_random_names(self.num_players)
        for i in range(self.num_players):
            role = 'Mafia' if i < self.num_mafia else 'Townsperson'
            name = random_names[i]
            agents.append(Agent(role, name))
        return agents
    
    def role_assignment(self):
        return
    
    
GAME_OVER = False
nihgt_counter = 0

Print("GitHub Test")
Print("GitHub Test2")
while GAME_OVER != True:
    nihgt_counter += 1
    print(nihgt_counter)
    if nihgt_counter == 10:
        GAME_OVER = True


def main():
    # Get API key from file
    api_key = read_api_key()
    if not api_key:
        return
    
    # Start the game
    game = Game(num_players=6, api_key=api_key)
    game.start_game()

if __name__ == "__main__":
    main()
