from __future__ import annotations

from collections import deque
from pathlib import Path


def write_config(
    tmp_path: Path,
    *,
    width: int,
    height: int,
    entry: tuple[int, int],
    exit_pos: tuple[int, int],
    output_file: Path,
    perfect: bool,
    seed: int,
    algorithm: str = "DFS",
    gui: bool = False,
    animations: bool = False,
) -> Path:
    lines = [
        f"WIDTH={width}",
        f"HEIGHT={height}",
        f"ENTRY={entry[0]},{entry[1]}",
        f"EXIT={exit_pos[0]},{exit_pos[1]}",
        f"OUTPUT_FILE={output_file}",
        f"PERFECT={'True' if perfect else 'False'}",
        f"SEED={seed}",
        f"ALGORITHM={algorithm}",
        f"GUI={'True' if gui else 'False'}",
        f"ANIMATIONS={'True' if animations else 'False'}",
    ]
    config_path = tmp_path / "config.txt"
    config_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return config_path


def parse_output_file(
    path: Path,
) -> tuple[list[list[int]], tuple[int, int], tuple[int, int], str]:
    raw = path.read_text(encoding="utf-8")
    assert raw.endswith("\n"), "Output file must end with a newline."
    parts = raw.split("\n\n")
    assert len(parts) == 2, "Output file must contain a single blank line separator."
    grid_part, trailer_part = parts
    grid_lines = grid_part.splitlines()
    trailer_lines = trailer_part.splitlines()
    assert len(trailer_lines) == 3, "Output file must have 3 trailer lines."

    grid = [[int(c, 16) for c in line.strip()] for line in grid_lines]
    entry_str, exit_str, path_str = trailer_lines
    entry = tuple(int(v) for v in entry_str.split(","))
    exit_pos = tuple(int(v) for v in exit_str.split(","))
    return grid, entry, exit_pos, path_str


def wall_closed(value: int, direction: str) -> bool:
    direction = direction.upper()
    if direction == "N":
        return bool(value & 1)
    if direction == "E":
        return bool(value & 2)
    if direction == "S":
        return bool(value & 4)
    if direction == "W":
        return bool(value & 8)
    raise ValueError(f"Unknown direction {direction}")


def grid_bounds(grid: list[list[int]]) -> tuple[int, int]:
    return len(grid[0]), len(grid)


def open_neighbors(grid: list[list[int]], x: int, y: int) -> list[tuple[int, int]]:
    width, height = grid_bounds(grid)
    value = grid[y][x]
    neighbors: list[tuple[int, int]] = []
    if y > 0 and not wall_closed(value, "N"):
        neighbors.append((x, y - 1))
    if y < height - 1 and not wall_closed(value, "S"):
        neighbors.append((x, y + 1))
    if x > 0 and not wall_closed(value, "W"):
        neighbors.append((x - 1, y))
    if x < width - 1 and not wall_closed(value, "E"):
        neighbors.append((x + 1, y))
    return neighbors


def reachable_nodes(
    grid: list[list[int]],
    start: tuple[int, int],
    blocked: set[tuple[int, int]],
) -> set[tuple[int, int]]:
    if start in blocked:
        return set()
    queue = deque([start])
    visited = {start}
    while queue:
        x, y = queue.popleft()
        for nx, ny in open_neighbors(grid, x, y):
            if (nx, ny) in blocked or (nx, ny) in visited:
                continue
            visited.add((nx, ny))
            queue.append((nx, ny))
    return visited


def count_open_edges(grid: list[list[int]], blocked: set[tuple[int, int]]) -> int:
    width, height = grid_bounds(grid)
    edges = 0
    for y in range(height):
        for x in range(width):
            if (x, y) in blocked:
                continue
            value = grid[y][x]
            if x + 1 < width and (x + 1, y) not in blocked and not wall_closed(value, "E"):
                edges += 1
            if y + 1 < height and (x, y + 1) not in blocked and not wall_closed(value, "S"):
                edges += 1
    return edges


def degree(grid: list[list[int]], x: int, y: int, blocked: set[tuple[int, int]]) -> int:
    if (x, y) in blocked:
        return 0
    return sum((nx, ny) not in blocked for nx, ny in open_neighbors(grid, x, y))


def bfs_distance(
    grid: list[list[int]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> int | None:
    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        (x, y), dist = queue.popleft()
        if (x, y) == goal:
            return dist
        for nx, ny in open_neighbors(grid, x, y):
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), dist + 1))
    return None


def path_is_valid(
    grid: list[list[int]],
    entry: tuple[int, int],
    exit_pos: tuple[int, int],
    path: str,
) -> bool:
    x, y = entry
    width, height = grid_bounds(grid)
    for step in path:
        if step not in {"N", "E", "S", "W"}:
            return False
        if step == "N":
            if y == 0 or wall_closed(grid[y][x], "N"):
                return False
            y -= 1
        elif step == "S":
            if y >= height - 1 or wall_closed(grid[y][x], "S"):
                return False
            y += 1
        elif step == "W":
            if x == 0 or wall_closed(grid[y][x], "W"):
                return False
            x -= 1
        elif step == "E":
            if x >= width - 1 or wall_closed(grid[y][x], "E"):
                return False
            x += 1
    return (x, y) == exit_pos


def has_fully_open_3x3(grid: list[list[int]], blocked: set[tuple[int, int]]) -> bool:
    width, height = grid_bounds(grid)
    for top_y in range(height - 2):
        for top_x in range(width - 2):
            cells = {
                (top_x + dx, top_y + dy)
                for dy in range(3)
                for dx in range(3)
            }
            if cells & blocked:
                continue
            fully_open = True
            for dy in range(3):
                for dx in range(3):
                    x = top_x + dx
                    y = top_y + dy
                    if dx < 2 and wall_closed(grid[y][x], "E"):
                        fully_open = False
                        break
                    if dy < 2 and wall_closed(grid[y][x], "S"):
                        fully_open = False
                        break
                if not fully_open:
                    break
            if fully_open:
                return True
    return False
