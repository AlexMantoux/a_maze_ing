from __future__ import annotations

from pathlib import Path

import pytest

from src.a_maze_ing.core.parsing import ParsingError
from src.a_maze_ing.core.parsing import check_config_mandatory, parse_config


def _write_raw_config(tmp_path: Path, lines: list[str]) -> Path:
    config_path = tmp_path / "config.txt"
    config_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return config_path


def test_default_config_exists_and_valid() -> None:
    config_path = Path("config.txt")
    assert config_path.exists()
    config = parse_config(str(config_path))
    check_config_mandatory(config)


def test_comments_and_blank_lines_are_ignored(tmp_path: Path) -> None:
    config_path = _write_raw_config(
        tmp_path,
        [
            "# comment",
            "",
            "WIDTH=5",
            "HEIGHT=5",
            "ENTRY=0,0",
            "EXIT=4,4",
            "OUTPUT_FILE=maze.txt",
            "PERFECT=True",
        ],
    )
    config = parse_config(str(config_path))
    check_config_mandatory(config)
    assert config["WIDTH"] == 5


def test_invalid_line_format_is_rejected(tmp_path: Path) -> None:
    config_path = _write_raw_config(tmp_path, ["WIDTH:5"])
    with pytest.raises(ParsingError):
        parse_config(str(config_path))

    config_path = _write_raw_config(tmp_path, ["WIDTH=5=7"])
    with pytest.raises(ParsingError):
        parse_config(str(config_path))


def test_invalid_key_is_rejected(tmp_path: Path) -> None:
    config_path = _write_raw_config(tmp_path, ["FOO=5"])
    with pytest.raises(ParsingError):
        parse_config(str(config_path))


def test_invalid_tuple_is_rejected(tmp_path: Path) -> None:
    config_path = _write_raw_config(
        tmp_path,
        [
            "WIDTH=5",
            "HEIGHT=5",
            "ENTRY=0;0",
            "EXIT=4,4",
            "OUTPUT_FILE=maze.txt",
            "PERFECT=True",
        ],
    )
    with pytest.raises(ParsingError):
        parse_config(str(config_path))


def test_invalid_bool_is_rejected(tmp_path: Path) -> None:
    config_path = _write_raw_config(
        tmp_path,
        [
            "WIDTH=5",
            "HEIGHT=5",
            "ENTRY=0,0",
            "EXIT=4,4",
            "OUTPUT_FILE=maze.txt",
            "PERFECT=true",
        ],
    )
    with pytest.raises(ParsingError):
        parse_config(str(config_path))


def test_invalid_algorithm_is_rejected(tmp_path: Path) -> None:
    config_path = _write_raw_config(
        tmp_path,
        [
            "WIDTH=5",
            "HEIGHT=5",
            "ENTRY=0,0",
            "EXIT=4,4",
            "OUTPUT_FILE=maze.txt",
            "PERFECT=True",
            "ALGORITHM=NOPE",
        ],
    )
    with pytest.raises(ParsingError):
        parse_config(str(config_path))


def test_entry_exit_checks(tmp_path: Path) -> None:
    config_path = _write_raw_config(
        tmp_path,
        [
            "WIDTH=5",
            "HEIGHT=5",
            "ENTRY=1,1",
            "EXIT=1,1",
            "OUTPUT_FILE=maze.txt",
            "PERFECT=True",
        ],
    )
    with pytest.raises(ParsingError):
        parse_config(str(config_path))

    config_path = _write_raw_config(
        tmp_path,
        [
            "WIDTH=5",
            "HEIGHT=5",
            "ENTRY=5,0",
            "EXIT=4,4",
            "OUTPUT_FILE=maze.txt",
            "PERFECT=True",
        ],
    )
    with pytest.raises(ParsingError):
        parse_config(str(config_path))

    config_path = _write_raw_config(
        tmp_path,
        [
            "WIDTH=5",
            "HEIGHT=5",
            "ENTRY=0,0",
            "EXIT=4,5",
            "OUTPUT_FILE=maze.txt",
            "PERFECT=True",
        ],
    )
    with pytest.raises(ParsingError):
        parse_config(str(config_path))


def test_missing_mandatory_key_is_rejected(tmp_path: Path) -> None:
    config_path = _write_raw_config(
        tmp_path,
        [
            "WIDTH=5",
            "HEIGHT=5",
            "ENTRY=0,0",
            "EXIT=4,4",
        ],
    )
    config = parse_config(str(config_path))
    with pytest.raises(ParsingError):
        check_config_mandatory(config)
