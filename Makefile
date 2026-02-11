NAME = a_maze_ing
POETRY = ~/.local/bin/poetry
PY_FILES = $(shell find . -name "*.py")

all: install

install:
	@echo "Installing dependencies with Poetry..."
	@$(POETRY) install

run:
	@$(POETRY) run python a_maze_ing.py config.txt

debug:
	@echo "Running in debug mode..."
	@$(POETRY) run python -m pdb a_maze_ing.py config.txt

clean:
	@echo "Cleaning temporary files..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete

lint:
	@echo "Linting with flake8 and mypy..."
	@$(POETRY) run flake8 $(PY_FILES)
	@$(POETRY) run mypy $(PY_FILES) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	@echo "Linting with strict mode..."
	@$(POETRY) run flake8 $(PY_FILES)
	@$(POETRY) run mypy $(PY_FILES) --strict

.PHONY: all install run debug clean lint lint-strict
