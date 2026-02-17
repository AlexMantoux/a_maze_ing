from __future__ import annotations

import random

import pytest

from src.a_maze_ing.algorithms.dfs import generate_dfs
from src.a_maze_ing.algorithms.kruskal import generate_kruskal
from src.a_maze_ing.algorithms.wilson import generate_wilson
from src.a_maze_ing.algorithms.ft_pattern import where_is_ft_pattern
from src.a_maze_ing.io.rendering import render_hex
from tests.helpers import (
    count_open_edges,
    degree,
    grid_bounds,
    has_fully_open_3x3,
    reachable_nodes,
    wall_closed,
)


@pytest.mark.parametrize("algorithm", ["DFS", "KRUSKAL", "WILSON"])
def test_reproducible_generation(algorithm: str) -> None:
    config = {
        "WIDTH": 15,
        "HEIGHT": 13,
        "ENTRY": (0, 0),
        "EXIT": (14, 12),
    }
    random.seed(4242)
    if algorithm == "DFS":
        grid_first = generate_dfs(config)
    elif algorithm == "KRUSKAL":
        grid_first = generate_kruskal(config)
    else:
        grid_first = generate_wilson(config)
    first = render_hex(grid_first)

    random.seed(4242)
    if algorithm == "DFS":
        grid_second = generate_dfs(config)
    elif algorithm == "KRUSKAL":
        grid_second = generate_kruskal(config)
    else:
        grid_second = generate_wilson(config)
    second = render_hex(grid_second)

    assert first == second


@pytest.mark.parametrize("algorithm", ["DFS", "KRUSKAL", "WILSON"])
def test_maze_validity_and_structure(algorithm: str) -> None:
    config = {
        "WIDTH": 19,
        "HEIGHT": 17,
        "ENTRY": (0, 0),
        "EXIT": (18, 16),
    }
    random.seed(1337)
    if algorithm == "DFS":
        grid = generate_dfs(config)
    elif algorithm == "KRUSKAL":
        grid = generate_kruskal(config)
    else:
        grid = generate_wilson(config)

    hex_grid = [[int(str(cell), 16) for cell in row] for row in grid]
    width, height = grid_bounds(hex_grid)
    pattern_positions = set(where_is_ft_pattern(
        [[None] * width for _ in range(height)])
        )

    for x in range(width):
        assert wall_closed(hex_grid[0][x], "N")
        assert wall_closed(hex_grid[height - 1][x], "S")
    for y in range(height):
        assert wall_closed(hex_grid[y][0], "W")
        assert wall_closed(hex_grid[y][width - 1], "E")

    for y in range(height):
        for x in range(width):
            if y > 0:
                assert wall_closed(
                    hex_grid[y][x],
                    "N"
                    ) == wall_closed(
                        hex_grid[y - 1][x],
                        "S"
                        )
            if y < height - 1:
                assert wall_closed(
                    hex_grid[y][x],
                    "S"
                    ) == wall_closed(
                        hex_grid[y + 1][x],
                        "N"
                        )
            if x > 0:
                assert wall_closed(
                    hex_grid[y][x],
                    "W"
                    ) == wall_closed(
                        hex_grid[y][x - 1],
                        "E"
                        )
            if x < width - 1:
                assert wall_closed(
                    hex_grid[y][x],
                    "E"
                    ) == wall_closed(
                        hex_grid[y][x + 1],
                        "W"
                        )

    assert pattern_positions, "Pattern should be present at this size."
    for x, y in pattern_positions:
        assert hex_grid[y][x] == 0xF

    for y in range(height):
        for x in range(width):
            if (x, y) in pattern_positions:
                continue
            assert degree(hex_grid, x, y, pattern_positions) > 0

    reachable = reachable_nodes(hex_grid, config["ENTRY"], pattern_positions)
    assert config["EXIT"] in reachable
    total_nodes = width * height - len(pattern_positions)
    assert len(reachable) == total_nodes

    edges = count_open_edges(hex_grid, pattern_positions)
    assert edges == total_nodes - 1

    assert not has_fully_open_3x3(hex_grid, pattern_positions)
