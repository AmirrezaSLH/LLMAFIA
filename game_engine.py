
from api_key import get_api_key
from gpt_client import ChatGPTClient
from context_manager import ContextManager
from agent import Agent

import random

def generate_random_names(num_names=10):
    """Generates a list of unique random names."""
    names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", "Ivy", "Jack"]
    return random.sample(names, num_names)

class GameEngine:
    def __init__(self, num_players=4, num_mafia=1, num_days=2):
        """Initializes the game engine with the specified number of players, mafia, and days."""
        self.num_players = num_players
        self.num_mafia = num_mafia
        self.num_days = num_days
        self.agents = self.create_agents()
        self.context_manager = ContextManager()
        self.context_manager.update_game_history(f"Game started with {self.num_players} players.")
        self.display_initial_roles()
        self.run_game()

    def create_agents(self):
        """Creates agents with assigned roles and names."""
        agents = []
        random_names = generate_random_names(self.num_players)
        roles = ['Mafia'] * self.num_mafia + ['Townsperson'] * (self.num_players - self.num_mafia)
        random.shuffle(roles)
        for i in range(self.num_players):
            role = roles[i]
            name = random_names[i]
            agents.append(Agent(role, name))
        return agents

    def display_initial_roles(self):
        """Displays the initial role assignment for each agent."""
        for agent in self.agents:
            print(f"{agent.get_name()} is {agent.get_role()}")

    def game_over(self):
        """Determines if the game is over and returns the result."""
        alive_mafia = sum(1 for agent in self.agents if agent.get_role() == 'Mafia' and agent.get_status())
        alive_citizens = sum(1 for agent in self.agents if agent.get_role() == 'Townsperson' and agent.get_status())
        
        if alive_mafia == 0:
            return True, "Mafia lost"
        elif alive_mafia >= alive_citizens:
            return True, "Mafia won"
        else:
            return False, ""

    def run_game(self):
        """Runs the game loop, iterating over days and checking for game over conditions."""
        for day in range(self.num_days):
            print(f"Day {day + 1} begins.")

            print("It is night and players take night actions")
            self.night_phase()

            game_over, result = self.game_over()
            if game_over:
                print(result)
                break

            print("It is morning and players take morning actions")
            self.morning_phase()
            
            print(f"Day {day + 1} ends.")
        else:
            print("Game ended after maximum days.")

    def night_phase(self):
        """Handles the night phase where agents perform their actions."""
        for agent in self.agents:
            if agent.get_status() and agent.get_role() == 'Mafia':
                self.call_agent(agent)  # Call mafia for action

    def morning_phase(self):
        """Handles the morning phase where players discuss and vote."""
        print("Morning phase begins. Players discuss and vote.")
        
        # First round: every agent gives an argument
        for agent in self.agents:
            if agent.get_status():
                print(f"{agent.get_name()} gives an argument.")
        
        # Second round: every agent gives a defense or followup or counter argument
        for agent in self.agents:
            if agent.get_status():
                print(f"{agent.get_name()} gives a defense or followup or counter argument.")
        
        # Third round: agents vote
        for agent in self.agents:
            if agent.get_status():
                print(f"{agent.get_name()} votes.")

    def call_agent(self, agent):
        """Placeholder for calling agent actions."""
        print(f"Calling agent {agent.get_name()} for action.")

    
# Create agents and print their names for testing outside of the class
game_engine = GameEngine(num_players=4, num_mafia=1, num_days=2)

#game_engine.display_initial_roles()


