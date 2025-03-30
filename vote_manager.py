class VoteManager:
    def __init__(self, agents, context_manager):
        self.agents = agents
        self.context_manager = context_manager

    def conduct_vote(self):
        """Conducts the voting process among the agents."""
        votes, vote_messages = self.collect_votes()
        self.update_vote_history(vote_messages)
        self.process_vote_results(votes)

    def collect_votes(self):
        """Collects votes from all alive agents."""
        votes = {}
        vote_messages = []
        alive_players = [player for player in self.agents if player.get_status()]
        for agent in alive_players:
            voted_player_name = agent.vote(alive_players)
            vote_message = f"{agent.get_name()} votes for {voted_player_name}."
            print(vote_message)
            vote_messages.append(vote_message)
            if voted_player_name in votes:
                votes[voted_player_name] += 1
            else:
                votes[voted_player_name] = 1
        return votes, vote_messages

    def update_vote_history(self, vote_messages):
        """Updates the game history with the voting messages."""
        for message in vote_messages:
            self.context_manager.update_game_history(message)

    def process_vote_results(self, votes):
        """Processes the results of the vote and updates the game state."""
        if votes:
            max_votes = max(votes.values())
            players_with_max_votes = [player for player, count in votes.items() if count == max_votes]
            
            if len(players_with_max_votes) == 1:
                self.eliminate_player(players_with_max_votes[0])
            else:
                self.handle_no_majority()

    def eliminate_player(self, voted_out_player):
        """Eliminates the player who received the majority of votes."""
        alive_players = [player for player in self.agents if player.get_status()]
        for player in alive_players:
            if player.get_name() == voted_out_player:
                player.set_status(False)
                voted_out_message = f"{voted_out_player} has been voted out."
                print(voted_out_message)
                self.context_manager.update_game_history(voted_out_message)
                break

    def handle_no_majority(self):
        """Handles the scenario where no player received a majority of votes."""
        no_majority_message = "No player received a majority of votes."
        print(no_majority_message)
        self.context_manager.update_game_history(no_majority_message)

