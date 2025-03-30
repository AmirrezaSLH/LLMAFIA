class Agent:
    def __init__(self, role, name, context_manager, llm_client):
        self.role = role
        self.name = name
        self.personal_history = []
        self.is_alive = True
        self.context_manager = context_manager  # Set context_manager as an input parameter
        self.llm_client = llm_client  # Set llm_client as an input parameter
        self.llm_client.set_model('gpt-4o' if role == 'Mafia' else 'gpt-4o-mini')  # Set LLM model based on agent role
        
    
    def get_role(self):
        return self.role
    
    def get_name(self):
        return self.name

    def update_personal_history(self, event):
        self.personal_history.append(event)
        if self.role == 'Mafia':
            self.personal_history.append(f"Remember, your name is {self.name}, you are Mafia. Do not reveal your identity. You are a key player in the Mafia team.")
        elif self.role == 'Townsperson':
            self.personal_history.append(f"Remember, your name is {self.name}, you are a Townsperson. Your goal is to identify and eliminate the Mafia. You are a crucial member of the Town.")
    def get_status(self):
        return self.is_alive
    
    def set_status(self, status):
        self.is_alive = status

    def generate_prompt(self, task, output_guideline):
        """
        Generates a prompt for the agent based on game rules, game history, agent role, and specific task.
        
        Args:
            task (str): The specific task for which the prompt is being generated.
        
        Returns:
            str: The generated prompt.
        """
        if not self.context_manager:
            raise ValueError("Context manager is not set for the agent.")
        
        game_rules = self.context_manager.get_rules()
        game_history = self.context_manager.get_game_history()
        agent_role = self.get_role()
        
        prompt = (
            f"Game Rules:\n{game_rules}\n\n"
            f"Game History:\n{game_history}\n\n"
            f"Your Name: {self.name}\n\n"
            f"Your Role: {agent_role}\n\n"
            f"Personal Memory (not known to other players):\n{self.personal_history}\n\n"
            f"Task: {task}\n\n"
            f"Output Guideline: {output_guideline}\n\n"
            "Please provide your response based on the above information, ensuring you follow the task and output guideline."
        )
        
        return prompt

    def vote(self, alive_players):
        if not alive_players:
            raise ValueError("No alive players to vote for.")
        
        alive_players_list = ", ".join([player.get_name() for player in alive_players])
        voting_task_guideline = (
            f"Task: voting. Output Guideline: pick one name among alive players ({alive_players_list}). "
            "Consider the game history, your role, and any personal observations. "
            "Choose a player who you suspect might be Mafia if you are a Townsperson, "
            "or a player who poses a threat if you are Mafia. "
            "Ensure your choice aligns with your strategy and the current game dynamics."
        )
        
        voting_output_guideline = (
            "Ensure your vote is a single name, returned as one word. "
        )
        prompt = self.generate_prompt(voting_task_guideline, voting_output_guideline)

        response = self.llm_client.call_llm(prompt)
        
        voted_player_name = response.strip()
        # For simplicity, let's assume the agent always picks the first player in the list
        
        return voted_player_name
    
    def provide_discussion(self, alive_players):
        if not alive_players:
            raise ValueError("No alive players to discuss with.")
        
        alive_players_list = ", ".join([player.get_name() for player in alive_players])
        discussion_task_guideline = (
            f"Task: discussion. Output Guideline: provide a discussion point considering the game history, "
            f"your role, and any personal observations. Engage with alive players ({alive_players_list}) "
            "and ensure your discussion point aligns with your strategy and the current game dynamics."
        )
        
        discussion_output_guideline = (
            "Ensure your discussion point is clear and concise."
        )
        prompt = self.generate_prompt(discussion_task_guideline, discussion_output_guideline)

        response = self.llm_client.call_llm(prompt)
        
        discussion_message = response.strip()
        
        return discussion_message

    def provide_counter_argument(self, alive_players):
        if not alive_players:
            raise ValueError("No alive players to discuss with.")
        
        alive_players_list = ", ".join([player.get_name() for player in alive_players])
        counter_argument_task_guideline = (
            f"Task: counter argument. Output Guideline: provide a counter argument considering the game history, "
            f"your role, and any personal observations. Engage with alive players ({alive_players_list}) "
            "and ensure your counter argument aligns with your strategy and the current game dynamics."
        )
        
        counter_argument_output_guideline = (
            "Ensure your counter argument is clear, concise, and is a single statement."
        )
        
        prompt = self.generate_prompt(counter_argument_task_guideline, counter_argument_output_guideline)

        response = self.llm_client.call_llm(prompt)
        
        counter_argument_message = response.strip()
        
        return counter_argument_message

    def select_target_to_kill(self, alive_players):
        """If the agent is Mafia, select a target to kill from alive players."""
        if self.role == 'Mafia':
            # Select a target to kill, excluding self
            potential_targets = [player for player in alive_players if player.get_name() != self.name]
            if potential_targets:
                alive_players_list = ", ".join([player.get_name() for player in potential_targets])
                kill_task_guideline = (
                    f"Task: select a target to kill. Output Guideline: choose a target from the alive players ({alive_players_list}) "
                    "considering the game history, your role, and any personal observations. Ensure your choice aligns with your strategy and the current game dynamics."
                )
                
                kill_output_guideline = (
                    "Ensure your vote is a single name, returned as one word. "
                )
                
                prompt = self.generate_prompt(kill_task_guideline, kill_output_guideline)
                response = self.llm_client.call_llm(prompt)
                
                selected_target = response.strip()
                return selected_target