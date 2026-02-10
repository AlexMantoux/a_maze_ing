"""Entry point for the A-Maze-ing project."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import cast

from src.a_maze_ing.algorithms.a_star import a_star
from src.a_maze_ing.parsing import check_config_mandatory
from src.a_maze_ing.parsing import parse_config
from src.a_maze_ing.algorithms.dfs import generate_dfs
from src.a_maze_ing.rendering import render_hex


def main() -> int:
    """Run the CLI entry point for the project."""
    parser = argparse.ArgumentParser(prog="a_maze_ing")
    parser.add_argument(
        "config",
        nargs="?",
        help="Path to the maze configuration file",
    )
    args = parser.parse_args()
    if not args.config:
        print("No config file provided. "
              "Usage: python a_maze_ing.py [CONFIG_FILE].")
        return 1

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Config file not found: {config_path}")
        return 1

    try:
        config = parse_config(str(config_path))
        check_config_mandatory(config)
        # After validation, we know all required values are present and valid
        validated_config = cast(
            dict[str, int | tuple[int, int] | str | bool],
            config
        )

        maze = generate_dfs(validated_config)

        output_file = validated_config["OUTPUT_FILE"]
        assert isinstance(output_file, str)
        entry = validated_config["ENTRY"]
        assert isinstance(entry, tuple)
        exit_pos = validated_config["EXIT"]
        assert isinstance(exit_pos, tuple)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(render_hex(maze))

            f.write("\n\n")

            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit_pos[0]},{exit_pos[1]}\n")
            f.write(f"{a_star(entry, exit_pos, maze)}\n")
    except OSError as e:
        print(f"Error when writing into file : {e}")
    except Exception as e:
        print(e)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
