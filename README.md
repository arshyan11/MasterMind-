# MasterMind
Overview
This project implements an intelligent solver for the Mastermind game using Constraint Satisfaction Problem (CSP) principles, paired with graphical visualization via Pygame. The system operates as an autonomous codebreaker that efficiently deduces the hidden color sequence through systematic inference and constraint-based elimination.

Key Features
CSP-Driven Reasoning: The guessing agent applies CSP logic to narrow down the solution space, ensuring that each new guess remains consistent with all previous feedback.

Domain Pruning: At each stage, infeasible candidates are eliminated from the search domain based on constraint violations, improving efficiency.

Graphical User Interface: The game features an interactive interface rendered using Pygame, including pegs, feedback indicators, and interactive buttons.

Configurable Rules: The user can determine whether the hidden code permits repeated colors, thereby modifying the domain of possible solutions.

Stepwise Visualization: Each guess is drawn on-screen with corresponding feedback (correct placement and misplaced colors), making the deduction process transparent and traceable.

Replay Option: Upon completion, the interface allows the user to either restart the game or exit gracefully.

How It Works
User Input: At launch, the interface prompts the user to specify whether duplicates are allowed in the code.

Code Initialization: A hidden code is generated randomly according to the user's selected constraints.

Agent's Guessing Loop:

The agent proposes a guess from the valid domain.

Feedback is calculated: how many colors are correct and how many are correctly placed.

Using this feedback, the remaining candidate space is pruned—removing any guess that would have resulted in inconsistent feedback in prior turns.

Termination Condition: The process continues until the correct code is discovered (i.e., feedback matches complete correctness).

Restart Option: After the code is cracked, the player can choose to play another round or exit.

Underlying Concepts
CSP Representation: Each possible code is treated as a potential assignment, subject to constraints derived from feedback.

Constraint Filtering: At each turn, the agent filters the solution space by enforcing arc consistency — retaining only those candidates that satisfy all gathered constraints.

Efficiency through Pruning: Rather than brute-force enumeration, the algorithm dynamically reduces its search space, inspired by CSP-solving techniques such as forward checking.

Technical Requirements
Python 3.7 or higher

pygame library (install via pip install pygame)
