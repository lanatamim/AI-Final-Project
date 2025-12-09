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
Human Play Mode
    Use W/A/S/D to control Pac-Man:
    python play.py
Web Frontend (play in browser)
    Install Flask (once):
        pip install flask
    Run the web server:
        python web_app.py
    Open http://localhost:5000 and use WASD/arrow keys to move Pac-Man.
Train the RL Agent
    Runs Q-learning over many episodes:
    python train_search_agent.py
Run the Trained Agent Automatically
    Watch the RL+A* agent play by itself:
    python run_agent.py
Run Experiments / Generate Plots
Compare multiple training schedules:
    python experiments.py

Reinforcement Learning Agent Notes
    The agent uses Q-learning with an epsilon-greedy policy and decaying epsilon (configurable in search_agent.py).
    Ghost behavior can be configured via PacmanEnv(ghost_mode="mixed"|"chase"|"scatter") for different training curricula.
    Training saves a Q-table (q_table_search_agent.npy) that run_agent.py loads for autonomous play.

Conclusion
This project demonstrates how combining Reinforcement Learning (Q-learning) with A* search produces a powerful hybrid agent capable of navigating a complex game environment. Each team role contributed to a system that:
    Learns better strategies over time
    Makes informed high-level decisions
    Moves efficiently and intelligently through the maze
    Supports human interaction and automated evaluation
    A complete, working intelligent Pac-Man system.