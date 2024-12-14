# Blackjack Three Layer AI - 481

## Overview
This project is a Python implementation of Blackjack with an interactive interface powered by **PyGame**. Players can compete against two AI agents, each utilizing distinct strategies: **Hi-Lo card counting**, **Minimax decision-making**, and **historical data analysis**. The goal is to develop an intelligent system capable of outperforming the dealer and providing a challenging gameplay experience.

---

## Group Members

- **Keith Bui**  
  - **Games Rules Manager**: Implemented the core Blackjack rules.  
  - **Card Counting Specialist**: Developed the Hi-Lo card counting algorithm.  

- **Desire Hernandez**  
  - **Deck/Card Manager**: Managed the deck shuffling, card dealing, and handling ace values.  
  - **Alpha-Beta Pruning Specialist**: Integrated Alpha-Beta pruning for AI optimization.  

- **Justin Rodriguez**  
  - **Game Flow Coordinator**: Managed the overall game state and sequence.  
  - **AI Developer**: Designed AI decision-making logic using Minimax and card counting.  

- **Hyndavi Teegala**  
  - **User Interface Developer**: Built the user-friendly interface using PyGame.  
  - **AI Integration Lead**: Connected AI actions with the game logic and user interactions.  

---

## Goal
Our goal is to create an AI agent with a competitive edge over the dealer, leveraging:
- **Hi-Lo Card Counting**: Tracking the running and true count for strategic decisions.  
- **Alpha-Beta Pruning**: Optimizing decision-making with Minimax.  
- **Historical Data Analysis**: Learning from previous rounds to improve strategy.  

Additional objectives include:
- Extending functionality for custom decks (e.g., incomplete or stacked odds decks).  
- Stress testing with multiple players and AI agents.  
- Evaluating performance through detailed win/loss statistics.  
- Enhancing the interface for better visualization of AI decisions.  

---

## File Structure
The project is organized into the following files and folders:

### Folders
- **`Resources/`**  
  Stores card resources, including images used during gameplay.

---

### Core Files
- **`main.py`**  
  The primary entry point for running a single-player game against AI and the dealer.  

- **`2_player_main.py`**  
  Entry point for a 2-player game (human vs. AI agents).  

- **`3_player_main.py`**  
  Entry point for a 3-player game with additional AI agents.  

- **`ai.py`**  
  Implements the main AI logic, combining historical data analysis, Hi-Lo card counting, and the Minimax algorithm.

- **`ai_algorithm_1.py`**  
  Implements AI Version 1, focusing on basic Hi-Lo card counting.

- **`ai_algorithm_2.py`**  
  Implements AI Version 2, using the Minimax algorithm for decision-making.

- **`ai_algorithm_3.py`**  
  Implements AI Version 3, combining all strategies for optimal decision-making.

- **`deck.py`**  
  Handles deck creation, shuffling, and card dealing.

- **`player.py`**  
  Represents a player (human or AI), managing actions like hit/stand, hand evaluation, and score tracking.

- **`dealer.py`**  
  Represents the dealer's logic, adhering to standard Blackjack rules (e.g., hitting until 17).

---

### Supporting Files
- **`card_counter.py`**  
  Implements the Hi-Lo card counting system, tracking running and true counts.  

- **`blackjack.py`**  
  Contains centralized rules and logic specific to Blackjack.  

- **`constants.py`**  
  Stores constant values like colors, screen dimensions, and game settings.  

- **`shared.py`**  
  Provides shared classes like `Card` for use across multiple modules.

---

### Data Files
- **`ai_history.csv`**  
  Logs AI gameplay data in the format:  
  `PlayerSum, DealerVisibleCard, Decision, Outcome`  
  Used to predict optimal actions based on historical rounds.

- **`history.csv`**  
  Tracks gameplay history (e.g., win/loss outcomes).

- **`cards.txt`**  
  Stores metadata about the card deck (e.g., suits, ranks).

---

## How to Interact with the Program

### Prerequisites
1. Install Python 3.x.  
2. Install required libraries using:
   ```bash
   pip install pygame pandas


### Running the Program
Single-Player Game:
- # To play AI version 1, run:
  python3 main1.py
- # To play AI version 2, run:
  python3 main2.py
- # To play AI version 3, run:
  python3 main3.py

Multi-Player Game:
- # To play against AI version 3, run:
  python3 2_player_main.py
- # To play against AI version 3 and AI version 2, run:
  python3 3_player_main.py

