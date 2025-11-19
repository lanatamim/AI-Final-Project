import numpy as np
import random
from .game_map import GameMap
from .entities import Pacman, Ghost

class PacmanEnv:
    def __init__(self):
        self.map = GameMap()
        
        # Initialize Pac-Man
        px, py = self.map.start_pos
        self.pacman = Pacman(px, py)
        
        # Initialize Ghosts
        self.ghosts = [Ghost(x, y) for (x, y) in self.map.ghost_positions]
        
        # Action dictionary: 0=up, 1=down, 2=left, 3=right
        self.actions = {
            0: (-1, 0),
            1: (1, 0),
            2: (0, -1),
            3: (0, 1)
        }

    def reset(self):
        # Reset Pac-Man
        self.pacman.x, self.pacman.y = self.map.start_pos
        
        # Reset Ghosts
        for ghost, pos in zip(self.ghosts, self.map.ghost_positions):
            ghost.x, ghost.y = pos
        
        return self.get_observation()

    def step(self, action):
        reward = 0
        done = False
        
        # --- Pac-Man movement ---
        dx, dy = self.actions[action]
        new_x = self.pacman.x + dx
        new_y = self.pacman.y + dy
        
        if not self.map.is_wall(new_x, new_y):
            self.pacman.move(dx, dy)
            
            # Collect dot
            if self.map.grid[self.pacman.y][self.pacman.x] == 2:
                reward += 10
                self.map.grid[self.pacman.y][self.pacman.x] = 0
        else:
            reward -= 1  # bump into wall penalty
        
        # --- Ghost movement (random simple) ---
        for g in self.ghosts:
            self.ghost_random_move(g)
        
        # --- Check collisions ---
        for g in self.ghosts:
            if (g.x, g.y) == (self.pacman.x, self.pacman.y):
                reward -= 100
                done = True
        
        # --- Check win condition ---
        if self.map.remaining_dots() == 0:
            reward += 200
            done = True
        
        return self.get_observation(), reward, done, {}

    def ghost_random_move(self, ghost):
        directions = list(self.actions.values())
        random.shuffle(directions)
        for dx, dy in directions:
            new_x = ghost.x + dx
            new_y = ghost.y + dy
            if not self.map.is_wall(new_x, new_y):
                ghost.move(dx, dy)
                break

    def render(self):
        for y in range(self.map.height):
            row = ""
            for x in range(self.map.width):
                if (x, y) == (self.pacman.x, self.pacman.y):
                    row += "P "
                elif any((g.x, g.y) == (x, y) for g in self.ghosts):
                    row += "G "
                elif self.map.grid[y][x] == 2:
                    row += ". "
                elif self.map.grid[y][x] == 1:
                    row += "# "
                else:
                    row += "  "
            print(row)
        print("\n")

    def get_observation(self):
        # Return a simple 2D numpy array representing the current map
        obs = np.copy(self.map.grid)
        obs[self.pacman.y, self.pacman.x] = 4  # mark Pac-Man
        for g in self.ghosts:
            obs[g.y, g.x] = 3  # mark ghosts
        return obs
