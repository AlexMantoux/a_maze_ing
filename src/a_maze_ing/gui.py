from curses import wrapper, init_pair, init_color, error
from curses import start_color, color_pair
from curses import COLOR_GREEN, COLOR_BLACK
from src.a_maze_ing.cell import Cell
from src.a_maze_ing.algorithms.dfs import generate_dfs
from src.a_maze_ing.algorithms.ft_pattern import where_is_ft_pattern


class GUI():
	def __init__(self, config: dict) -> None:
		self.config = config
		wrapper(self.__main)

	def __main(self, stdscr):
		start_color()
		init_color(10, 1000, 1000, 1000)
		init_color(11, 500, 500, 500)
		init_pair(1, COLOR_GREEN, COLOR_BLACK)
		init_pair(2, 10, COLOR_BLACK)
		init_pair(3, 10, 11)
		stdscr.bkgd(' ', color_pair(2))
		stdscr.clear()

		maze = generate_dfs(self.config)
		self.ft_pattern = where_is_ft_pattern(maze)
		rows = len(maze)
		cols = len(maze[0]) if rows > 0 else 0

		for y, row in enumerate(maze):
			for x, cell in enumerate(row):
				self.__draw_cell_structured(stdscr, x, y, cell, rows, cols)

		stdscr.refresh()
		stdscr.getch()

	def __safe_add(self, stdscr, y, x, text, cp):
		try:
			stdscr.addstr(y, x, text, cp)
		except error:
			pass

	def __draw_cell_structured(self, stdscr, x, y, cell: Cell, max_y, max_x):
		yy, xx = y * 2, x * 4
		cp = color_pair(3) if (x, y) in self.ft_pattern else color_pair(2)
		
		# Top-left corner of the cell
		self.__safe_add(stdscr, yy, xx, "█", cp)
		
		# NORTH wall (top horizontal line)
		self.__safe_add(stdscr, yy, xx + 1, "███" if cell.north else "   ", cp)
		
		# WEST wall (left vertical line)
		self.__safe_add(stdscr, yy + 1, xx, "█" if cell.west else " ", cp)
		
		# Interior space of the cell
		self.__safe_add(stdscr, yy + 1, xx + 1, "   ", cp)
		
		# If we're at the last column, draw the right edge of the maze
		if x == max_x - 1:
			# Top-right corner
			self.__safe_add(stdscr, yy, xx + 4, "█", cp)
			# EAST wall (right vertical line)
			self.__safe_add(stdscr, yy + 1, xx + 4, "█" if cell.east else " ", cp)
		
		# If we're at the last row, draw the bottom edge of the maze
		if y == max_y - 1:
			# Bottom-left corner
			self.__safe_add(stdscr, yy + 2, xx, "█", cp)
			# SOUTH wall (bottom horizontal line)
			self.__safe_add(stdscr, yy + 2, xx + 1, "███" if cell.south else "   ", cp)
			# If we're at the bottom-right corner of the maze
			if x == max_x - 1:
				# Bottom-right corner
				self.__safe_add(stdscr, yy + 2, xx + 4, "█", cp)