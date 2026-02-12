from collections.abc import Callable
from src.a_maze_ing.cell import Cell, CellState
from random import choice as random_choice
from src.a_maze_ing.algorithms.ft_pattern import where_is_ft_pattern


def _get_neighbors(
        coordinates: tuple[int, int],
        grid: list[list[Cell]]
) -> list[Cell]:
    x, y = coordinates
    neighbors = []
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    if y > 0 and grid[y - 1][x]:
        neighbors.append(grid[y - 1][x])
    if y < height - 1 and grid[y + 1][x]:
        neighbors.append(grid[y + 1][x])
    if x > 0 and grid[y][x - 1]:
        neighbors.append(grid[y][x - 1])
    if x < width - 1 and grid[y][x + 1]:
        neighbors.append(grid[y][x + 1])

    return neighbors


def _generate_full_grid(width: int, height: int) -> list[list[Cell]]:
    grid = [
        [
            Cell(
                CellState.UNVISITED,
                True, True, True, True,
                (x, y)
            ) for x in range(width)
        ] for y in range(height)
    ]
    for x, y in where_is_ft_pattern(grid):
        grid[y][x].state = CellState.VISITED
    return grid


def _remove_walls_between(cell1: Cell, cell2: Cell) -> None:
    """
    Removes the walls between two adjacent cells.
    """
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


def generate_dfs(
        config: dict[str, int | tuple[int, int] | str | bool],
        on_step: Callable[[list[list[Cell]]], None] | None = None
) -> list[list[Cell]]:
    entry = config["ENTRY"]
    assert isinstance(entry, tuple)
    x, y = entry
    width = config["WIDTH"]
    height = config["HEIGHT"]
    assert isinstance(width, int)
    assert isinstance(height, int)
    grid = _generate_full_grid(width, height)
    current = grid[y][x]
    current.state = CellState.VISITED
    stack = [current]
    if on_step:
        on_step(grid)

    while stack:
        current = stack[-1]
        neighbors = [nb for nb in _get_neighbors(current.coordinates, grid)
                     if nb.state != CellState.VISITED]

        if neighbors:
            next_cell = random_choice(neighbors)
            _remove_walls_between(current, next_cell)
            next_cell.state = CellState.VISITED
            stack.append(next_cell)
            if on_step:
                on_step(grid)
        else:
            stack.pop()

    return grid
