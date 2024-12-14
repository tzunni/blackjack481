# Blackjack - 481

# Overview:
  This project is a Python implementation of Blackjack with an interactive interface powered by pygame. Players can compete against two AI agents, each utilizing distinct strategies like Hi-Lo card counting, Minimax decision-making, and historical data analysis.
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

## Goal:
- Our goal is to create an AI agent that has a competitive advantage over the dealer using card counting. This will be implemented using a form of the Alpha-Beta Minimax algorithm.
- If we can manage it, we will try to:
  - Extend the algorithm to work on custom decks, such as incomplete decks and stacked odds decks.
  - Create multiple players/agents to stress test our algorithm's performance and robustness.
  - Integrate historical gameplay data to improve decision-making through learning patterns and outcomes.
  - Add a user-friendly interface that enables players to easily visualize AI decision-making and its reasoning (e.g., highlighting moves based on card counting or Minimax evaluations).
  - Evaluate the AI's performance using win/loss statistics against other AI versions, the dealer, and human players.


# File Structure:
  The project is organized into the following files and folders:

  - # Folders

    Assets/:
    Contains additional assets for the game such as UI elements, card images, or icons.

    Resources/:
    Stores card resources used during the gameplay.
    Includes subdirectories for card images, which are rendered during the game.

  - # Core Logic
    main.py:
    The primary entry point for running the game.
    Manages the game loop, user interaction, and integration with AI agents.
    Launches a single-player Blackjack game against two AI agents and the dealer.
    
    multi_main.py:
    An alternative entry point designed for multiplayer modes.
    Enables more players (or additional AI agents) to compete simultaneously.
    
    multiplayer_main.py:
    Handles multiplayer-specific logic and UI rendering.
    
    constants.py:
    Stores constant values such as colors, screen dimensions, or game settings for easier customization.
    Game Components
    
    deck.py:
    Implements the logic for creating, shuffling, and dealing a standard 52-card deck.
    Uses the Card class from shared.py.
    
    player.py:
    Defines the Player class to represent human and AI players.
    Manages player actions (hit, stand), hand evaluation, and score tracking.
    
    dealer.py:
    Represents the dealer's actions, hand management, and turn logic.
    Implements rules like forced hitting until the dealer's count is at least 17.
    AI Logic
    
    ai.py:
    The main AI implementation.
    Combines three decision-making strategies:
    Historical Data Analysis: Predicts optimal actions based on prior rounds.
    Hi-Lo Card Counting: Adjusts decisions based on the running and true count.
    Minimax Algorithm: Simulates potential outcomes to choose the best action.
    
    ai_algorithm_1.py:
    Implements the logic for AI Version 1.
    Focuses on basic Hi-Lo card counting as the primary decision-making strategy.
    
    ai_algorithm_2.py:
    Implements the logic for AI Version 2.
    Uses the Minimax algorithm to simulate outcomes and improve decision-making.
    
  - # Supporting Files
    card_counter.py:
    Implements the Hi-Lo card counting system.
    Tracks the running count of cards and calculates the true count for the AI.
    
    blackjack.py:
    Handles Blackjack-specific rules and logic (e.g., busts, Blackjacks).
    Centralized for game rules that interact with the Player, Dealer, and AI classes.
    
    shared.py:
    Defines shared classes and utilities like Card for use across multiple modules.
  - # Data Files
    ai_history.csv:
    Stores historical gameplay data in the format:
    PlayerSum,DealerVisibleCard,Decision,Outcome
    Used by the AI to predict optimal decisions based on previous rounds.
   
    history.csv:
    Another file for tracking gameplay history (specific use case may vary).
    
    cards.txt:
    Likely contains metadata or card information (e.g., suit, rank, values).

- # How to Interact with the Program

  - # Prerequisites
    Install Python 3+.
    Install required libraries using:
    pip install pygame pandas

  - # Running the Program
    Single-Player Game: Run the main.py file to start a game against the AI:
    python main.py
    Use H to "Hit" or S to "Stand" during your turn.

    Multiplayer Game: Run the multi_main.py file for multiplayer functionality:
    python multi_main.py
    
    Alternative Multiplayer Logic: 
    Use multiplayer_main.py for an enhanced multiplayer experience.

  - # Gameplay Instructions
    Objective: Beat the dealer by getting a hand value closer to 21 than theirs without going over.

    Players:
    Human Player: Controlled using keyboard inputs.
    
    AI Players:
    AI Version 1: Relies on Hi-Lo card counting.
    AI Version 2: Uses Minimax decision-making.
    Dealer: Plays according to Blackjack rules (e.g., hits until reaching at least 17).
    
    End of Round:
    The program evaluates each player's score and displays the results.

- # Code Layout
  Classes
  Card (in shared.py): Represents a playing card with attributes like suit, value, and label.

  Deck (in deck.py): Manages the deck, including shuffling and dealing cards.

  Player (in player.py): Represents a human or AI player. Handles gameplay actions and score tracking.

  Dealer (in dealer.py): Represents the dealer's logic and adheres to standard Blackjack rules.

  AI (in ai.py): Implements decision-making strategies using historical data, card counting, and Minimax.

  CardCounter (in card_counter.py): Tracks card counts using the Hi-Lo system.

