"""Wilson's algorithm for maze generation."""

from collections.abc import Callable
from random import choice as rd_choice
from src.a_maze_ing.core.cell import Cell, CellState
from src.a_maze_ing.algorithms.grid_utils import (
    generate_full_grid,
    get_neighbors,
    remove_walls_between
)


def _has_unvisited(grid: list[list[Cell]]):
    """Check whether the grid contains unvisited cells.

    Args:
        grid: 2D maze grid.

    Returns:
        True if any cell is unvisited, otherwise False.
    """
    return any(
        cell.state == CellState.UNVISITED
        for row in grid
        for cell in row
    )


def _get_random_unvisited(grid: list[list[Cell]]):
    """Pick a random unvisited cell.

    Args:
        grid: 2D maze grid.

    Returns:
        A randomly selected unvisited cell.
    """
    unvisited = [
        cell for row in grid
        for cell in row
        if cell.state == CellState.UNVISITED
    ]
    return rd_choice(unvisited)


def generate_wilson(
        config: dict[str, object],
        on_step: Callable[[list[list[Cell]]], None] | None = None
        ) -> list[list[Cell]]:
    """Generate a perfect maze using Wilson's algorithm.

    Args:
        config: Configuration dictionary with WIDTH and HEIGHT keys.
        on_step: Optional callback called after each carving step.

    Returns:
        Generated maze grid.
    """
    width: int = config["WIDTH"]
    height: int = config["HEIGHT"]
    assert isinstance(width, int)
    assert isinstance(height, int)
    grid, pattern_positions = generate_full_grid(width, height)

    random_cell_in_maze: Cell = _get_random_unvisited(grid)
    random_cell_in_maze.state = CellState.IN_MAZE

    if on_step:
        on_step(grid)

    while _has_unvisited(grid):
        current_cell: Cell = _get_random_unvisited(grid)
        path: list[Cell] = [current_cell]
        while (current_cell.state != CellState.IN_MAZE):
            neighbors = get_neighbors(
                current_cell.coordinates,
                grid,
                blocked=pattern_positions
            )
            if not neighbors:
                break
            next_cell: Cell = rd_choice(neighbors)
            if next_cell in path:
                index = path.index(next_cell)
                path = path[:index + 1]
            else:
                path.append(next_cell)
            current_cell = next_cell

        if current_cell.state == CellState.IN_MAZE:
            for i in range(len(path) - 1):
                remove_walls_between(path[i], path[i + 1])
                if on_step:
                    on_step(grid)
            for cells in path:
                cells.state = CellState.IN_MAZE

    return grid
