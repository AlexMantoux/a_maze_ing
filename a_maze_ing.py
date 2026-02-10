"""Entry point for the A-Maze-ing project."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.a_maze_ing.parsing import check_config_mandatory
from src.a_maze_ing.parsing import parse_config
from src.a_maze_ing.algorithms.dfs import generate_dfs


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
        config = parse_config(str(config_path))
        check_config_mandatory(config)
        print(config)
        
        maze = generate_dfs(config)
        for row in maze:
            print("".join(str(cell) for cell in row))
    except Exception as e:
        print(e)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
