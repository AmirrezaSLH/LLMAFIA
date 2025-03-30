class Agent:
    def __init__(self, role, name, context_manager, llm_client):
        self.role = role
        self.name = name
        self.personal_history = []
        self.is_alive = True
        self.context_manager = context_manager
        self.llm_client = llm_client
        self.llm_client.set_model('gpt-4o-mini')  # Default to lightweight model

    def get_role(self):
        return self.role

    def get_name(self):
        return self.name

    def update_personal_history(self, event):
        self.personal_history.append(event)

    def get_status(self):
        return self.is_alive

    def set_status(self, status):
        self.is_alive = status

    def generate_prompt(self, task, output_guideline):
        if not self.context_manager:
            raise ValueError("Context manager is not set for the agent.")
        
        game_rules = self.context_manager.get_rules()
        game_history = self.context_manager.get_game_history()
        
        prompt = (
            f"Game Rules:\n{game_rules}\n\n"
            f"Game History:\n{game_history}\n\n"
            f"Your Name: {self.name}\n\n"
            f"Your Role: {self.role}\n\n"
            f"Personal Memory (not known to other players):\n{self.personal_history}\n\n"
            f"Task: {task}\n\n"
            f"Output Guideline: {output_guideline}\n\n"
            "Please provide your response based on the above information, ensuring you follow the task and output guideline."
        )
        
        return prompt

    def vote(self, alive_players):
        raise NotImplementedError

    def provide_discussion(self, alive_players):
        raise NotImplementedError

    def provide_counter_argument(self, alive_players):
        raise NotImplementedError


class MafiaAgent(Agent):
    def __init__(self, name, context_manager, llm_client):
        super().__init__('Mafia', name, context_manager, llm_client)
        self.llm_client.set_model('gpt-4o')  # More advanced model for Mafia
        self.update_personal_history(
            f"Remember, your name is {self.name}, you are Mafia. Do not reveal your identity. You are a key player in the Mafia team."
        )

    def vote(self, alive_players):
        return self._perform_task(
            alive_players,
            task_desc="voting",
            output_guide="Ensure your vote is a single name, returned as one word.",
            strategy="Choose a player who poses a threat to the Mafia."
        )

    def provide_discussion(self, alive_players):
        return self._perform_task(
            alive_players,
            task_desc="discussion",
            output_guide="Ensure your discussion point is clear and concise.",
            strategy="Blend in, create doubt, or subtly redirect suspicion."
        )

    def provide_counter_argument(self, alive_players):
        return self._perform_task(
            alive_players,
            task_desc="counter argument",
            output_guide="Ensure your counter argument is clear, concise, and a single statement.",
            strategy="Defend yourself or subtly shift blame."
        )

    def select_target_to_kill(self, alive_players):
        potential_targets = [p for p in alive_players if p.get_name() != self.name]
        return self._perform_task(
            potential_targets,
            task_desc="select a target to kill",
            output_guide="Ensure your vote is a single name, returned as one word.",
            strategy="Pick someone suspicious of Mafia or influential."
        )

    def _perform_task(self, alive_players, task_desc, output_guide, strategy):
        names = ", ".join([p.get_name() for p in alive_players])
        task = (
            f"Task: {task_desc}. Output Guideline: pick one name among alive players ({names}). "
            f"{strategy}"
        )
        prompt = self.generate_prompt(task, output_guide)
        response = self.llm_client.call_llm(prompt)
        return response.strip()


class TownspersonAgent(Agent):
    def __init__(self, name, context_manager, llm_client):
        super().__init__('Townsperson', name, context_manager, llm_client)
        self.llm_client.set_model('gpt-4o-mini')  # Lighter model for townsfolk
        self.update_personal_history(
            f"Remember, your name is {self.name}, you are a Townsperson. Your goal is to identify and eliminate the Mafia."
        )

    def vote(self, alive_players):
        return self._perform_task(
            alive_players,
            task_desc="voting",
            output_guide="Ensure your vote is a single name, returned as one word.",
            strategy="Choose a player you suspect might be Mafia."
        )

    def provide_discussion(self, alive_players):
        return self._perform_task(
            alive_players,
            task_desc="discussion",
            output_guide="Ensure your discussion point is clear and concise.",
            strategy="Share suspicions or ask questions to gather clues."
        )

    def provide_counter_argument(self, alive_players):
        return self._perform_task(
            alive_players,
            task_desc="counter argument",
            output_guide="Ensure your counter argument is clear, concise, and a single statement.",
            strategy="Defend your innocence or point out inconsistencies."
        )

    def _perform_task(self, alive_players, task_desc, output_guide, strategy):
        names = ", ".join([p.get_name() for p in alive_players])
        task = (
            f"Task: {task_desc}. Output Guideline: pick one name among alive players ({names}). "
            f"{strategy}"
        )
        prompt = self.generate_prompt(task, output_guide)
        response = self.llm_client.call_llm(prompt)
        return response.strip()
