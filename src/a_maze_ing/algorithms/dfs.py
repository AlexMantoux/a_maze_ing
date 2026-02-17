"""Depth-first search maze generation."""

from collections.abc import Callable
from random import choice as random_choice
from src.a_maze_ing.core.cell import Cell, CellState
from src.a_maze_ing.core.types import MazeConfig
from src.a_maze_ing.algorithms.grid_utils import (
    generate_full_grid,
    get_neighbors,
    remove_walls_between
)


def generate_dfs(
        config: MazeConfig,
        on_step: Callable[[list[list[Cell]]], None] | None = None
) -> list[list[Cell]]:
    """Generate a perfect maze using recursive backtracker (DFS).

    Args:
        config: Configuration dictionary with WIDTH, HEIGHT, ENTRY keys.
        on_step: Optional callback called after each carving step.

    Returns:
        Generated maze grid.
    """
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
