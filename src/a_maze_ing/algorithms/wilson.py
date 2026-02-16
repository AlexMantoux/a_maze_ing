from collections.abc import Callable
from src.a_maze_ing.cell import Cell, CellState
from random import choice as rd_choice
from src.a_maze_ing.algorithms.ft_pattern import where_is_ft_pattern


def _get_neighbors(
        coordinates: tuple[int, int],
        grid: list[list[Cell]],
        pattern_positions: set[tuple[int, int]]
) -> list[Cell]:
    x, y = coordinates
    neighbors = []
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    if y > 0 and grid[y - 1][x] and (x, y - 1) not in pattern_positions:
        neighbors.append(grid[y - 1][x])
    if y < height - 1 and grid[y + 1][x] and (x, y + 1) not in pattern_positions:
        neighbors.append(grid[y + 1][x])
    if x > 0 and grid[y][x - 1] and (x - 1, y) not in pattern_positions:
        neighbors.append(grid[y][x - 1])
    if x < width - 1 and grid[y][x + 1] and (x + 1, y) not in pattern_positions:
        neighbors.append(grid[y][x + 1])

    return neighbors

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

def _has_unvisited(grid: list[list[Cell]]):
    return any(
        cell.state == CellState.UNVISITED
        for row in grid
        for cell in row
    )

def _get_random_unvisited(grid: list[list[Cell]]):
    unvisited = [
        cell for row in grid
        for cell in row
        if cell.state == CellState.UNVISITED
    ]
    return rd_choice(unvisited)

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
    pattern_positions = where_is_ft_pattern(grid)
    for x, y in pattern_positions:
        grid[y][x].state = CellState.VISITED
    return grid

def generate_wilson(
        config: dict[str, object],
        on_step: Callable[[list[list[Cell]]], None] | None = None
        ) -> list[list[Cell]]:
    width: int = config["WIDTH"]
    height: int = config["HEIGHT"]
    assert isinstance(width, int)
    assert isinstance(height, int)
    grid = _generate_full_grid(width, height)
    
    pattern_positions = set(where_is_ft_pattern(grid))

    random_cell_in_maze: Cell = _get_random_unvisited(grid)
    random_cell_in_maze.state = CellState.IN_MAZE

    if on_step:
        on_step(grid)

    while _has_unvisited(grid):
        current_cell: Cell = _get_random_unvisited(grid)
        path: list[Cell] = [current_cell]
        while (current_cell.state != CellState.IN_MAZE):
            neighbors = _get_neighbors(current_cell.coordinates, grid, pattern_positions)
            if not neighbors:
                break
            next_cell: Cell = rd_choice(neighbors)
            if next_cell in path:
                index = path.index(next_cell)
                path = path[:index+1]
            else:
                path.append(next_cell)
            current_cell = next_cell
        
        if current_cell.state == CellState.IN_MAZE:
            for i in range(len(path) - 1):
                _remove_walls_between(path[i], path[i+1])
                if on_step:
                    on_step(grid)
            for cells in path:
                cells.state = CellState.IN_MAZE
    
    return grid