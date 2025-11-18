# AI-Final-Project
Person A — Environment & A*

Responsibilities (≈1/3 of workload):

Implement Pac-Man maze/grid (walls, tiles)

Implement pellets & power pellets

Implement ghosts with initial behaviors (random & aggressive)

Implement A* search for pathfinding:

Path to food/power pellet

Path away from ghosts

Provide API functions for agent to query:

Current state

Valid moves

Ghost positions

Danger zones (for RL input)

Optional: visualization of the environment for debugging

Deliverables: working environment + A* functions, accessible for agent integration

Person B — RL Agent & Decision-Making

Responsibilities (≈1/3 of workload):

Implement Q-learning (or SARSA if preferred)

Define state representation and action space:

Discretize distances to ghosts/food

Track ghost mode, quadrant, danger flags

Implement reward function (eat pellet, avoid ghost, chase frightened ghost, etc.)

Integrate A* with high-level RL decisions:

RL chooses the action → triggers corresponding A* path

Implement exploration strategy (ε-greedy, decaying ε, softmax optional)

Save/load Q-tables, run training episodes

Deliverables: trained RL agent, integration with A*, Q-table storage, agent API

Person C — Experiments, Metrics, and Reporting

Responsibilities (≈1/3 of workload):

Plan and run experiments:

Compare ε schedules (constant vs decaying)

RL + A* vs RL only

Ghost difficulty variants

Reward shaping variants

Collect data: average reward, survival time, pellets eaten, learning curves

Generate plots and tables using matplotlib or another library

Summarize results and observations for presentation and report

Help debug/validate environment & agent interactions

Optional: design presentation slides

Deliverables: experimental results, plots, report analysis, slides

Team Collaboration Notes

Weekly sync: Everyone tests their module together once per week to avoid integration issues.

Integration checkpoints:

Environment + A* working independently

RL agent hooked up to environment + paths

Experiments run smoothly and data plots generated

Documentation: Each person should comment code and document module-specific logic.

Cross-training: Everyone should understand all modules, even if they aren’t implementing them, to help with debugging and report writing.
