from heapq import heappush, heappop
from src.a_maze_ing.cell import Cell


def _manhattan_distance(pos: tuple[int, int], goal: tuple[int, int]) -> int:
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])


def _get_accessible_neighbors(cell: Cell, grid: list[list[Cell]]) -> list[tuple[Cell, str]]:
    x, y = cell.coordinates
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    neighbors = []

    if not cell.north and y > 0:
        neighbors.append((grid[y - 1][x], 'N'))
    if not cell.south and y < height - 1:
        neighbors.append((grid[y + 1][x], 'S'))
    if not cell.west and x > 0:
        neighbors.append((grid[y][x - 1], 'W'))
    if not cell.east and x < width - 1:
        neighbors.append((grid[y][x + 1], 'E'))

    return neighbors


def a_star(entry: tuple[int, int], exit: tuple[int, int], grid: list[list[Cell]]) -> str:
    if not grid or not grid[0]:
        return ""
    
    counter = 0
    open_set = []
    heappush(open_set, (0, counter, entry, ""))
    
    g_score = {entry: 0}
    
    closed_set = set()
    
    while open_set:
        _, _, current_pos, path = heappop(open_set)
        
        if current_pos == exit:
            return path
        
        if current_pos in closed_set:
            continue
        closed_set.add(current_pos)
        
        current_x, current_y = current_pos
        current_cell = grid[current_y][current_x]
        
        for neighbor_cell, direction in _get_accessible_neighbors(current_cell, grid):
            neighbor_pos = neighbor_cell.coordinates
            
            if neighbor_pos in closed_set:
                continue
            
            tentative_g = g_score[current_pos] + 1
            
            if neighbor_pos not in g_score or tentative_g < g_score[neighbor_pos]:
                g_score[neighbor_pos] = tentative_g
                f_score = tentative_g + _manhattan_distance(neighbor_pos, exit)
                counter += 1
                heappush(open_set, (f_score, counter, neighbor_pos, path + direction))
    
    return ""
