#!/usr/bin/env python3
"""
Bundle script to generate the mazegen package from src/a_maze_ing sources.

This script reads the source files from src/a_maze_ing/ and generates
a standalone mazegen/ package with rewritten imports.

Usage:
    python scripts/bundle_mazegen.py
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
SRC_DIR = ROOT / "src" / "a_maze_ing"
MAZEGEN_DIR = ROOT / "mazegen"
MAZEGEN_SRC_DIR = Path(__file__).parent / "mazegen_sources"

# Standard library imports to keep at the top of generator.py
STDLIB_IMPORTS = {
    "random",
    "heapq",
    "collections.abc",
    "enum",
    "typing",
    "__future__",
}


def rewrite_imports(content: str) -> str:
    """Rewrite imports from src.a_maze_ing to mazegen."""
    content = re.sub(
        r'from src\.a_maze_ing\.algorithms\.(\w+)',
        r'from mazegen.algorithms.\1',
        content
    )
    content = re.sub(
        r'from src\.a_maze_ing\.(\w+)',
        r'from mazegen.\1',
        content
    )
    content = re.sub(
        r'import src\.a_maze_ing\.(\w+)',
        r'import mazegen.\1',
        content
    )
    return content


def is_stdlib_import(line: str) -> bool:
    """Check if an import line is for stdlib."""
    for mod in STDLIB_IMPORTS:
        if f"import {mod}" in line or f"from {mod}" in line:
            return True
    return False


def is_internal_import(line: str) -> bool:
    """Check if an import is internal (mazegen or src.a_maze_ing)."""
    return "mazegen" in line or "src.a_maze_ing" in line


def extract_code_parts(content: str) -> tuple[list[str], str]:
    """Extract stdlib imports and code body from a file."""
    lines = content.split('\n')
    stdlib_imports: list[str] = []
    code_lines: list[str] = []

    in_docstring = False
    docstring_char = None
    at_start = True

    skip_until_paren_close = False

    for line in lines:
        stripped = line.strip()

        if skip_until_paren_close:
            if ')' in stripped:
                skip_until_paren_close = False
            continue

        if in_docstring:
            if docstring_char and docstring_char in stripped:
                in_docstring = False
            continue

        if at_start and stripped.startswith(('"""', "'''")):
            docstring_char = stripped[:3]
            if stripped.count(docstring_char) >= 2 and len(stripped) > 3:
                continue
            in_docstring = True
            continue

        if stripped and not stripped.startswith('#'):
            at_start = False

        if stripped.startswith(('import ', 'from ')):
            if is_internal_import(stripped):
                if '(' in stripped and ')' not in stripped:
                    skip_until_paren_close = True
                continue
            elif is_stdlib_import(stripped):
                if stripped not in stdlib_imports:
                    stdlib_imports.append(stripped)
            else:
                code_lines.append(line)
        else:
            code_lines.append(line)

    code = '\n'.join(code_lines).strip()
    return stdlib_imports, code


def add_docstring_if_missing(content: str, docstring: str) -> str:
    """Add a module docstring if not present."""
    if content.strip().startswith(('"""', "'''")):
        return content
    return docstring + "\n\n" + content


def bundle_cell() -> None:
    """Bundle cell.py from source."""
    src_cell = SRC_DIR / "core" / "cell.py"
    content = read_and_process(src_cell)

    docstring = '''"""Cell module for maze representation.

This module defines the Cell class and CellState enum used to represent
individual cells within a maze.

This file is auto-generated from src/a_maze_ing sources.
Do not edit directly - modify the source files instead.
"""'''

    content = add_docstring_if_missing(content, docstring)

    dest = MAZEGEN_DIR / "cell.py"
    dest.write_text(content)
    print(f"  Generated {dest.relative_to(ROOT)}")


def read_and_process(path: Path) -> str:
    """Read file and rewrite imports."""
    content = path.read_text()
    return rewrite_imports(content)


def bundle_generator() -> None:
    """Bundle generator.py by combining algorithm sources."""

    # Read all algorithm files
    dfs_src = SRC_DIR / "algorithms" / "dfs.py"
    kruskal_src = SRC_DIR / "algorithms" / "kruskal.py"
    wilson_src = SRC_DIR / "algorithms" / "wilson.py"
    a_star_src = SRC_DIR / "algorithms" / "a_star.py"
    ft_pattern_src = SRC_DIR / "algorithms" / "ft_pattern.py"
    grid_utils_src = SRC_DIR / "algorithms" / "grid_utils.py"
    flaw_src = SRC_DIR / "maze" / "flaw.py"
    wrapper_src = MAZEGEN_SRC_DIR / "wrapper.py.part"

    # Extract code from each file
    dfs_imports, dfs_code = extract_code_parts(read_and_process(dfs_src))
    kruskal_imports, kruskal_code = extract_code_parts(
        read_and_process(kruskal_src)
    )
    wilson_imports, wilson_code = extract_code_parts(
        read_and_process(wilson_src)
    )
    a_star_imports, a_star_code = extract_code_parts(
        read_and_process(a_star_src)
    )
    ft_imports, ft_code = extract_code_parts(
        read_and_process(ft_pattern_src)
    )
    grid_utils_imports, grid_utils_code = extract_code_parts(
        read_and_process(grid_utils_src)
    )
    flaw_imports, flaw_code = extract_code_parts(
        read_and_process(flaw_src)
    )
    wrapper_imports, wrapper_code = extract_code_parts(
        read_and_process(wrapper_src)
    )

    # Merge all stdlib imports (deduplicated)
    all_imports = set()
    for imp_list in [
        dfs_imports,
        kruskal_imports,
        wilson_imports,
        a_star_imports,
        ft_imports,
        grid_utils_imports,
        flaw_imports,
        wrapper_imports
    ]:
        all_imports.update(imp_list)
    all_imports.add("from collections.abc import Mapping")

    # Sort imports nicely
    from_future = [i for i in all_imports if "from __future__" in i]
    regular_imports = [i for i in all_imports if i.startswith("import ")]
    from_imports = [i for i in all_imports
                    if i.startswith("from ") and "from __future__" not in i]

    sorted_imports = (from_future
                      + sorted(regular_imports)
                      + sorted(from_imports))

    # Build the combined file
    header = '''"""Maze Generator module.

This module provides the MazeGenerator class for creating random mazes
using DFS, Kruskal, or Wilson algorithms, with A* pathfinding.

This file is auto-generated from src/a_maze_ing sources.
Do not edit directly - modify the source files instead.
"""

'''

    imports_section = '\n'.join(sorted_imports)
    internal_import = "\nfrom mazegen.cell import Cell, CellState\n"
    type_alias = (
        "\nMazeConfig = Mapping[str, int | tuple[int, int] | str | bool]\n"
    )

    # Combine all code sections
    combined_code = f"""

# =============================================================================
# FT Pattern (from algorithms/ft_pattern.py)
# =============================================================================

{ft_code}


# =============================================================================
# Grid Helpers (from algorithms/grid_utils.py)
# =============================================================================

{grid_utils_code}


# =============================================================================
# Flaw Maze (from maze/flaw.py)
# =============================================================================

{flaw_code}


# =============================================================================
# DFS Algorithm (from algorithms/dfs.py)
# =============================================================================

{dfs_code}


# =============================================================================
# Kruskal Algorithm (from algorithms/kruskal.py)
# =============================================================================

{kruskal_code}


# =============================================================================
# Wilson Algorithm (from algorithms/wilson.py)
# =============================================================================

{wilson_code}


# =============================================================================
# A* Pathfinding (from algorithms/a_star.py)
# =============================================================================

{a_star_code}


# =============================================================================
# MazeGenerator - Main class (from mazegen_wrapper.py)
# =============================================================================

{wrapper_code}
"""

    # Write the combined file
    full_content = (
        header
        + imports_section
        + internal_import
        + type_alias
        + combined_code
    )

    # Clean up multiple blank lines
    full_content = re.sub(r'\n{3,}', '\n\n\n', full_content)

    dest = MAZEGEN_DIR / "generator.py"
    dest.write_text(full_content)
    print(f"  Generated {dest.relative_to(ROOT)}")


def bundle_init() -> None:
    """Generate __init__.py for mazegen package."""
    init_src = MAZEGEN_SRC_DIR / "__init__.py.part"
    content = read_and_process(init_src)

    dest = MAZEGEN_DIR / "__init__.py"
    dest.write_text(content)
    print(f"  Generated {dest.relative_to(ROOT)}")


def bundle_py_typed() -> None:
    """Create py.typed marker file."""
    dest = MAZEGEN_DIR / "py.typed"
    dest.write_text("")
    print(f"  Generated {dest.relative_to(ROOT)}")


def bundle_readme() -> None:
    """Copy README for the mazegen package."""
    src = MAZEGEN_SRC_DIR / "README.md"
    if not src.exists():
        raise FileNotFoundError(
            f"Missing {src.relative_to(ROOT)}. "
            "Please add a short README for the mazegen package."
        )
    dest = MAZEGEN_DIR / "README.md"
    dest.write_text(src.read_text())
    print(f"  Generated {dest.relative_to(ROOT)}")


def main() -> None:
    """Main entry point for bundling."""
    print("Bundling mazegen package from src/a_maze_ing sources...")
    print()

    # Ensure mazegen directory exists
    MAZEGEN_DIR.mkdir(exist_ok=True)

    # Generate files
    bundle_cell()
    bundle_generator()
    bundle_init()
    bundle_py_typed()
    bundle_readme()

    print()
    print("Done! mazegen package has been generated.")


if __name__ == "__main__":
    main()
