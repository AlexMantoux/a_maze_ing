from __future__ import annotations

import random

from src.a_maze_ing.algorithms.a_star import a_star
from src.a_maze_ing.algorithms.dfs import generate_dfs
from tests.helpers import bfs_distance


def test_a_star_matches_shortest_path() -> None:
    config: dict[str, int | tuple[int, int]] = {
        "WIDTH": 13,
        "HEIGHT": 9,
        "ENTRY": (0, 0),
        "EXIT": (12, 8),
    }
    random.seed(777)
    grid = generate_dfs(config)
    entry = config["ENTRY"]
    exit_pos = config["EXIT"]
    assert isinstance(entry, tuple)
    assert isinstance(exit_pos, tuple)
    path = a_star(entry, exit_pos, grid)
    hex_grid = [[int(str(cell), 16) for cell in row] for row in grid]
    shortest = bfs_distance(hex_grid, entry, exit_pos)
    assert shortest is not None
    assert len(path) == shortest
