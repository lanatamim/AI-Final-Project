# search_agent.py
import random
import numpy as np
from env.pacman_env import PacmanEnv
from env.pathfinding import a_star_path

class SearchRLAgent:
    """
    Combines Q-learning (high-level decisions) with A* planning
    (low-level movement) in the Pac-Man environment.

    High-level actions:
        0 = chase reward (go toward nearest dot)
        1 = avoid threat (run away from ghosts)
    """

    def __init__(self,
                 alpha=0.1,
                 gamma=0.95,
                 epsilon_start=1.0,
                 epsilon_min=0.05,
                 epsilon_decay=0.995):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon_start
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

        # Q-table: dict[state][action] -> value
        self.Q = {}

        # Two high-level actions: 0=chase, 1=avoid
        self.high_actions = [0, 1]

    # State representation (for Q-learning)
    def get_state(self, env: PacmanEnv):
        """
        Build a small, discrete state from the environment.

        Features:
          pacman position bucketed
          danger flag (ghost within distance <= 2)
          dots_left bucket (many / few / almost none)
        """

        px, py = env.get_pacman_position()
        ghosts = env.get_ghost_positions()

        # Danger flag: is any ghost very close?
        danger = 0
        for gx, gy in ghosts:
            dist = abs(px - gx) + abs(py - gy)
            if dist <= 2:
                danger = 1
                break

        # Dots left buckets
        dots_left = env.map.remaining_dots()
        if dots_left > 30:
            dots_bucket = 2  # many
        elif dots_left > 10:
            dots_bucket = 1  # medium
        else:
            dots_bucket = 0  # few

        # Coarse position buckets (divide into quadrants)
        w, h = env.map.width, env.map.height
        px_bucket = 0 if px < w // 2 else 1
        py_bucket = 0 if py < h // 2 else 1

        # State is a small tuple (all hashable)
        state = (px_bucket, py_bucket, danger, dots_bucket)
        return state

    def ensure_state_in_Q(self, state):
        if state not in self.Q:
            self.Q[state] = {a: 0.0 for a in self.high_actions}

    # Epsilon-greedy over high-level actions
    def choose_high_level_action(self, state):
        self.ensure_state_in_Q(state)

        if random.random() < self.epsilon:
            return random.choice(self.high_actions)
        else:
            # Argmax over actions
            q_vals = self.Q[state]
            return max(q_vals, key=q_vals.get)

    # High-level action -> low-level primitive action via A*
    def plan_with_astar(self, env: PacmanEnv, high_action):
        """
        Convert high-level choice (chase / avoid) into a primitive action
        (0=up,1=down,2=left,3=right) by using A*.
        """
        start = env.get_pacman_position()

        # Goal selection based on high-level action
        if high_action == 0:
            # Chase reward: choose nearest dot as goal
            goal = self._nearest_dot(env, start)
        else:
            # Avoid threat: choose safest tile (farthest from ghosts)
            goal = self._safest_tile(env)

        # If no valid goal, fall back to random valid primitive action
        if goal is None:
            valid_acts = env.get_valid_actions()
            return random.choice(valid_acts) if valid_acts else 0

        path = a_star_path(env.map, start, goal)

        # If A* fails or returns only the start node, choose random valid action
        if not path or len(path) < 2:
            valid_acts = env.get_valid_actions()
            return random.choice(valid_acts) if valid_acts else 0

        # Next cell on the A* path
        next_pos = path[1]
        primitive_action = self._pos_to_action(env, start, next_pos)
        if primitive_action is None:
            # fallback again in weird cases
            valid_acts = env.get_valid_actions()
            return random.choice(valid_acts) if valid_acts else 0

        return primitive_action

    def _nearest_dot(self, env: PacmanEnv, start):
        """Return coordinates of the nearest dot to 'start', or None if none."""
        sx, sy = start
        best_dist = None
        best_pos = None

        for y in range(env.map.height):
            for x in range(env.map.width):
                if env.map.grid[y][x] == 2:  # dot
                    d = abs(sx - x) + abs(sy - y)
                    if best_dist is None or d < best_dist:
                        best_dist = d
                        best_pos = (x, y)

        return best_pos

    def _safest_tile(self, env: PacmanEnv):
        """Return tile that maximizes distance to the closest ghost."""
        ghosts = env.get_ghost_positions()
        if not ghosts:
            return None

        best_score = None
        best_pos = None

        for y in range(env.map.height):
            for x in range(env.map.width):
                if env.map.is_wall(x, y):
                    continue
                # compute distance to the closest ghost
                min_d = min(abs(x - gx) + abs(y - gy) for gx, gy in ghosts)
                if best_score is None or min_d > best_score:
                    best_score = min_d
                    best_pos = (x, y)

        return best_pos

    def _pos_to_action(self, env: PacmanEnv, start, next_pos):
        """Convert step from start -> next_pos into action index 0..3."""
        sx, sy = start
        nx, ny = next_pos
        dx, dy = nx - sx, ny - sy

        for a, (adx, ady) in env.actions.items():
            if (adx, ady) == (dx, dy):
                return a
        return None

    # Q-learning update
    def update_q(self, state, action, reward, next_state, done):
        self.ensure_state_in_Q(state)
        self.ensure_state_in_Q(next_state)

        q_sa = self.Q[state][action]
        if done:
            target = reward
        else:
            max_next = max(self.Q[next_state].values())
            target = reward + self.gamma * max_next

        self.Q[state][action] = q_sa + self.alpha * (target - q_sa)

    # Training loop
    def train(self, num_episodes=200, ghost_mode="mixed"):
        """
        Train the search-based RL agent in PacmanEnv.
        Returns list of total rewards per episode (for plotting).
        """
        rewards_per_episode = []

        for ep in range(num_episodes):
            env = PacmanEnv(ghost_mode=ghost_mode)
            obs = env.reset()
            total_reward = 0
            done = False

            state = self.get_state(env)

            step_count = 0

            while not done:
                # High-level decision
                high_action = self.choose_high_level_action(state)

                # Plan via A* to get primitive action (up/down/left/right)
                primitive_action = self.plan_with_astar(env, high_action)

                # Step environment
                obs, reward, done, _ = env.step(primitive_action)
                total_reward += reward
                step_count += 1

                next_state = self.get_state(env)

                # Q-learning update on HIGH-LEVEL action
                self.update_q(state, high_action, reward, next_state, done)

                state = next_state

                # Safety stop in case of weird loops
                if step_count > 500:
                    break

            rewards_per_episode.append(total_reward)

            # Decay epsilon
            if self.epsilon > self.epsilon_min:
                self.epsilon *= self.epsilon_decay

            print(f"Episode {ep+1}/{num_episodes} - Total reward: {total_reward:.1f}, epsilon={self.epsilon:.3f}")

        return rewards_per_episode

    # Save / load Q-table
    def save(self, path="q_table.npy"):
        # Save as (keys, values) arrays
        keys = np.array(list(self.Q.keys()), dtype=object)
        vals = np.array([self.Q[k] for k in keys], dtype=object)
        np.save(path, (keys, vals), allow_pickle=True)

    def load(self, path="q_table.npy"):
        keys, vals = np.load(path, allow_pickle=True)
        self.Q = {}
        for k, v in zip(keys, vals):
            self.Q[tuple(k)] = dict(v)
