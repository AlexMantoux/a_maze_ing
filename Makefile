NAME = a_maze_ing
POETRY = poetry run
PY_FILES = $(shell find . -name "*.py")

all: install

install:
	@echo "Installing dependencies with Poetry..."
	@poetry install

run:
	@$(POETRY) python a_maze_ing.py config.txt

debug:
	@echo "Running in debug mode..."
	@$(POETRY) python -m pdb a_maze_ing.py config.txt

clean:
	@echo "Cleaning temporary files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete

lint:
	@echo "Linting with flake8 and mypy..."
	@$(POETRY) flake8 $(PY_FILES)
	@$(POETRY) mypy $(PY_FILES) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	@echo "Linting with strict mode..."
	@$(POETRY) flake8 $(PY_FILES)
	@$(POETRY) mypy $(PY_FILES) --strict

.PHONY: all install run debug clean lint lint-strict
