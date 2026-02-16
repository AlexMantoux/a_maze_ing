from src.a_maze_ing.core.cell import Cell, CellState
from src.a_maze_ing.algorithms.ft_pattern import where_is_ft_pattern


def generate_full_grid(
        width: int,
        height: int
) -> tuple[list[list[Cell]], set[tuple[int, int]]]:
    grid = [
        [
            Cell(
                CellState.UNVISITED,
                True, True, True, True,
                (x, y)
            ) for x in range(width)
        ] for y in range(height)
    ]
    pattern_positions = set(where_is_ft_pattern(grid))
    for x, y in pattern_positions:
        grid[y][x].state = CellState.VISITED
    return grid, pattern_positions


def get_neighbors(
        coordinates: tuple[int, int],
        grid: list[list[Cell]],
        blocked: set[tuple[int, int]] | None = None
) -> list[Cell]:
    x, y = coordinates
    neighbors = []
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    blocked_positions = blocked or set()

    if y > 0 and (x, y - 1) not in blocked_positions:
        neighbors.append(grid[y - 1][x])
    if y < height - 1 and (x, y + 1) not in blocked_positions:
        neighbors.append(grid[y + 1][x])
    if x > 0 and (x - 1, y) not in blocked_positions:
        neighbors.append(grid[y][x - 1])
    if x < width - 1 and (x + 1, y) not in blocked_positions:
        neighbors.append(grid[y][x + 1])

    return neighbors


def remove_walls_between(cell1: Cell, cell2: Cell) -> None:
    """Remove the walls between two adjacent cells."""
    x1, y1 = cell1.coordinates
    x2, y2 = cell2.coordinates

    if x1 == x2:
        if y2 < y1:
            cell1.north = False
            cell2.south = False
        else:
            cell1.south = False
            cell2.north = False
    elif y1 == y2:
        if x2 < x1:
            cell1.west = False
            cell2.east = False
        else:
            cell1.east = False
            cell2.west = False
