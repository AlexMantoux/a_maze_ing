from collections.abc import Callable
from random import shuffle as random_shuffle
from src.a_maze_ing.core.cell import Cell, CellState
from src.a_maze_ing.algorithms.grid_utils import (
    generate_full_grid,
    remove_walls_between
)


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

    grid, _ = generate_full_grid(width, height)
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
            remove_walls_between(cell1, cell2)
            if on_step:
                on_step(grid)

    return grid
