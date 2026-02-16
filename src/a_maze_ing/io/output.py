from src.a_maze_ing.algorithms.a_star import a_star
from src.a_maze_ing.core.cell import Cell
from src.a_maze_ing.io.rendering import render_hex


def write_output_file(
    output_file: str,
    maze: list[list[Cell]],
    entry: tuple[int, int],
    exit_pos: tuple[int, int],
    path: str | None = None
) -> None:
    if path is None:
        path = a_star(entry, exit_pos, maze)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(render_hex(maze))
        f.write("\n\n")
        f.write(f"{entry[0]},{entry[1]}\n")
        f.write(f"{exit_pos[0]},{exit_pos[1]}\n")
        f.write(f"{path}\n")
