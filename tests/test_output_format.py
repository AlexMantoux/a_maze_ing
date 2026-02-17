from __future__ import annotations

from pathlib import Path

import pytest

from a_maze_ing import main
from tests.helpers import bfs_distance, grid_bounds
from tests.helpers import parse_output_file, path_is_valid, write_config


def test_output_file_format_and_path_validity(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_path = tmp_path / "maze_output.txt"
    config_path = write_config(
        tmp_path,
        width=15,
        height=11,
        entry=(0, 0),
        exit_pos=(14, 10),
        output_file=output_path,
        perfect=True,
        seed=4242,
        algorithm="DFS",
    )

    monkeypatch.setenv("PYTHONHASHSEED", "0")
    monkeypatch.setattr("sys.argv", ["a_maze_ing.py", str(config_path)])
    assert main() == 0
    assert output_path.exists()

    grid, entry, exit_pos, path = parse_output_file(output_path)
    width, height = grid_bounds(grid)
    assert (width, height) == (15, 11)

    for row in output_path.read_text(encoding="utf-8").splitlines():
        if row.strip() == "":
            break
        assert row.strip().upper() == row.strip()

    assert entry == (0, 0)
    assert exit_pos == (14, 10)
    assert path, "Shortest path must not be empty."
    assert path_is_valid(grid, entry, exit_pos, path)

    shortest = bfs_distance(grid, entry, exit_pos)
    assert shortest is not None
    assert len(path) == shortest
