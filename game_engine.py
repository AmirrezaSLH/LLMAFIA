
from api_key import get_api_key
from gpt_client import ChatGPTClient
from context_manager import ContextManager
from agent import Agent
from vote_manager import VoteManager

import random

def generate_random_names(num_names=10):
    """Generates a list of unique random names."""
    names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", "Ivy", "Jack"]
    return random.sample(names, num_names)

class GameEngine:
    def __init__(self, num_players=4, num_mafia=1, num_days=2):
        """Initializes the game engine with the specified number of players, mafia, and days."""
        if num_mafia >= num_players:
            raise ValueError("Number of mafia must be less than the number of players.")
        self.num_players = num_players
        self.num_mafia = num_mafia
        self.num_days = num_days
        self.context_manager = ContextManager()
        self.context_manager.update_game_history(f"Game started with {self.num_players} players.")
        self.llm_client = ChatGPTClient(get_api_key())
        self.agents = self.create_agents()

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
            agents.append(Agent(role, name, self.context_manager, self.llm_client))
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

    def mafia_action(self, agent):
        """Calls the Mafia agent for action if they are alive."""
        call_action_message = f"{agent.get_name()}, you are called as the {agent.get_role()} for night phase action in private. Please decide what action you take, and it is private to you."
        print(call_action_message)
        agent.update_personal_history(call_action_message)
        alive_players = [player for player in self.agents if player.get_status()]
        target = agent.select_target_to_kill(alive_players)
        if target:
            print("TEeeeeesst Test Tesssssst ")
            print(target)
            for player in self.agents:
                if player.get_name() == target:
                    player.set_status(False)
                    elimination_message = f"{target} has been killed by the Mafia."
                    print(elimination_message)
                    self.context_manager.update_game_history(elimination_message)
                    break

    def night_phase(self):
        """Handles the night phase where agents perform their actions."""
        for agent in self.agents:
            if agent.get_status() and agent.get_role() == 'Mafia':
                self.mafia_action(agent)  # Call mafia for action

    def morning_phase(self):
        """Handles the morning phase where players discuss and vote."""
        morning_start_message = "There are three rounds in the morning phase. First round: Players discuss and give arguments. Second round: Players provide defenses, followups, or counter arguments. Third round: Players vote."
        print(morning_start_message)
        self.context_manager.update_game_history(morning_start_message)
        
        first_round_message = "First round of discussion begins."
        print(first_round_message)
        self.context_manager.update_game_history(first_round_message)
        # First round: every agent gives an argument
        for agent in self.agents:
            if agent.get_status():
                argument_message = f"{agent.get_name()}: {agent.provide_discussion(self.agents)}"
                print(argument_message)
                self.context_manager.update_game_history(argument_message)


        # Announce the second round of discussion
        second_round_message = "Second round of discussion begins. Players should provide defenses, followups, or counter arguments. The next round is voting."
        print(second_round_message)
        self.context_manager.update_game_history(second_round_message)

        # Second round: every agent gives a defense or followup or counter argument
        for agent in self.agents:
            if agent.get_status():
                defense_message = f"{agent.get_name()}: {agent.provide_counter_argument(self.agents)}"
                print(defense_message)
                self.context_manager.update_game_history(defense_message)
        
        print("It is the third round. Players should now vote.")
        # Third round: agents vote
        vote_manager = VoteManager(self.agents, self.context_manager)
        vote_manager.conduct_vote()

    def run_game(self):
        """Runs the game loop, iterating over days and checking for game over conditions."""
        for day in range(self.num_days):
            day_start_message = f"Day {day + 1} begins."
            print(day_start_message)
            self.context_manager.update_game_history(day_start_message)

            night_phase_message = "It is night and players take night actions"
            print(night_phase_message)
            self.context_manager.update_game_history(night_phase_message)
            self.night_phase()

            game_over, result = self.game_over()
            if game_over:
                game_over_message = result
                print(game_over_message)
                self.context_manager.update_game_history(game_over_message)
                break

            morning_phase_message = "It is morning and players take morning actions"
            print(morning_phase_message)
            self.context_manager.update_game_history(morning_phase_message)
            self.morning_phase()
            
            day_end_message = f"Day {day + 1} ends."
            print(day_end_message)
            self.context_manager.update_game_history(day_end_message)
        else:
            max_days_message = "Game ended after maximum days."
            print(max_days_message)
            self.context_manager.update_game_history(max_days_message)

    

    
# Create agents and print their names for testing outside of the class
game_engine = GameEngine(num_players=5, num_mafia=1, num_days=3)

#game_engine.display_initial_roles()


