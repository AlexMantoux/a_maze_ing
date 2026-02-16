from collections.abc import Callable
from random import choice as random_choice
from src.a_maze_ing.core.cell import Cell, CellState
from src.a_maze_ing.algorithms.grid_utils import (
    generate_full_grid,
    get_neighbors,
    remove_walls_between
)


def generate_dfs(
        config: dict[str, object],
        on_step: Callable[[list[list[Cell]]], None] | None = None
) -> list[list[Cell]]:
    entry = config["ENTRY"]
    assert isinstance(entry, tuple)
    x, y = entry
    width = config["WIDTH"]
    height = config["HEIGHT"]
    assert isinstance(width, int)
    assert isinstance(height, int)
    grid, _ = generate_full_grid(width, height)
    current = grid[y][x]
    current.state = CellState.VISITED
    stack = [current]
    if on_step:
        on_step(grid)

    while stack:
        current = stack[-1]
        neighbors = [nb for nb in get_neighbors(current.coordinates, grid)
                     if nb.state != CellState.VISITED]

        if neighbors:
            next_cell = random_choice(neighbors)
            remove_walls_between(current, next_cell)
            next_cell.state = CellState.VISITED
            stack.append(next_cell)
            if on_step:
                on_step(grid)
        else:
            stack.pop()

    return grid
