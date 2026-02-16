"""MazeGenerator wrapper class for bundling.

This module provides the main MazeGenerator class that wraps all algorithms.
"""

from collections.abc import Callable
import random

from src.a_maze_ing.core.cell import Cell
from src.a_maze_ing.algorithms.dfs import generate_dfs
from src.a_maze_ing.algorithms.kruskal import generate_kruskal
from src.a_maze_ing.algorithms.a_star import a_star
from src.a_maze_ing.algorithms.ft_pattern import where_is_ft_pattern
from src.a_maze_ing.algorithms.wilson import generate_wilson


class MazeGenerator:
    """A configurable maze generator supporting multiple algorithms.

    This class wraps the DFS, Kruskal, and Wilson generation algorithms and
    A* solver.
    Generated mazes are perfect mazes (exactly one path between any two cells).

    Attributes:
        width: Number of cells horizontally.
        height: Number of cells vertically.
        seed: Random seed for reproducibility.
        algorithm: 'DFS', 'KRUSKAL', or 'WILSON'.
        include_pattern: Whether to include the 42 pattern.
        maze: The generated maze grid (None until generate() is called).

    Example:
        >>> from mazegen import MazeGenerator
        >>> gen = MazeGenerator(width=20, height=15, seed=42)
        >>> maze = gen.generate()
        >>> path = gen.solve((0, 0), (19, 14))
    """

    def __init__(
        self,
        width: int = 20,
        height: int = 15,
        seed: int | None = None,
        algorithm: str = "DFS",
        include_pattern: bool = True
    ) -> None:
        if width < 1:
            raise ValueError(f"Width must be at least 1, got {width}")
        if height < 1:
            raise ValueError(f"Height must be at least 1, got {height}")
        if algorithm.upper() not in ("DFS", "KRUSKAL", "WILSON"):
            raise ValueError(
                f"Algorithm must be 'DFS', 'KRUSKAL', or 'WILSON', got {algorithm}"
            )

        self.width = width
        self.height = height
        self.seed = seed
        self.algorithm = algorithm.upper()
        self.include_pattern = include_pattern
        self.maze: list[list[Cell]] | None = None
        self._pattern_cells: list[tuple[int, int]] = []

    def generate(
        self,
        entry: tuple[int, int] | None = None,
        on_step: Callable[[list[list[Cell]]], None] | None = None
    ) -> list[list[Cell]]:
        """Generate a new maze."""
        if entry is None:
            entry = (0, 0)

        if not (0 <= entry[0] < self.width and 0 <= entry[1] < self.height):
            raise ValueError(f"Entry {entry} out of bounds")

        if self.seed is not None:
            random.seed(self.seed)

        # Build config dict for algorithm functions
        config = {
            "WIDTH": self.width,
            "HEIGHT": self.height,
            "ENTRY": entry,
            "INCLUDE_PATTERN": self.include_pattern,
        }

        if self.algorithm == "KRUSKAL":
            self.maze = generate_kruskal(config, on_step)
        elif self.algorithm == "WILSON":
            self.maze = generate_wilson(config, on_step)
        else:
            self.maze = generate_dfs(config, on_step)

        # Compute pattern cells
        if self.maze:
            self._pattern_cells = where_is_ft_pattern(self.maze)

        return self.maze

    def solve(
        self,
        entry: tuple[int, int],
        exit_pos: tuple[int, int],
        on_step: Callable[
            [tuple[int, int], set[tuple[int, int]], set[tuple[int, int]], str],
            None
        ] | None = None
    ) -> str:
        """Find the shortest path using A* algorithm."""
        if self.maze is None:
            raise RuntimeError("Maze must be generated before solving")

        if not (0 <= entry[0] < self.width and 0 <= entry[1] < self.height):
            raise ValueError(f"Entry {entry} out of bounds")
        if not (0 <= exit_pos[0] < self.width and
                0 <= exit_pos[1] < self.height):
            raise ValueError(f"Exit {exit_pos} out of bounds")

        return a_star(entry, exit_pos, self.maze, on_step)

    def get_pattern_cells(self) -> list[tuple[int, int]]:
        """Get coordinates of the '42' pattern cells."""
        return self._pattern_cells.copy()

    def to_hex_string(self) -> str:
        """Convert maze to hexadecimal string format."""
        if self.maze is None:
            raise RuntimeError("Maze must be generated first")
        return "\n".join(
            "".join(str(cell) for cell in row) for row in self.maze
        )

    def get_cell(self, x: int, y: int) -> Cell:
        """Get cell at specified coordinates."""
        if self.maze is None:
            raise RuntimeError("Maze must be generated first")
        return self.maze[y][x]

    def reset(self) -> None:
        """Reset the generator."""
        self.maze = None
        self._pattern_cells = []
