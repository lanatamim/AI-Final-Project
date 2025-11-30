from env.pacman_env import PacmanEnv

# Create the environment
env = PacmanEnv() # Initialize Pac-Man environment
state = env.reset()

print("Welcome to Console Pac-Man!")
print("Controls: w=up, s=down, a=left, d=right")
print("---------- GAME START ----------")

done = False

while not done:
    env.render()

    key = input("Move (w/a/s/d): ").strip().lower()

    # Map keys to actions
    if key == "w":
        action = 0  # up
    elif key == "s":
        action = 1  # down
    elif key == "a":
        action = 2 # left
    elif key == "d":
        action = 3  # right
    else:
        print("Invalid key. Use w/a/s/d.")
        continue

    # Take step
    state, reward, done, info = env.step(action)
    print(f"Reward: {reward}")

print("---------- GAME OVER ----------")
env.render()
