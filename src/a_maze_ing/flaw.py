from collections.abc import Callable
from src.a_maze_ing.cell import Cell
from src.a_maze_ing.algorithms.ft_pattern import where_is_ft_pattern
from random import choice as random_choice
from enum import Enum, auto


class CardinalPoint(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()


def _get_neighbors(
    cell: Cell,
    grid: list[list[Cell]]
) -> dict[CardinalPoint, Cell]:
    x, y = cell.coordinates
    neighbors = {}
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    if y > 0 and grid[y - 1][x]:
        neighbors[CardinalPoint.NORTH] = grid[y - 1][x]
    if y < height - 1 and grid[y + 1][x]:
        neighbors[CardinalPoint.SOUTH] = grid[y + 1][x]
    if x > 0 and grid[y][x - 1]:
        neighbors[CardinalPoint.WEST] = grid[y][x - 1]
    if x < width - 1 and grid[y][x + 1]:
        neighbors[CardinalPoint.EAST] = grid[y][x + 1]

    return neighbors


def _wall_breakable_toward(
    grid: list[list[Cell]],
    cell: Cell,
    direction: CardinalPoint
) -> bool:
    if cell.coordinates in where_is_ft_pattern(grid):
        return False
    neighbors = _get_neighbors(cell, grid)
    for direction in neighbors:
        if neighbors[direction].coordinates in where_is_ft_pattern(grid):
            return False

    match direction:
        case CardinalPoint.NORTH:
            if CardinalPoint.NORTH not in neighbors:
                return False
            if not neighbors[CardinalPoint.NORTH].south:
                return False
        case CardinalPoint.SOUTH:
            if CardinalPoint.SOUTH not in neighbors:
                return False
            if not neighbors[CardinalPoint.SOUTH].north:
                return False
        case CardinalPoint.EAST:
            if CardinalPoint.EAST not in neighbors:
                return False
            if not neighbors[CardinalPoint.EAST].west:
                return False
        case CardinalPoint.WEST:
            if CardinalPoint.WEST not in neighbors:
                return False
            if not neighbors[CardinalPoint.WEST].east:
                return False

    return True


def _remove_walls_toward(
    grid: list[list[Cell]],
    cell: Cell,
    direction: CardinalPoint
) -> None:
    """
    Removes the walls between two adjacent cells.
    """
    x, y = cell.coordinates
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    match direction:
        case CardinalPoint.NORTH:
            if y > 0:
                cell.north = False
                grid[y - 1][x].south = False
        case CardinalPoint.SOUTH:
            if y < height - 1:
                cell.south = False
                grid[y + 1][x].north = False
        case CardinalPoint.EAST:
            if x < width - 1:
                cell.east = False
                grid[y][x + 1].west = False
        case CardinalPoint.WEST:
            if x > 0:
                cell.west = False
                grid[y][x - 1].east = False


def flaw_maze(
    maze: list[list[Cell]],
    on_step: Callable[[list[list[Cell]]], None] | None = None
) -> None:
    walls_to_break: int = len(maze) * len(maze[0]) // 7
    iterations_remaining: int = 1500

    while walls_to_break > 0 and iterations_remaining > 0:
        rd_cell: Cell = random_choice(random_choice(maze))
        rd_direction = random_choice(list(CardinalPoint))

        if _wall_breakable_toward(maze, rd_cell, rd_direction):
            _remove_walls_toward(maze, rd_cell, rd_direction)
            walls_to_break -= 1
            if on_step:
                on_step(maze)
        
        iterations_remaining -= 1
