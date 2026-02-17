from __future__ import annotations

import random

from src.a_maze_ing.algorithms.dfs import generate_dfs
from src.a_maze_ing.algorithms.ft_pattern import where_is_ft_pattern
from src.a_maze_ing.core.types import MazeConfig
from src.a_maze_ing.maze.flaw import flaw_maze
from tests.helpers import count_open_edges, has_fully_open_3x3


def test_imperfect_maze_has_cycles() -> None:
    config: MazeConfig = {
        "WIDTH": 21,
        "HEIGHT": 21,
        "ENTRY": (0, 0),
        "EXIT": (20, 20),
    }
    random.seed(2025)
    grid = generate_dfs(config)
    before = [[int(str(cell), 16) for cell in row] for row in grid]
    pattern_positions = set(where_is_ft_pattern(
        [[None] * 21 for _ in range(21)])
        )
    edges_before = count_open_edges(before, pattern_positions)
    nodes = 21 * 21 - len(pattern_positions)
    assert edges_before == nodes - 1

    flaw_maze(grid)
    after = [[int(str(cell), 16) for cell in row] for row in grid]
    edges_after = count_open_edges(after, pattern_positions)
    assert edges_after > edges_before
    assert not has_fully_open_3x3(after, pattern_positions)
