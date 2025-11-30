import numpy as np
import random
from .game_map import GameMap
from .entities import Pacman, Ghost
from .pathfinding import a_star_path

class PacmanEnv:
    def __init__(self):
        self.map = GameMap()
        
        # Initialize Pac-Man
        px, py = self.map.start_pos
        self.pacman = Pacman(px, py)
        
        # Initialize one ghost (you can extend to more later)
        self.ghosts = [Ghost(x, y) for (x, y) in self.map.ghost_positions]

        # If map only provided one ghost start, keep it.
        if not self.ghosts:
            gx, gy = self.map.width - 2, self.map.height - 2
            self.ghosts = [Ghost(gx, gy)]
            self.map.ghost_positions = [(gx, gy)]

        # Action dictionary: 0=up, 1=down, 2=left, 3=right
        self.actions = {
            0: (0, -1),   # up (y - 1)
            1: (0, 1),    # down (y + 1)
            2: (-1, 0),   # left (x - 1)
            3: (1, 0)     # right (x + 1)
        }

        # --- Ghost behavior system (Pac-Man style-ish) ---
        # Scatter: ghost runs toward its corner.
        # Chase: ghost uses A* to chase Pac-Man.
        self.mode = "scatter"       # "scatter" or "chase"
        self.mode_timer = 0         # counts steps in current mode

        # Scatter target (top-right corner-ish)
        self.scatter_target = (self.map.width - 2, 1)

    # Reset
    def reset(self):
        # Reset Pac-Man
        self.pacman.x, self.pacman.y = self.map.start_pos
        
        # Reset Ghost(s)
        for ghost, pos in zip(self.ghosts, self.map.ghost_positions):
            ghost.x, ghost.y = pos
        
        # Reset ghost mode system
        self.mode = "scatter"
        self.mode_timer = 0

        return self.get_observation()

    # Step function
    def step(self, action):
        reward = 0
        done = False
        
        # ---------- Pac-Man movement ----------
        dx, dy = self.actions[action]
        new_x = self.pacman.x + dx
        new_y = self.pacman.y + dy
        
        if not self.map.is_wall(new_x, new_y):
            self.pacman.move(dx, dy)
            
            # Collect dot (2 = dot)
            tile = self.map.grid[self.pacman.y][self.pacman.x]
            if tile == 2:
                reward += 10
                self.map.grid[self.pacman.y][self.pacman.x] = 0
        else:
            # bump into wall penalty
            reward -= 2
        
        # ---------- Update ghost mode (scatter <-> chase) ----------
        self.update_ghost_mode()

        # ---------- Ghost movement ----------
        for g in self.ghosts:
            self.ghost_smart_move(g)

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

    # Ghost mode system (scatter / chase cycling)
    def update_ghost_mode(self):
        """
        Simple Pac-Man style mode cycles:
        - Scatter for a while (ghost runs to corner)
        - Then Chase (ghost chases Pac-Man)
        - Then back to Scatter, etc.
        """

        self.mode_timer += 1

        if self.mode == "scatter":
            # after ~40 steps, switch to chase
            if self.mode_timer > 40:
                self.mode = "chase"
                self.mode_timer = 0
        elif self.mode == "chase":
            # after ~80 steps, switch back to scatter
            if self.mode_timer > 80:
                self.mode = "scatter"
                self.mode_timer = 0

    # Ghost movement: smarter, Pac-Man-like
    def ghost_smart_move(self, ghost):
        start = (ghost.x, ghost.y)

        if self.mode == "scatter":
            # Run toward scatter corner
            target = self.scatter_target
        else:
            # Chase Pac-Man
            target = (self.pacman.x, self.pacman.y)

        path = a_star_path(self.map, start, target)

        if path and len(path) > 1:
            # Move to next tile on A* path
            next_x, next_y = path[1]
            ghost.x, ghost.y = next_x, next_y
        else:
            # No good path (or already at target) → move randomly but valid
            self.ghost_random_move(ghost)

    def ghost_random_move(self, ghost):
        # Truly random among ALL valid neighbor tiles (no more left-right only)
        valid_moves = []
        for dx, dy in self.actions.values():
            new_x = ghost.x + dx
            new_y = ghost.y + dy
            if not self.map.is_wall(new_x, new_y):
                valid_moves.append((dx, dy))

        if valid_moves:
            dx, dy = random.choice(valid_moves)
            ghost.move(dx, dy)

    # Get valid actions for RL agent
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

    # Rendering
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

    # Observation for RL
    def get_observation(self):
        # Use a proper numpy 2D array
        obs = np.array(self.map.grid, dtype=int)
        # Pac-Man mark
        obs[self.pacman.y][self.pacman.x] = 4
        # Ghost(s) mark
        for g in self.ghosts:
            obs[g.y][g.x] = 3
        return obs
