# Blackjack - 481
This is our group's implementation of Blackjack with a dealer and an AI that counts cards, written in **Python** using **PyGame**.

## Group Members:
- ### Keith Bui
  - **Games Rules Manager** (Implement the core Blackjack rules)
  - **Card Counting Specialist** (Implement the Hi-Lo card counting algorithm and maintain a running count)
- ### Desire Hernandez
  - **Deck/Card Manager** (Handle deck shuffling, card dealing, and tracking the remaining cards in the deck & special handling for ace values)
  - **Alpha-Beta Pruning Specialist** (Integrate Alpha-Beta pruning to optimize AI decision-making and improve performance)
- ### Justin Rodriguez
  - **Game Flow Coordinator** (Manage the overall game state and ensure proper sequence)
  - **AI Developer** (Develop the AI agent’s decision-making logic using Minimax/Integrate AI actions with the card counting system)
- ### Hyndavi Teegala
  - **User Interface Developer** (Create the frontend interface using PyGame, including the buttons, game status displays, interaction panels and maybe add real time updates with count display)
  - **AI Integration Lead** (Ensure communication between the AI agent and the game logic, connecting the UI actions to the AI’s responses)

# Goal:
- Our goal is to create an AI agent that has a competitive advantage over the dealer using card counting. This will be implemented using a form of the Alpha Beta Minimax algorithm.
- If we can manage it, we will try to...
  - extend the algorithm to work on custom decks, such as incomplete decks, and stacked odds decks
  - create multiple players/agents in order to stress test our algorithm
  - ... **TBA**