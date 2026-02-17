# mazegen

Reusable maze generation module extracted from the A-Maze-ing project.

## Quick start
```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=20, height=15, seed=42, algorithm="DFS")
maze = gen.generate(entry=(0, 0))
path = gen.solve((0, 0), (19, 14))
hex_string = gen.to_hex_string()
```

## Usage
- `MazeGenerator(width, height, seed, algorithm, perfect)`
- `generate(entry=(0, 0), on_step=None)` returns the maze grid
- `solve(entry, exit_pos, on_step=None)` returns the shortest path as `N/E/S/W`
- `to_hex_string()` returns the maze in hex row format
- `get_pattern_cells()` returns the "42" pattern coordinates (if enabled)

## Notes
- Supported algorithms: `DFS`, `KRUSKAL`
- The generated structure is a grid of `Cell` objects
