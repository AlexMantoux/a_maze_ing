*This project has been created as part of the 42 curriculum by trgascoi, amantoux.*

# A-Maze-ing

## Description
Maze generation project in Python. The program reads a configuration file, generates
a random maze (DFS or Kruskal), writes an output file in hexadecimal format, and
provides a terminal visualization (curses) with interactions. A "42" pattern is
embedded when the grid size allows it.

## Instructions

### Prerequisites
- Python 3.10+
- Poetry (for the environment)

### Installation
```bash
make install
```

### Run
```bash
python3 a_maze_ing.py config.txt
```

### Minimal config example
```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

### Full configuration file format
One line per key, `KEY=VALUE`. Lines starting with `#` are comments.

Mandatory keys:
- `WIDTH`: width (int)
- `HEIGHT`: height (int)
- `ENTRY`: entry coordinates `x,y`
- `EXIT`: exit coordinates `x,y`
- `OUTPUT_FILE`: output filename
- `PERFECT`: `True` or `False`

Optional keys:
- `ALGORITHM`: `DFS` or `KRUSKAL` (default `DFS`)
- `SEED`: integer for reproducibility
- `GUI`: `True` or `False` (default `False`)
- `ANIMATIONS`: `True` or `False` (default `True`)

## Maze generation algorithm
Two algorithms are available:
- **DFS (recursive backtracker)**: fast, simple, produces long winding corridors.
- **Kruskal**: generates a perfect maze using union-find.

Default choice: **DFS**, for its simple implementation and recognizable visual
style. Kruskal is available as an alternative.

## Output file
The maze is written in hexadecimal, one cell per character.
Bits: N=1, E=2, S=4, W=8. Each line represents a row of the grid.
After an empty line, the program writes:
1) entry coordinates
2) exit coordinates
3) shortest path using `N/E/S/W`

## Visualization
Terminal rendering via `curses`. Interactions:
- `r`: regenerate
- `p`: show/hide the shortest path
- `w`: change wall colors
- `f`: change the 42 pattern color
- `q`: quit

## Reusable module (mazegen)
The generation code can be exported as a Python package `mazegen` (see
`make bundle-mazegen` and `make build-package`). The module provides a
`MazeGenerator` class.

### Usage example
```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=20, height=15, seed=42, algorithm="DFS", perfect=True)
maze = gen.generate(entry=(0, 0))
path = gen.solve((0, 0), (19, 14))
hex_string = gen.to_hex_string()
```

Main features:
- custom parameters (size, seed, algorithm, perfect)
- access to the structure (cells, 42 pattern)
- solution via A*

## Team & project management
- Trgascoi
	- DFS & KRUSKAL
	- A*
	- GUI
	- Tests
	- Packaging
	- README

 - Amantoux
	- Parsing
	- Wilson
	- Flaw system
	- README

## Resources
- Depth-first search (DFS) maze generation
- Kruskal algorithm
- A* pathfinding
- Python curses documentation

### AI usage
- Used to make researches about the algorithms and libraries
- Used to find little errors that we had difficulty to find ourselves
- Used to create tests
