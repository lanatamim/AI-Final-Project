import matplotlib.pyplot as plt
import numpy as np
from search_agent import SearchRLAgent
from env.pacman_env import PacmanEnv


def run_baseline_random(num_episodes=200):
    """Run a random policy baseline (no learning) for comparison."""
    rewards_over_time = []

    for _ in range(num_episodes):
        env = PacmanEnv()
        env.reset()
        total_reward = 0
        done = False
        step_count = 0

        while not done:
            valid = env.get_valid_actions()
            if not valid:
                break
            action = np.random.choice(valid)
            _, reward, done, _ = env.step(action)
            total_reward += reward
            step_count += 1
            if step_count > 500:
                break

        rewards_over_time.append(total_reward)

    return rewards_over_time

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


def run_experiment_with_mode(num_episodes=150, epsilon_decay=0.995, ghost_mode="mixed"):
    """Train/evaluate RL+A* under a specific ghost behavior mode."""
    agent = SearchRLAgent(epsilon_decay=epsilon_decay)
    rewards_over_time = []

    for ep in range(num_episodes):
        env = PacmanEnv(ghost_mode=ghost_mode)
        env.reset()
        total_reward = 0
        done = False
        state = agent.get_state(env)
        step_count = 0

        while not done:
            high_action = agent.choose_high_level_action(state)
            primitive_action = agent.plan_with_astar(env, high_action)
            _, reward, done, _ = env.step(primitive_action)
            total_reward += reward
            step_count += 1

            next_state = agent.get_state(env)
            agent.update_q(state, high_action, reward, next_state, done)
            state = next_state

            if step_count > 500:
                break

        rewards_over_time.append(total_reward)

        if agent.epsilon > agent.epsilon_min:
            agent.epsilon *= agent.epsilon_decay

    return rewards_over_time


def plot_results(results, outfile="experiments_rewards.png", title="RL Performance Under Different ε-Decay Rates"):
    plt.figure(figsize=(10, 6))
    for label, rewards in results.items():
        smoothed = np.convolve(rewards, np.ones(10)/10, mode='valid')
        plt.plot(smoothed, label=label)

    plt.title(title)
    plt.xlabel("Episode")
    plt.ylabel("Smoothed Reward")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outfile, dpi=150)
    print(f"Saved plot to {outfile}")


def plot_mode_comparison(mode_stats, outfile="experiments_ghost_modes.png"):
    labels = list(mode_stats.keys())
    means = [mode_stats[k]["mean"] for k in labels]
    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, means, color=["#7dd3fc", "#fb923c", "#a78bfa"])
    plt.ylabel("Average Reward (over episodes)")
    plt.title("Ghost Behavior Impact on RL+A* Performance")
    plt.grid(axis="y", alpha=0.3)
    for bar, label in zip(bars, labels):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, f"{bar.get_height():.1f}", ha="center", va="bottom")
    plt.tight_layout()
    plt.savefig(outfile, dpi=150)
    print(f"Saved plot to {outfile}")


if __name__ == "__main__":
    print("Running Pac-Man RL Experiments...")

    # Experiment 1: Different epsilon decay schedules (learning curve over time)
    results = {
        "ε-decay=0.995": run_experiment(400, epsilon_decay=0.995),
        "ε-decay=0.980": run_experiment(400, epsilon_decay=0.980),
        "ε-decay=0.999": run_experiment(400, epsilon_decay=0.999),
    }
    plot_results(results, outfile="experiments_rewards2.png", title="RL Learning Curves (ε-decay variants)")

    # Experiment 2: RL (ε=0.995) vs Random baseline
    print("\nRunning baseline random policy...")
    rl_rewards = results["ε-decay=0.995"]
    random_rewards = run_baseline_random(num_episodes=200)
    compare = {
        "RL+A* (ε=0.995)": rl_rewards,
        "Random policy": random_rewards,
    }
    plot_results(compare, outfile="experiments_rl_vs_random.png", title="RL+A* vs Random Baseline")

    # Experiment 3: Ghost behavior modes (Random vs Chase vs Mixed)
    print("\nRunning ghost-mode comparison (random/chase/mixed)...")
    modes = ["random", "chase", "mixed"]
    mode_stats = {}
    for m in modes:
        rewards = run_experiment_with_mode(num_episodes=120, epsilon_decay=0.995, ghost_mode=m)
        mode_stats[m] = {"mean": float(np.mean(rewards)), "rewards": rewards}
        print(f"  Mode {m}: mean reward {mode_stats[m]['mean']:.1f}")

    plot_mode_comparison(mode_stats, outfile="experiments_ghost_modes.png")
