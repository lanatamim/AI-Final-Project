class GameMap:
    """
    Maze loader for Pac-Man.
    # = wall
    . = dot
    P = power pellet
    space = empty
    """

    def __init__(self, maze_id=1):
        self.mazes = {
            1: self._maze_simple(),
            2: self._maze_classic(),
            3: self._maze_power(),
            4: self._maze_hard()
        }

        # Load selected ASCII maze
        raw = self.mazes[maze_id]

        # Parse -> rectangular 2D list
        self.grid = self._parse(raw)

        # Height/width after parsing
        self.height = len(self.grid)
        self.width = len(self.grid[0])

        # Pac-Man start
        self.start_pos = (1, 1)

        # Ghost start(s)
        self.ghost_starts = [(self.width - 2, self.height - 2)]
        self.ghost_positions = self.ghost_starts[:]

    # Check if wall
    def is_wall(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        return self.grid[y][x] == 1
    
    def remaining_dots(self):
        """Count all dot tiles (value == 2) remaining in the maze."""
        count = 0
        for row in self.grid:
            count += row.count(2)
        return count

    # PARSE MAZE TEXT → CLEAN RECTANGULAR GRID
    def _parse(self, maze_str):
        # Split lines, remove empty ones
        lines = [
            line.rstrip()
            for line in maze_str.split("\n")
            if line.strip()
        ]

        # Remove tabs, force spaces
        lines = [line.replace("\t", " ") for line in lines]

        # Compute maximum width
        max_len = max(len(line) for line in lines)

        grid = []
        for line in lines:
            # pad shorter lines with walls (#)
            padded = line.ljust(max_len, "#")

            row = []
            for ch in padded:
                if ch == "#":
                    row.append(1)
                elif ch == ".":
                    row.append(2)
                elif ch == "P":
                    row.append(2)
                else:
                    row.append(0)
            grid.append(row)

        return grid

    # MAZES
    def _maze_simple(self):
        return """
####################
#......##......##..#
#.####.#.####.#....#
#.#....#......#.##.#
#.#.##.######.#....#
#.#.##........#.##.#
#......#######......#
####.#.......#.#####
#....###...###....#.#
#....#.......#....#.#
#....###...###....#.#
####.#.......#.#####
#......#######......#
#.#.##........#.##.#
#.#.##.######.#....#
#.#....#......#.##.#
#.####.#.####.#....#
#......##......##..#
####################
"""

    def _maze_classic(self):
        return """
####################
#........##........#
#.####.#.##.#.####.#
#.#  #.#....#. #.  #
#.#  #.######.# #  #
#......#....#......#
#.####.#.##.#.####.#
#........##........#
#######.####.#######
#.......####.......#
#######.####.#######
#........##........#
#.####.#.##.#.####.#
#......#....#......#
#.#  #.######.# #  #
#.#  #....##....#  #
#.#.####.##.####.#.#
#........##........#
####################
"""

    def _maze_power(self):
        return """
####################
#P......##......P..#
#.####.#.##.#.####.#
#.#....#....#....#.#
#.#.##.######.##.#.#
#......#....#......#
#.####.#.##.#.####.#
#P......####......P#
####.#.......#.#####
#....###P.P###....#.#
#....#.......#....#.#
#.P..###...###..P.#.#
####.#.......#.#####
#......#######......#
#.#.##........#.##.#
#.#.##.######.#....#
#.#....#......#.##.#
#.####.#.####.#....#
#P......##......P..#
####################
"""

    def _maze_hard(self):
        return """
####################
#....#....##....#..#
#.##.#.##.##.##.#.##
#.#..#....##....#.#.#
#.#.####.####.###.#.#
#.....##......##....#
###.#.####.####.#.###
#...#....#....#...#.#
#.###.########.###.##
#.....# P..P #.....#.#
#.###.########.###.##
#...#....#....#...#.#
###.#.####.####.#.###
#.....##......##....#
#.#.####.####.###.#.#
#.#..#....##....#.#.#
#.##.#.##.##.##.#.##
#....#....##....#..#
####################
"""
