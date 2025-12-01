class GameMap:
    """
    Standard fully connected Pac-Man maze.
    # = wall
    . = dot
    P = power pellet
    = = ghost gate
    space = empty
    """

    def __init__(self):
        # Load ONLY the fixed, connected maze
        raw = self._maze_arcade_clean()

        # Parse into a grid
        self.grid = self._parse(raw)

        self.height = len(self.grid)
        self.width = len(self.grid[0])

        # Pac-Man always starts here
        self.start_pos = (1, 1)

        # Ghost starts at center of ghost room
        self.ghost_starts = [(self.width // 2, self.height // 2)]
        self.ghost_positions = self.ghost_starts[:]

    # -------------------------------
    # WALL CHECK
    # -------------------------------
    def is_wall(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return self.grid[y][x] == 1

    def remaining_dots(self):
        return sum(row.count(2) for row in self.grid)

    # -------------------------------
    # PARSER
    # -------------------------------
    def _parse(self, maze_str):
        raw_lines = [line.rstrip() for line in maze_str.split("\n") if line.strip()]
        max_width = max(len(line) for line in raw_lines)

        grid = []
        for line in raw_lines:
            padded = line.ljust(max_width, " ")  # pad with empty, NOT walls

            row = []
            for ch in padded:
                if ch == "#":
                    row.append(1)     # wall
                elif ch == ".":
                    row.append(2)     # dot
                elif ch == "P":
                    row.append(2)     # power pellet as dot
                elif ch == "=":
                    row.append(0)     # ghost gate
                else:
                    row.append(0)     # empty
            grid.append(row)

        return grid

    # -------------------------------
    # FIXED, CONNECTED MAZE
    # -------------------------------
    def _maze_arcade_clean(self):
        return """
############################
#............##............#
#.####.#####.##.#####.####.#
#P####.#####.##.#####.####P#
#.####.#####.##.#####.####.#
#............==............#
#.####.##.########.##.####.#
#.####.##....##....##.####.#
#......##### ## #####......#
######.##### ## #####.######
######.##          ##.######
######.## ######## ##.######
#............##............#
#.####.#####.##.#####.####.#
#P.......##   G   ##.......P#
######.## ######## ##.######
######.##          ##.######
######.## ######## ##.######
#............##............#
############################
"""
