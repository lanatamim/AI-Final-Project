# train_search_agent.py
from search_agent import SearchRLAgent
import matplotlib.pyplot as plt

agent = SearchRLAgent()
rewards = agent.train(num_episodes=200, ghost_mode="mixed")

# Plot learning curve
plt.plot(rewards)
plt.xlabel("Episode")
plt.ylabel("Total Reward")
plt.title("Search-based Q-learning Pac-Man")
plt.show()

# Optionally save Q-table
agent.save("q_table_search_agent.npy")
