import curses
import random
import time
from curses import wrapper, init_pair, init_color, error
from curses import start_color, color_pair, use_default_colors, curs_set
from curses import can_change_color
from curses import COLOR_BLACK, COLOR_BLUE, COLOR_CYAN, COLOR_GREEN
from curses import COLOR_MAGENTA, COLOR_RED, COLOR_WHITE, COLOR_YELLOW
from src.a_maze_ing.core.cell import Cell
from src.a_maze_ing.algorithms.dfs import generate_dfs
from src.a_maze_ing.algorithms.kruskal import generate_kruskal
from src.a_maze_ing.algorithms.wilson import generate_wilson
from src.a_maze_ing.algorithms.ft_pattern import where_is_ft_pattern
from src.a_maze_ing.algorithms.a_star import a_star
from src.a_maze_ing.io.output import write_output_file
from src.a_maze_ing.maze.flaw import flaw_maze
from typing import Callable


class GUI:
    def __init__(
        self,
        config: dict,
        maze: list[list[Cell]] | None = None,
        seed: int | None = None
    ) -> None:
        self.config = config
        self.initial_maze = maze
        self.initial_seed = seed
        self.animations_enabled = bool(self.config.get("ANIMATIONS", True))
        self.animation_delay = 0.01
        self.path_animation_delay = 0.01
        wrapper(self.__main)

    def __main(self, stdscr: curses.window) -> None:
        start_color()
        use_default_colors()
        self.gray_bg = COLOR_BLACK
        colors_count = getattr(curses, "COLORS", 0)
        if can_change_color() and colors_count >= 9:
            try:
                init_color(8, 500, 500, 500)
                self.gray_bg = 8
            except error:
                self.gray_bg = COLOR_BLACK
        try:
            curs_set(0)
        except error:
            pass
        stdscr.keypad(True)

        self.wall_colors = [
            COLOR_WHITE, COLOR_GREEN, COLOR_CYAN, COLOR_YELLOW,
            COLOR_MAGENTA, COLOR_BLUE, COLOR_RED
        ]
        self.pattern_colors = [
            COLOR_CYAN, COLOR_MAGENTA, COLOR_BLUE, COLOR_YELLOW,
            COLOR_GREEN, COLOR_RED, COLOR_WHITE
        ]
        self.wall_color_index = 0
        self.pattern_color_index = 0

        self.wall_pair = 1
        self.path_pair = 2
        self.entry_pair = 3
        self.exit_pair = 4
        self.pattern_pair = 5
        self.help_pair = 6
        self.pattern_fill_pair = 7
        self.empty_pair = 8
        self.search_frontier_pair = 10
        self.search_current_pair = 11

        self.__apply_color_pairs()
        stdscr.bkgd(' ', color_pair(self.empty_pair))

        entry = self.config.get("ENTRY")
        exit_pos = self.config.get("EXIT")
        assert isinstance(entry, tuple)
        assert isinstance(exit_pos, tuple)
        self.show_path = False
        if self.animations_enabled:
            maze = self.__generate_maze(
                stdscr,
                entry,
                exit_pos,
                seed=self.initial_seed
            )
        elif self.initial_maze is not None:
            maze = self.initial_maze
            self.ft_pattern = set(where_is_ft_pattern(maze))
        else:
            maze = self.__generate_maze(
                stdscr,
                entry,
                exit_pos
            )
        path, path_coords, path_edges = self.__compute_path(
            stdscr,
            maze,
            entry,
            exit_pos
        )
        self.__write_output_file(maze, entry, exit_pos, path)

        while True:
            self.__draw_maze(
                stdscr,
                maze,
                entry,
                exit_pos,
                path_coords,
                path_edges,
                self.show_path
            )
            key = stdscr.getch()
            if key in (ord('q'), ord('Q')):
                break
            if key in (ord('r'), ord('R')):
                maze = self.__generate_maze(
                    stdscr,
                    entry,
                    exit_pos
                )
                path, path_coords, path_edges = self.__compute_path(
                    stdscr,
                    maze,
                    entry,
                    exit_pos
                )
                self.__write_output_file(maze, entry, exit_pos, path)
            elif key in (ord('p'), ord('P')):
                self.show_path = not self.show_path
                if self.show_path:
                    path, path_coords, path_edges = self.__compute_path(
                        stdscr,
                        maze,
                        entry,
                        exit_pos
                    )
            elif key in (ord('w'), ord('W')):
                self.wall_color_index = (
                    self.wall_color_index + 1
                ) % len(self.wall_colors)
                self.__apply_color_pairs()
            elif key in (ord('f'), ord('F')):
                self.pattern_color_index = (
                    self.pattern_color_index + 1
                ) % len(self.pattern_colors)
                self.__apply_color_pairs()

    def __safe_add(
        self,
        stdscr: curses.window,
        y: int,
        x: int,
        text: str,
        cp: int
    ) -> None:
        try:
            stdscr.addstr(y, x, text, cp)
        except error:
            pass

    def __apply_color_pairs(self) -> None:
        init_pair(
            self.wall_pair,
            self.wall_colors[self.wall_color_index],
            COLOR_BLACK
        )
        init_pair(self.path_pair, COLOR_BLACK, COLOR_BLUE)
        init_pair(self.entry_pair, COLOR_BLACK, COLOR_GREEN)
        init_pair(self.exit_pair, COLOR_BLACK, COLOR_RED)
        init_pair(
            self.pattern_pair,
            self.pattern_colors[self.pattern_color_index],
            COLOR_WHITE
        )
        init_pair(
            self.pattern_fill_pair,
            COLOR_BLACK,
            COLOR_WHITE
        )
        init_pair(self.help_pair, COLOR_WHITE, COLOR_BLACK)
        init_pair(self.empty_pair, COLOR_BLACK, COLOR_BLACK)
        init_pair(self.search_frontier_pair, COLOR_BLACK, COLOR_CYAN)
        init_pair(self.search_current_pair, COLOR_BLACK, COLOR_YELLOW)

    def __write_output_file(
            self,
            maze: list[list[Cell]],
            entry: tuple[int, int],
            exit_pos: tuple[int, int],
            path: str | None = None
    ) -> None:
        output_file = self.config.get("OUTPUT_FILE")
        if not isinstance(output_file, str):
            return
        try:
            write_output_file(output_file, maze, entry, exit_pos, path)
        except OSError:
            pass

    def __generate_maze(
            self,
            stdscr: curses.window,
            entry: tuple[int, int],
            exit_pos: tuple[int, int],
            seed: int | None = None
    ) -> list[list[Cell]]:
        if seed is not None:
            random.seed(seed)
        if self.animations_enabled:
            return self.__generate_maze_with_animation(stdscr, entry, exit_pos)
        generator = self.__select_generator()
        maze: list[list[Cell]] = generator(self.config)
        self.ft_pattern = set(where_is_ft_pattern(maze))
        if not bool(self.config.get("PERFECT", True)):
            flaw_maze(maze)
        return maze

    def __compute_path(
            self,
            stdscr: curses.window,
            maze: list[list[Cell]],
            entry: tuple[int, int],
            exit_pos: tuple[int, int]
    ) -> tuple[str, set[tuple[int, int]], dict[tuple[int, int], set[str]]]:
        if self.show_path and self.animations_enabled:
            return self.__animate_search(stdscr, maze, entry, exit_pos)
        path = a_star(entry, exit_pos, maze)
        path_coords, path_edges = self.__path_to_coords_and_edges(path, entry)
        return path, path_coords, path_edges

    def __generate_maze_with_animation(
            self,
            stdscr: curses.window,
            entry: tuple[int, int],
            exit_pos: tuple[int, int]
    ) -> list[list[Cell]]:
        self.ft_pattern = set()
        generator = self.__select_generator()

        def on_step(grid: list[list[Cell]]) -> None:
            if not self.ft_pattern:
                self.ft_pattern = set(where_is_ft_pattern(grid))
            self.__draw_maze(
                stdscr,
                grid,
                entry,
                exit_pos,
                set(),
                {},
                False
            )
            time.sleep(self.animation_delay)

        maze: list[list[Cell]] = generator(self.config, on_step=on_step)
        if not bool(self.config.get("PERFECT", True)):
            flaw_maze(maze, on_step=on_step)
        return maze

    def __select_generator(
        self,
    ) -> Callable[..., list[list[Cell]]]:
        algorithm = self.config.get("ALGORITHM", "DFS")
        if isinstance(algorithm, str) and algorithm.upper() == "KRUSKAL":
            return generate_kruskal
        if isinstance(algorithm, str) and algorithm.upper() == "WILSON":
            return generate_wilson
        return generate_dfs

    def __path_to_coords_and_edges(
            self,
            path: str,
            entry: tuple[int, int]
    ) -> tuple[set[tuple[int, int]], dict[tuple[int, int], set[str]]]:
        x, y = entry
        coords: set[tuple[int, int]] = set()
        edges: dict[tuple[int, int], set[str]] = {}
        opposites = {"N": "S", "S": "N", "E": "W", "W": "E"}
        for step in path:
            start = (x, y)
            if step == 'N':
                y -= 1
            elif step == 'S':
                y += 1
            elif step == 'W':
                x -= 1
            elif step == 'E':
                x += 1
            end = (x, y)
            coords.add(end)
            edges.setdefault(start, set()).add(step)
            edges.setdefault(end, set()).add(opposites[step])
        return coords, edges

    def __animate_search(
            self,
            stdscr: curses.window,
            maze: list[list[Cell]],
            entry: tuple[int, int],
            exit_pos: tuple[int, int]
    ) -> tuple[str, set[tuple[int, int]], dict[tuple[int, int], set[str]]]:
        def on_step(
                current: tuple[int, int],
                open_set: set[tuple[int, int]],
                closed_set: set[tuple[int, int]],
                path: str
        ) -> None:
            path_coords, path_edges = self.__path_to_coords_and_edges(
                path,
                entry
            )
            self.__draw_maze(
                stdscr,
                maze,
                entry,
                exit_pos,
                path_coords,
                path_edges,
                True,
                search_frontier=open_set,
                search_current=current
            )
            time.sleep(self.path_animation_delay)

        path = a_star(entry, exit_pos, maze, on_step=on_step)
        path_coords, path_edges = self.__path_to_coords_and_edges(path, entry)
        return path, path_coords, path_edges

    def __animate_path(
            self,
            stdscr: curses.window,
            maze: list[list[Cell]],
            entry: tuple[int, int],
            exit_pos: tuple[int, int],
            path: str
    ) -> tuple[set[tuple[int, int]], dict[tuple[int, int], set[str]]]:
        x, y = entry
        coords: set[tuple[int, int]] = set()
        edges: dict[tuple[int, int], set[str]] = {}
        opposites = {"N": "S", "S": "N", "E": "W", "W": "E"}
        for step in path:
            start = (x, y)
            if step == 'N':
                y -= 1
            elif step == 'S':
                y += 1
            elif step == 'W':
                x -= 1
            elif step == 'E':
                x += 1
            end = (x, y)
            coords.add(end)
            edges.setdefault(start, set()).add(step)
            edges.setdefault(end, set()).add(opposites[step])
            self.__draw_maze(
                stdscr,
                maze,
                entry,
                exit_pos,
                coords,
                edges,
                True
            )
            time.sleep(self.path_animation_delay)
        return coords, edges

    def __is_pattern_wall(self, x: int, y: int, direction: str) -> bool:
        """Check if a wall should be colored as pattern wall."""
        if (x, y) in self.ft_pattern:
            return True
        if direction == "N" and (x, y - 1) in self.ft_pattern:
            return True
        if direction == "S" and (x, y + 1) in self.ft_pattern:
            return True
        if direction == "W" and (x - 1, y) in self.ft_pattern:
            return True
        if direction == "E" and (x + 1, y) in self.ft_pattern:
            return True
        if direction == "TL":  # Top-left corner
            if ((x - 1, y - 1) in self.ft_pattern or
                    (x - 1, y) in self.ft_pattern or
                    (x, y - 1) in self.ft_pattern):
                return True
        if direction == "TR":  # Top-right corner
            if ((x + 1, y - 1) in self.ft_pattern or
                    (x + 1, y) in self.ft_pattern or
                    (x, y - 1) in self.ft_pattern):
                return True
        if direction == "BL":  # Bottom-left corner
            if ((x - 1, y + 1) in self.ft_pattern or
                    (x - 1, y) in self.ft_pattern or
                    (x, y + 1) in self.ft_pattern):
                return True
        if direction == "BR":  # Bottom-right corner
            if ((x + 1, y + 1) in self.ft_pattern or
                    (x + 1, y) in self.ft_pattern or
                    (x, y + 1) in self.ft_pattern):
                return True
        return False

    def __draw_help(self, stdscr: curses.window, rows: int) -> None:
        help_y = rows * 2 + 2
        help_text = (
            "r: new maze  p: toggle search/path  w: wall color  "
            "f: 42 color  q: quit"
        )
        self.__safe_add(
            stdscr,
            help_y,
            0,
            help_text,
            color_pair(self.help_pair)
        )

    def __draw_maze(
            self,
            stdscr: curses.window,
            maze: list[list[Cell]],
            entry: tuple[int, int],
            exit_pos: tuple[int, int],
            path_coords: set[tuple[int, int]],
            path_edges: dict[tuple[int, int], set[str]],
            show_path: bool,
            search_frontier: set[tuple[int, int]] | None = None,
            search_current: tuple[int, int] | None = None
    ) -> None:
        stdscr.erase()
        search_frontier = search_frontier or set()
        rows = len(maze)
        cols = len(maze[0]) if rows > 0 else 0

        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                self.__draw_cell_structured(
                    stdscr,
                    x,
                    y,
                    cell,
                    rows,
                    cols,
                    entry,
                    exit_pos,
                    path_coords if show_path else set(),
                    path_edges if show_path else {},
                    search_frontier,
                    search_current
                )

        self.__draw_help(stdscr, rows)
        stdscr.noutrefresh()
        curses.doupdate()

    def __draw_cell_structured(
            self,
            stdscr: curses.window,
            x: int,
            y: int,
            cell: Cell,
            max_y: int,
            max_x: int,
            entry: tuple[int, int],
            exit_pos: tuple[int, int],
            path_coords: set[tuple[int, int]],
            path_edges: dict[tuple[int, int], set[str]],
            search_frontier: set[tuple[int, int]],
            search_current: tuple[int, int] | None
    ) -> None:
        yy, xx = y * 2, x * 4
        is_pattern = (x, y) in self.ft_pattern
        edge_dirs = path_edges.get((x, y), set())
        is_search_current = search_current == (x, y)

        # Top-left corner of the cell
        wall_cp_tl = (
            color_pair(self.pattern_pair)
            if self.__is_pattern_wall(x, y, "TL")
            else color_pair(self.wall_pair)
        )
        self.__safe_add(stdscr, yy, xx, "█", wall_cp_tl)

        # NORTH wall (top horizontal line)
        wall_cp_n = (
            color_pair(self.pattern_pair)
            if self.__is_pattern_wall(x, y, "N")
            else color_pair(self.wall_pair)
        )
        self.__safe_add(
            stdscr,
            yy,
            xx + 1,
            "███" if cell.north else "   ",
            wall_cp_n if cell.north else
            (color_pair(self.path_pair)
             if "N" in edge_dirs
             else color_pair(self.empty_pair))
        )

        # WEST wall (left vertical line)
        wall_cp_w = (
            color_pair(self.pattern_pair)
            if self.__is_pattern_wall(x, y, "W")
            else color_pair(self.wall_pair)
        )
        self.__safe_add(
            stdscr,
            yy + 1,
            xx,
            "█" if cell.west else " ",
            wall_cp_w if cell.west else
            (color_pair(self.path_pair)
             if "W" in edge_dirs
             else color_pair(self.empty_pair))
        )

        if (x, y) == entry:
            content = "   "
            content_cp = color_pair(self.entry_pair)
        elif (x, y) == exit_pos:
            content = "   "
            content_cp = color_pair(self.exit_pair)
        elif (x, y) in path_coords:
            content = "   "
            content_cp = color_pair(self.path_pair)
        elif is_search_current:
            content = "   "
            content_cp = color_pair(self.search_current_pair)
        elif (x, y) in search_frontier:
            content = "   "
            content_cp = color_pair(self.search_frontier_pair)
        else:
            content = "   "
            if is_pattern:
                content_cp = color_pair(self.pattern_fill_pair)
            else:
                content_cp = color_pair(self.empty_pair)

        # Interior space of the cell
        self.__safe_add(stdscr, yy + 1, xx + 1, content, content_cp)

        # If we're at the last column, draw the right edge of the maze
        if x == max_x - 1:
            # Top-right corner
            wall_cp_tr = (
                color_pair(self.pattern_pair)
                if self.__is_pattern_wall(x, y, "TR")
                else color_pair(self.wall_pair)
            )
            self.__safe_add(stdscr, yy, xx + 4, "█", wall_cp_tr)
            # EAST wall (right vertical line)
            wall_cp_e = (
                color_pair(self.pattern_pair)
                if self.__is_pattern_wall(x, y, "E")
                else color_pair(self.wall_pair)
            )
            self.__safe_add(
                stdscr,
                yy + 1,
                xx + 4,
                "█" if cell.east else " ",
                wall_cp_e if cell.east else
                (color_pair(self.path_pair)
                 if "E" in edge_dirs
                 else color_pair(self.empty_pair))
            )

        # If we're at the last row, draw the bottom edge of the maze
        if y == max_y - 1:
            # Bottom-left corner
            wall_cp_bl = (
                color_pair(self.pattern_pair)
                if self.__is_pattern_wall(x, y, "BL")
                else color_pair(self.wall_pair)
            )
            self.__safe_add(stdscr, yy + 2, xx, "█", wall_cp_bl)
            # SOUTH wall (bottom horizontal line)
            wall_cp_s = (
                color_pair(self.pattern_pair)
                if self.__is_pattern_wall(x, y, "S")
                else color_pair(self.wall_pair)
            )
            self.__safe_add(
                stdscr,
                yy + 2,
                xx + 1,
                "███" if cell.south else "   ",
                wall_cp_s if cell.south else
                (color_pair(self.path_pair)
                 if "S" in edge_dirs
                 else color_pair(self.empty_pair))
            )
            # If we're at the bottom-right corner of the maze
            if x == max_x - 1:
                # Bottom-right corner
                wall_cp_br = (
                    color_pair(self.pattern_pair)
                    if self.__is_pattern_wall(x, y, "BR")
                    else color_pair(self.wall_pair)
                )
                self.__safe_add(stdscr, yy + 2, xx + 4, "█", wall_cp_br)
