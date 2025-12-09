AI Final Project — Pac-Man Search + Reinforcement Learning Agent
University of Akron — CPSC 460/560 (AI & Heuristic Programming)

This project implements an intelligent Pac-Man agent that combines:
    - Search-based planning (A*) for low-level movement
    - Q-learning for high-level decision-making
    - A fully custom Pac-Man environment, ghosts, scatter/chase behavior, and maze system
    - Both human-play mode and autonomous agent mode

The system demonstrates how reinforcement learning and search can work together in a game environment.

How It Works
High-Level Decisions (Q-Learning)
    The RL agent chooses between two high-level strategies:
        0 — Chase rewards: Move toward the nearest dot
        1 — Avoid threats: Move toward the safest tile (farthest from ghosts)
Low-Level Movement (A*)
After selecting a high-level strategy:
    The agent uses A* to compute the optimal next move.
    A* ensures smooth, purposeful movement.

Environment Features
    Full maze with dots, walls, corridors
    Smart ghost behavior (scatter / chase cycles)
    Collision rules
    Dot collection
    Terminal win/loss states
    Console renderer for debugging and human play

Roles and Responsibilities
Person A — Environment & A* Pathfinding (≈ 1/3 of project workload)
    Person A built the entire Pac-Man world, including:
        Environment & Maze
        Grid/maze layout, walls, dots
        Multiple maze options
        Dot tracking and win condition
    Entities
        Pac-Man mechanics
        Ghost entities
    Smart Ghosts
        Scatter and chase mode
        A* pathfinding to Pac-Man
    Random fallback behavior
    More dynamic, less predictable movement
    A* Pathfinding
        Compute shortest path to any target
        Used by both ghosts and RL agent
    API for Agent & Experiments
    Valid actions
    Pac-Man and ghost positions
    Observation grid
    Dot counts
    Wall detection
Deliverables
    Fully working environment
    Ghost intelligence
    A* path planning
    Human-play mode (play.py)

Person B — Reinforcement Learning Agent (≈ 1/3 of project workload)
    Person B implemented the intelligent agent using Q-learning combined with A*.
        High-Level RL Logic
        State representation using:
            Ghost distance buckets
            Dot counts
            Danger flag
            Maze quadrant
        Two high-level actions (chase vs. avoid)
            Q-Learning Algorithm
            Epsilon-greedy exploration
            Decaying ε
            Q-table updates
            Saving/loading Q-tables
        Integration With A***
            RL chooses a high-level strategy
            A* picks the exact tile movement
            navigation + strategy
        Training Pipeline
            Multi-episode training
            Epsilon decay scheduling
            Logging & reward tracking
    Deliverables
        Full search_agent.py implementation
        Complete RL training script (train_search_agent.py)
        Autonomous agent runner (run_agent.py)
        Working Q-table

Person C — Experiments & Analysis (≈ 1/3 of project workload)
    Person C evaluated how well the agent learned.
    Experiment Design
    Compared different epsilon decay settings:
        0.995
        0.980
        0.999
    Measured reward progression across episodes
    Tested stability of learning
    Data Collection
        Total reward per episode
        Smoothed learning curves
        Behavior changes over time
    Visualization
        Matplotlib plots for reward curves
        Comparison graph of all experiments
    Analysis & Interpretation
        Identified optimal ε-decay
        Explained exploration vs exploitation behavior
        Summarized convergence trends
    Deliverables
        experiments.py
        Reward graphs
        Learning analysis section for report

How to Run the Project

## Pac-Man Game (Reinforcement Learning + A* Search)

Human Play Mode
    Use W/A/S/D to control Pac-Man in the console:
    python play.py

Web Frontend (Autonomous RL Agent Autoplay)
    Run the web server:
        python web_app.py
    Open http://localhost:5000 — the RL+A* agent auto-plays!
    Use WASD/arrow keys to take control (or reset to resume autoplay).

Train the RL Agent from Scratch
    Runs Q-learning over 200 episodes and saves q_table_search_agent.npy:
    python train_search_agent.py

Run the Trained Agent Automatically (Console)
    Watch the learned agent play in the terminal:
    python run_agent.py

Run Pac-Man Experiments / Generate Plots
    Compare different epsilon decay schedules:
    python experiments.py

## Adversarial Games (Tic-Tac-Toe)

Run All Adversarial Experiments
    Generates 4 PNG comparison plots (takes ~5-10 min):
    python adversarial_experiments.py
    
    Plots generated:
    - experiment_epsilon_decay.png: RL learning with different ε decay rates
    - experiment_alpha_beta_efficiency.png: Minimax pruning benefits (~96% reduction)
    - experiment_minimax_vs_rl.png: RL agent win/draw/loss vs Minimax
    - experiment_learning_progression.png: RL performance over training

Train RL Tic-Tac-Toe Agent and Play in Browser
    Train the agent (500 episodes, ~2 min):
        python -c "from adversarial_games import RLTicTacToeAgent; a = RLTicTacToeAgent(); a.train_self_play(500); a.save('rl_tictactoe.npy'); print('Agent saved!')"
    
    Run the web server (port 5001):
        python adversarial_web_api.py
    
    Play in browser at http://localhost:5001/api/tictactoe/reset (or use frontend)Reinforcement Learning Agent Notes
    The agent uses Q-learning with an epsilon-greedy policy and decaying epsilon (configurable in search_agent.py).
    Ghost behavior can be configured via PacmanEnv(ghost_mode="mixed"|"chase"|"scatter") for different training curricula.
    Training saves a Q-table (q_table_search_agent.npy) that run_agent.py loads for autonomous play.

Adversarial Game Agents & Experimentation
    New Components:
        adversarial_games.py: Complete Tic-Tac-Toe framework
            - TicTacToe environment with full game logic
            - MinimaxAgent: Optimal play with optional alpha-beta pruning
            - RLTicTacToeAgent: Q-learning with self-play training
            - play_match(): Tournament framework
        
        adversarial_experiments.py: Four comprehensive experiments
            1. Epsilon-Greedy Decay Comparison (ε=0.99, 0.995, 0.999)
               → Shows how decay rate affects learning speed and stability
            2. Alpha-Beta Pruning Efficiency
               → Demonstrates 96%+ reduction in nodes evaluated
            3. RL vs Minimax (Learned Agent vs Optimal Baseline)
               → RL learns to draw against perfect player
            4. Learning Progression Over Training
               → Tracks performance improvement across 500 episodes
        
        adversarial_web_api.py: REST API for browser-based play
            - /api/tictactoe/reset: Start new game vs RL or Minimax
            - /api/tictactoe/move: Player move + AI response
            - /api/tictactoe/state: Get current board state
    
    Key Findings:
        - Alpha-beta pruning reduces minimax search from ~278K to ~9K nodes (96% improvement)
        - RL agent converges to optimal play (draw/loss only) vs Minimax within 500 episodes
        - Slower ε decay (0.999) leads to more stable learning than aggressive decay (0.99)
        - Self-play training successfully teaches Q-learning to play optimally

Conclusion
This project demonstrates how combining Reinforcement Learning (Q-learning) with A* search produces a powerful hybrid agent capable of navigating a complex game environment. Each team role contributed to a system that:
    Learns better strategies over time
    Makes informed high-level decisions
    Moves efficiently and intelligently through the maze
    Supports human interaction and automated evaluation
    A complete, working intelligent Pac-Man system.