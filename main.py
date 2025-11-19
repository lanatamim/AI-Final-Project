from env.pacman_env import PacmanEnv

if __name__ == "__main__":
    env = PacmanEnv()
    obs = env.reset()
    env.render()
