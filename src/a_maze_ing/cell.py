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
            int(self.north) * 8 +
            int(self.east) * 4 +
            int(self.south) * 2 +
            int(self.west) * 1
        )[2:].upper()
