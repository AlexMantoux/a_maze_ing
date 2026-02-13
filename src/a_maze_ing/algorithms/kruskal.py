from collections.abc import Callable
from random import shuffle as random_shuffle
from src.a_maze_ing.cell import Cell, CellState
from src.a_maze_ing.algorithms.ft_pattern import where_is_ft_pattern


def _generate_full_grid(width: int, height: int) -> list[list[Cell]]:
    grid = [
        [
            Cell(
                CellState.UNVISITED,
                True, True, True, True,
                (x, y)
            ) for x in range(width)
        ] for y in range(height)
    ]
    for x, y in where_is_ft_pattern(grid):
        grid[y][x].state = CellState.VISITED
    return grid


def _remove_walls_between(cell1: Cell, cell2: Cell) -> None:
    """
    Removes the walls between two adjacent cells.
    """
    x1, y1 = cell1.coordinates
    x2, y2 = cell2.coordinates

    if x1 == x2:
        if y2 < y1:
            cell1.north = False
            cell2.south = False
        else:
            cell1.south = False
            cell2.north = False

    elif y1 == y2:
        if x2 < x1:
            cell1.west = False
            cell2.east = False
        else:
            cell1.east = False
            cell2.west = False


class _DisjointSet:
    def __init__(self, items: list[tuple[int, int]]) -> None:
        self.parent = {item: item for item in items}
        self.rank = {item: 0 for item in items}

    def find(self, item: tuple[int, int]) -> tuple[int, int]:
        parent = self.parent[item]
        if parent != item:
            self.parent[item] = self.find(parent)
        return self.parent[item]

    def union(self, a: tuple[int, int], b: tuple[int, int]) -> bool:
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            return False
        rank_a = self.rank[root_a]
        rank_b = self.rank[root_b]
        if rank_a < rank_b:
            self.parent[root_a] = root_b
        elif rank_a > rank_b:
            self.parent[root_b] = root_a
        else:
            self.parent[root_b] = root_a
            self.rank[root_a] += 1
        return True


def _get_edges(grid: list[list[Cell]]) -> list[tuple[Cell, Cell]]:
    edges: list[tuple[Cell, Cell]] = []
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    for y in range(height):
        for x in range(width):
            cell = grid[y][x]
            if cell.state == CellState.VISITED:
                continue
            if y + 1 < height:
                neighbor = grid[y + 1][x]
                if neighbor.state != CellState.VISITED:
                    edges.append((cell, neighbor))
            if x + 1 < width:
                neighbor = grid[y][x + 1]
                if neighbor.state != CellState.VISITED:
                    edges.append((cell, neighbor))

    return edges


def generate_kruskal(
        config: dict[str, object],
        on_step: Callable[[list[list[Cell]]], None] | None = None
) -> list[list[Cell]]:
    width = config["WIDTH"]
    height = config["HEIGHT"]
    assert isinstance(width, int)
    assert isinstance(height, int)

    grid = _generate_full_grid(width, height)
    edges = _get_edges(grid)
    random_shuffle(edges)

    items = [
        cell.coordinates
        for row in grid
        for cell in row
        if cell.state != CellState.VISITED
    ]
    disjoint_set = _DisjointSet(items)

    if on_step:
        on_step(grid)

    for cell1, cell2 in edges:
        if disjoint_set.union(cell1.coordinates, cell2.coordinates):
            _remove_walls_between(cell1, cell2)
            if on_step:
                on_step(grid)

    return grid
