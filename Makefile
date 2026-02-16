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

clean: clean-package
	@echo "Cleaning temporary files and build artifacts..."
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@rm -rf dist/ build/ *.egg-info mazegen/

lint:
	@echo "Linting with flake8 and mypy..."
	@$(POETRY) run flake8 $(PY_FILES)
	@$(POETRY) run mypy $(PY_FILES) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	@echo "Linting with strict mode..."
	@$(POETRY) run flake8 $(PY_FILES)
	@$(POETRY) run mypy $(PY_FILES) --strict

test:
	@echo "Running tests with pytest..."
	@$(POETRY) run pytest -q

bundle-mazegen:
	@echo "Bundling mazegen from source files..."
	@$(POETRY) run python scripts/bundle_mazegen.py

build-package: bundle-mazegen
	@echo "Building mazegen package..."
	@cp mazegen_pyproject.toml mazegen/pyproject.toml
	@$(POETRY) run python -m build mazegen/
	@rm mazegen/pyproject.toml
	@mv mazegen/dist/* ./ 2>/dev/null || true
	@rm -rf mazegen/dist

clean-package:
	@echo "Cleaning package build artifacts..."
	@rm -rf dist/ build/ *.egg-info mazegen/*.egg-info mazegen/build mazegen/dist
	@rm -f mazegen-*.whl mazegen-*.tar.gz

.PHONY: all install run debug clean lint lint-strict test bundle-mazegen build-package clean-package
