import matplotlib.pyplot as plt
import numpy as np
from search_agent import SearchRLAgent
from env.pacman_env import PacmanEnv

def run_experiment(num_episodes=200, epsilon_decay=0.995):
    agent = SearchRLAgent(epsilon_decay=epsilon_decay)
    rewards_over_time = []

    for ep in range(num_episodes):
        env = PacmanEnv()
        obs = env.reset()

        total_reward = 0
        done = False

        state = agent.get_state(env)

        step_count = 0

        while not done:
            # 1. Choose HIGH-LEVEL action (0=chase, 1=avoid)
            high_action = agent.choose_high_level_action(state)

            # 2. Convert high-level action into primitive (w/a/s/d movement)
            primitive_action = agent.plan_with_astar(env, high_action)

            # 3. Take the step
            obs, reward, done, _ = env.step(primitive_action)
            total_reward += reward
            step_count += 1

            next_state = agent.get_state(env)

            # 4. Update Q-table (HIGH-LEVEL decision)
            agent.update_q(state, high_action, reward, next_state, done)

            # 5. Move to next state
            state = next_state

            if step_count > 500:
                break

        # Episode complete
        rewards_over_time.append(total_reward)

        # Decay epsilon manually (same as training loop)
        if agent.epsilon > agent.epsilon_min:
            agent.epsilon *= agent.epsilon_decay

        print(f"[Experiment] Episode {ep+1}/{num_episodes} | Reward: {total_reward:.1f} | ε={agent.epsilon:.3f}")

    return rewards_over_time


def plot_results(results):
    plt.figure(figsize=(10, 6))
    for label, rewards in results.items():
        smoothed = np.convolve(rewards, np.ones(10)/10, mode='valid')
        plt.plot(smoothed, label=label)

    plt.title("RL Performance Under Different ε-Decay Rates")
    plt.xlabel("Episode")
    plt.ylabel("Smoothed Reward")
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    print("Running Pac-Man RL Experiments...")

    results = {
        "ε-decay=0.995": run_experiment(200, epsilon_decay=0.995),
        "ε-decay=0.980": run_experiment(200, epsilon_decay=0.980),
        "ε-decay=0.999": run_experiment(200, epsilon_decay=0.999),
    }

    plot_results(results)
