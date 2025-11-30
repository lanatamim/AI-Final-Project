# run_agent.py
import time
from search_agent import SearchRLAgent
from env.pacman_env import PacmanEnv

def main():
    # Create environment
    env = PacmanEnv()
    obs = env.reset()

    # Create agent and load learned Q-table
    agent = SearchRLAgent()
    try:
        agent.load("q_table_search_agent.npy")  # match filename from train_search_agent.py
        print("Loaded Q-table from q_table_search_agent.npy")
    except Exception as e:
        print("Could not load Q-table, using fresh agent:", e)

    # Turn off exploration for evaluation
    agent.epsilon = 0.0

    total_reward = 0
    done = False
    state = agent.get_state(env)

    print("----- RL AGENT PLAYING PAC-MAN -----")
    time.sleep(1)

    step_count = 0
    while not done:
        env.render()
        time.sleep(0.2)

        # Choose high-level action greedily (chase vs avoid)
        high_action = agent.choose_high_level_action(state)

        # Use A* planning to get primitive action
        primitive_action = agent.plan_with_astar(env, high_action)

        obs, reward, done, _ = env.step(primitive_action)
        total_reward += reward
        step_count += 1

        next_state = agent.get_state(env)
        state = next_state

        if step_count > 500:
            print("Stopping after 500 steps to avoid infinite loops.")
            break

    env.render()
    print("GAME OVER - Total reward:", total_reward)

if __name__ == "__main__":
    main()
