"""Cell model for maze grids."""

from enum import Enum, auto


class CellState(Enum):
    """State markers used during maze generation and solving."""

    UNVISITED = auto()
    VISITED = auto()
    FRONTIER = auto()
    IN_MAZE = auto()
    PATH = auto()


class Cell:
    """Represent a single maze cell and its walls."""

    def __init__(self,
                 state: CellState,
                 north: bool,
                 east: bool,
                 south: bool,
                 west: bool,
                 coordinates: tuple[int, int]
                 ) -> None:
        """Initialize a maze cell.

        Args:
            state: Initial state of the cell.
            north: Whether the north wall is closed.
            east: Whether the east wall is closed.
            south: Whether the south wall is closed.
            west: Whether the west wall is closed.
            coordinates: Cell coordinates as (x, y).
        """
        self.state = state

        self.north = north
        self.east = east
        self.south = south
        self.west = west

        self.coordinates = coordinates

    def __str__(self) -> str:
        """Return the hexadecimal wall encoding for the cell."""
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
        """Check if a wall exists in the given direction.

        Args:
            direction: Direction character (N/E/S/W).

        Returns:
            True if the wall is closed in that direction.
        """
        return {
            "N": self.north,
            "E": self.east,
            "S": self.south,
            "W": self.west
        }[direction.upper()]

    def set_wall(self, direction: str, value: bool) -> None:
        """Set the wall state in the given direction.

        Args:
            direction: Direction character (N/E/S/W).
            value: True to close the wall, False to open it.
        """
        direction = direction.upper()
        if direction == "N":
            self.north = value
        elif direction == "E":
            self.east = value
        elif direction == "S":
            self.south = value
        elif direction == "W":
            self.west = value
