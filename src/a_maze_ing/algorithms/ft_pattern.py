"""42 pattern placement for maze generation."""

from collections.abc import Sequence

_FT_PATTERN = [
    [1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1]
]

_FT_PATTERN_WARNED = False


def where_is_ft_pattern(
    grid: Sequence[Sequence[object]]
) -> list[tuple[int, int]]:
    """Compute the coordinates for the fixed '42' pattern.

    Args:
        grid: 2D maze grid.

    Returns:
        List of coordinates to mark as the 42 pattern. Empty if too small.
    """
    if len(grid) < 7 or len(grid[0]) < 9:
        global _FT_PATTERN_WARNED
        if not _FT_PATTERN_WARNED:
            print("Error: Maze too small for '42' pattern, skipping pattern.")
            _FT_PATTERN_WARNED = True
        return []
    result = []
    pattern_top_left = (len(grid[0]) / 2 - 3, len(grid) / 2 - 2)
    for y in range(len(_FT_PATTERN)):
        for x in range(len(_FT_PATTERN[y])):
            top_left_x, top_left_y = pattern_top_left
            if _FT_PATTERN[y][x] == 1:
                result.append((int(top_left_x + x), int(top_left_y + y)))
    return result
