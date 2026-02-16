from enum import Enum, auto


class CellState(Enum):
    UNVISITED = auto()
    VISITED = auto()
    FRONTIER = auto()
    IN_MAZE = auto()
    PATH = auto()


class Cell:
    def __init__(self,
                 state: CellState,
                 north: bool,
                 east: bool,
                 south: bool,
                 west: bool,
                 coordinates: tuple[int, int]
                 ) -> None:
        self.state = state

        self.north = north
        self.east = east
        self.south = south
        self.west = west

        self.coordinates = coordinates

    def __str__(self) -> str:
        return hex(
            int(self.north) * 1 +
            int(self.east) * 2 +
            int(self.south) * 4 +
            int(self.west) * 8
        )[2:].upper()

    def to_hex(self) -> str:
        """Return hexadecimal representation of the cell walls."""
        return str(self)

    def has_wall(self, direction: str) -> bool:
        """Check if wall exists in given direction (N/E/S/W)."""
        return {
            "N": self.north,
            "E": self.east,
            "S": self.south,
            "W": self.west
        }[direction.upper()]

    def set_wall(self, direction: str, value: bool) -> None:
        """Set wall state in given direction (N/E/S/W)."""
        direction = direction.upper()
        if direction == "N":
            self.north = value
        elif direction == "E":
            self.east = value
        elif direction == "S":
            self.south = value
        elif direction == "W":
            self.west = value
