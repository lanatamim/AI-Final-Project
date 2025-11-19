# game_map.py

class GameMap:
    """
    Simple grid-based map for Pac-Man.
    0 = empty space
    1 = wall
    2 = dot (reward)
    """

    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.grid = self._create_default_map()

        # Pac-Man starting position (must not be a wall)
        self.start_pos = (1, 1)

        # Ghost starting positions
        self.ghost_starts = [(width - 2, height - 2)]  # bottom-right corner

        # PacmanEnv expects ghost_positions
        self.ghost_positions = self.ghost_starts[:]

    def _create_default_map(self):
        grid = [[2 for _ in range(self.width)] for _ in range(self.height)]

        # Add border walls
        for x in range(self.width):
            grid[0][x] = 1
            grid[self.height - 1][x] = 1
        for y in range(self.height):
            grid[y][0] = 1
            grid[y][self.width - 1] = 1

        # Clear Pac-Man's start tile
        grid[1][1] = 0

        return grid

    def is_wall(self, x, y):
        return self.grid[y][x] == 1

    def remove_dot(self, x, y):
        if self.grid[y][x] == 2:
            self.grid[y][x] = 0  # remove dot
            return True
        return False

    def remaining_dots(self):
        return sum(row.count(2) for row in self.grid)
