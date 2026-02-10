"""Entry point for the A-Maze-ing project."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.a_maze_ing.parsing import parse_config


def main() -> int:
    """Run the CLI entry point for the project."""
    parser = argparse.ArgumentParser(prog="a_maze_ing")
    parser.add_argument(
        "config",
        nargs="?",
        default="config.txt",
        help="Path to the maze configuration file",
    )
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Config file not found: {config_path}")
        return 1

    try:
        print(parse_config(str(config_path)))
    except Exception as e:
        print(e)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
