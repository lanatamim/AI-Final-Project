# entities.py

class Entity:
    """Base class for Pac-Man and Ghosts."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy


class Pacman(Entity):
    """Pac-Man player entity."""
    def __init__(self, x, y):
        super().__init__(x, y)


class Ghost(Entity):
    """Ghost enemy entity."""
    def __init__(self, x, y):
        super().__init__(x, y)
