from __future__ import annotations

import random

import pytest

from src.a_maze_ing.algorithms.dfs import generate_dfs
from src.a_maze_ing.core.types import MazeConfig


def test_small_maze_prints_pattern_warning(
    capsys: pytest.CaptureFixture[str],
) -> None:
    import src.a_maze_ing.algorithms.ft_pattern as ft_pattern

    ft_pattern._FT_PATTERN_WARNED = False
    config: MazeConfig = {
        "WIDTH": 5,
        "HEIGHT": 5,
        "ENTRY": (0, 0),
        "EXIT": (4, 4),
    }
    random.seed(123)
    generate_dfs(config)
    out = capsys.readouterr().out
    assert "Maze too small" in out
