"""ASCII rendering for mazes."""

from src.a_maze_ing.cell import Cell

# ANSI color codes
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_RESET = "\033[0m"


def render_ascii(
    grid: list[list[Cell]],
    entry: tuple[int, int] | None = None,
    exit_point: tuple[int, int] | None = None
) -> str:
    """
    Render a maze grid as ASCII art.

    Each cell is represented as:
    +---+
    |   |
    +---+

    Where walls are drawn based on the cell's wall attributes.
    Entry point is displayed in green, exit point in red.
    """
    if not grid or not grid[0]:
        return ""

    height = len(grid)
    width = len(grid[0])
    lines = []

    for y in range(height):
        # Top line of the row (north walls)
        top_line = ""
        for x in range(width):
            cell = grid[y][x]
            top_line += "+"
            top_line += "---" if cell.north else "   "
        top_line += "+"
        lines.append(top_line)

        # Middle line of the row (west/east walls and cell content)
        mid_line = ""
        for x in range(width):
            cell = grid[y][x]
            mid_line += "|" if cell.west else " "
            # Cell content with color for entry/exit
            if entry and (x, y) == entry:
                mid_line += f"{COLOR_GREEN} S {COLOR_RESET}"
            elif exit_point and (x, y) == exit_point:
                mid_line += f"{COLOR_RED} E {COLOR_RESET}"
            else:
                mid_line += "   "
        # Last east wall
        mid_line += "|" if grid[y][width - 1].east else " "
        lines.append(mid_line)

    # Bottom line (south walls of last row)
    bottom_line = ""
    for x in range(width):
        cell = grid[height - 1][x]
        bottom_line += "+"
        bottom_line += "---" if cell.south else "   "
    bottom_line += "+"
    lines.append(bottom_line)

    return "\n".join(lines)


def render_hex(grid: list[list[Cell]]) -> str:
    """
    Render a maze grid as hexadecimal values.

    Each cell is displayed as its hex representation based on walls
    """
    if not grid or not grid[0]:
        return ""

    lines = []
    for row in grid:
        lines.append("".join(str(cell) for cell in row))

    return "\n".join(lines)
