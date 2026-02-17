from __future__ import annotations

from pathlib import Path

import pytest

from a_maze_ing import main
from src.a_maze_ing.algorithms.ft_pattern import where_is_ft_pattern
from tests.helpers import write_config


def test_cli_no_args_returns_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr("sys.argv", ["a_maze_ing.py"])
    assert main() == 1
    out = capsys.readouterr().out
    assert "No config file provided" in out


def test_cli_missing_file_returns_error(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr("sys.argv", ["a_maze_ing.py", "missing_config.txt"])
    assert main() == 1
    out = capsys.readouterr().out
    assert "Config file not found" in out


def test_entry_overlaps_pattern_is_rejected(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output_path = tmp_path / "maze_output.txt"
    width, height = 19, 19
    pattern_positions = where_is_ft_pattern(
        [[None] * width for _ in range(height)]
        )
    entry = pattern_positions[0]
    config_path = write_config(
        tmp_path,
        width=width,
        height=height,
        entry=entry,
        exit_pos=(18, 18),
        output_file=output_path,
        perfect=True,
        seed=123,
        algorithm="DFS",
    )

    monkeypatch.setattr("sys.argv", ["a_maze_ing.py", str(config_path)])
    assert main() == 1
