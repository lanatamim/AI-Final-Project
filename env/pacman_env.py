import numpy as np
import random
from .game_map import GameMap
from .entities import Pacman, Ghost
from .pathfinding import a_star_path  # NEW: import A*

class PacmanEnv:
    def __init__(self, ghost_mode="mixed"):
        """
        ghost_mode = "random", "chase", or "mixed"
        mixed => ghosts chase 50% of the time, move randomly otherwise
        """
        self.map = GameMap()
        self.ghost_mode = ghost_mode
        
        # Initialize Pac-Man
        px, py = self.map.start_pos
        self.pacman = Pacman(px, py)
        
        # Initialize Ghosts
        self.ghosts = [Ghost(x, y) for (x, y) in self.map.ghost_positions]
        
        # Action dictionary: 0=up, 1=down, 2=left, 3=right
        self.actions = {
            0: (-1, 0),   # up
            1: (1, 0),    # down
            2: (0, -1),   # left
            3: (0, 1)     # right
        }

    # ----------------------------------------------------------------------
    # Reset
    # ----------------------------------------------------------------------
    def reset(self):
        self.pacman.x, self.pacman.y = self.map.start_pos
        
        for ghost, pos in zip(self.ghosts, self.map.ghost_positions):
            ghost.x, ghost.y = pos
        
        return self.get_observation()

    # ----------------------------------------------------------------------
    # Step function
    # ----------------------------------------------------------------------
    def step(self, action):
        reward = 0
        done = False
        
        # ---------- Pac-Man movement ----------
        dx, dy = self.actions[action]
        new_x = self.pacman.x + dx
        new_y = self.pacman.y + dy
        
        if not self.map.is_wall(new_x, new_y):
            self.pacman.move(dx, dy)
            
            # Dot collection
            if self.map.grid[self.pacman.y][self.pacman.x] == 2:
                reward += 10
                self.map.grid[self.pacman.y][self.pacman.x] = 0
        else:
            reward -= 2  # penalty for bumping wall
        
        # ---------- Ghost movement ----------
        for g in self.ghosts:
            self.move_ghost(g)
        
        # ---------- Collisions ----------
        for g in self.ghosts:
            if (g.x, g.y) == (self.pacman.x, self.pacman.y):
                reward -= 100
                done = True
        
        # ---------- Win condition ----------
        if self.map.remaining_dots() == 0:
            reward += 200
            done = True
        
        return self.get_observation(), reward, done, {}

    # ----------------------------------------------------------------------
    # Ghost movement: random, chase, or mixed
    # ----------------------------------------------------------------------
    def move_ghost(self, ghost):
        mode = self.ghost_mode
        
        # Mixed mode logic
        if mode == "mixed":
            mode = "chase" if random.random() < 0.5 else "random"
        
        if mode == "random":
            self.ghost_random_move(ghost)
        elif mode == "chase":
            self.ghost_chase_move(ghost)

    # ----------------------------------------------------------------------
    # Simple random ghost movement
    # ----------------------------------------------------------------------
    def ghost_random_move(self, ghost):
        directions = list(self.actions.values())
        random.shuffle(directions)
        for dx, dy in directions:
            new_x = ghost.x + dx
            new_y = ghost.y + dy
            if not self.map.is_wall(new_x, new_y):
                ghost.move(dx, dy)
                break

    # ----------------------------------------------------------------------
    # A* ghost chasing movement
    # ----------------------------------------------------------------------
    def ghost_chase_move(self, ghost):
        start = (ghost.x, ghost.y)
        goal = (self.pacman.x, self.pacman.y)
        
        path = a_star_path(self.map, start, goal)
        
        # A* returns full list including start; need next step
        if path and len(path) > 1:
            next_x, next_y = path[1]
            ghost.x, ghost.y = next_x, next_y
        else:
            # fallback to random if no path
            self.ghost_random_move(ghost)

    # ----------------------------------------------------------------------
    # Get valid actions for RL agent
    # ----------------------------------------------------------------------
    def get_valid_actions(self):
        valid = []
        for a, (dx, dy) in self.actions.items():
            nx = self.pacman.x + dx
            ny = self.pacman.y + dy
            if not self.map.is_wall(nx, ny):
                valid.append(a)
        return valid

    def get_pacman_position(self):
        return (self.pacman.x, self.pacman.y)

    def get_ghost_positions(self):
        return [(g.x, g.y) for g in self.ghosts]

    # ----------------------------------------------------------------------
    # Rendering
    # ----------------------------------------------------------------------
    def render(self):
        print("----- PACMAN ENV -----")
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

    # ----------------------------------------------------------------------
    # Observation for RL
    # ----------------------------------------------------------------------
    def get_observation(self):
        obs = np.copy(self.map.grid)
        obs[self.pacman.y, self.pacman.x] = 4  # mark Pac-Man
        for g in self.ghosts:
            obs[g.y][g.x] = 3  # mark ghosts
        return obs
