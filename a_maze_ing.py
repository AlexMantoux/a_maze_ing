"""Entry point for the A-Maze-ing project."""

from __future__ import annotations

import argparse
import random
from pathlib import Path
from typing import cast

from src.a_maze_ing.parsing import check_config_mandatory
from src.a_maze_ing.parsing import parse_config
from src.a_maze_ing.algorithms.dfs import generate_dfs
from src.a_maze_ing.algorithms.kruskal import generate_kruskal
from src.a_maze_ing.algorithms.ft_pattern import where_is_ft_pattern
from src.a_maze_ing.output import write_output_file
from src.a_maze_ing.parsing import ParsingError


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

        gui_enabled = bool(validated_config.get("GUI", False))
        animations_enabled = bool(validated_config.get("ANIMATIONS", True))
        seed = None
        if gui_enabled and animations_enabled:
            seed = random.randrange(2**32)
            random.seed(seed)

        algorithm = validated_config.get("ALGORITHM", "DFS")
        assert isinstance(algorithm, str)
        if algorithm.upper() == "KRUSKAL":
            maze = generate_kruskal(validated_config)
        else:
            maze = generate_dfs(validated_config)
        ft_pattern = where_is_ft_pattern(maze)
        if validated_config["ENTRY"] in ft_pattern:
            raise ParsingError("Entry overlaps the 42 pattern.")
        if validated_config["EXIT"] in ft_pattern:
            raise ParsingError("Exit overlaps the 42 pattern.")

        output_file = validated_config["OUTPUT_FILE"]
        assert isinstance(output_file, str)
        entry = validated_config["ENTRY"]
        assert isinstance(entry, tuple)
        exit_pos = validated_config["EXIT"]
        assert isinstance(exit_pos, tuple)

        write_output_file(output_file, maze, entry, exit_pos)

        if gui_enabled:
            from src.a_maze_ing.gui import GUI

            gui_maze = None if animations_enabled else maze
            GUI(validated_config, maze=gui_maze, seed=seed)
    except OSError as e:
        print(f"Error when writing into file : {e}")
    except Exception as e:
        print(e)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())