# LLMAFIA

## Overview
LLMAFIA is a text-based simulation game where players take on the roles of either Mafia or Townsperson. The game involves strategic discussions, voting, and night actions to determine the winner.

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/llmafia.git
   ```
2. Navigate to the project directory:
   ```
   cd llmafia
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Set up your OpenAI API key:
   - Create a `.env` file in the project directory.
   - Add your OpenAI API key to the `.env` file:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```
2. Run the game:
   ```
   python game_engine.py
   ```

## Game Rules
- The game starts with a specified number of players, including a certain number of Mafia members.
- Each day consists of a night phase and a morning phase.
- During the night phase, Mafia members secretly choose a player to eliminate.
- During the morning phase, all players discuss and vote to eliminate a suspected Mafia member.
- The game continues until all Mafia members are eliminated or the number of Mafia members equals or exceeds the number of Townspeople.

## Files
- `game_engine.py`: Main game engine that runs the game loop.
- `agent.py`: Defines the Agent class representing players in the game.
- `vote_manager.py`: Manages the voting process and updates the game state based on votes.
- `context_manager.py`: Manages the game context, including game history and rules.
- `gpt_client.py`: Client for interacting with the OpenAI API.
- `api_key.py`: Utility for loading the OpenAI API key from the environment.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

