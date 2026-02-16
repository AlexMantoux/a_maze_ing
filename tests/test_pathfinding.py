from __future__ import annotations

import random

from src.a_maze_ing.algorithms.a_star import a_star
from src.a_maze_ing.algorithms.dfs import generate_dfs
from tests.helpers import bfs_distance


def test_a_star_matches_shortest_path() -> None:
    config = {
        "WIDTH": 13,
        "HEIGHT": 9,
        "ENTRY": (0, 0),
        "EXIT": (12, 8),
    }
    random.seed(777)
    grid = generate_dfs(config)
    path = a_star(config["ENTRY"], config["EXIT"], grid)
    hex_grid = [[int(str(cell), 16) for cell in row] for row in grid]
    shortest = bfs_distance(hex_grid, config["ENTRY"], config["EXIT"])
    assert shortest is not None
    assert len(path) == shortest
