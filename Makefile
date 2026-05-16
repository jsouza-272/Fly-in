FLAKE8_CHECK = $(shell .venv/bin/python3 -c 'import flake8' 2>/dev/null && echo '1' || echo '0')
MYPY_CHECK = $(shell .venv/bin/python3 -c 'import mypy' 2>/dev/null && echo '1' || echo '0')
PYGAME_CHECK = $(shell .venv/bin/python3 -c 'import pygame' 2>/dev/null && echo '1' || echo '0')
UV_CHECK = $(shell .venv/bin/python3 -c 'import uv' 2>/dev/null && echo '1' || echo '0')

UV = .venv/bin/uv
PYTHON = .venv/bin/python3
MAP = maps/challenger/01_the_impossible_dream.txt

install:
	@if [ ! -d ".venv" ]; then \
		python3 -m venv .venv; \
	fi
	@if [ "$(UV)" = "0" ]; then \
		.venv/bin/pip install uv; \
		.venv/bin/uv sync; \
	fi

run: install
	$(UV) run fly_in.py $(MAP)

debug: install
	$(PYTHON) -m pdb fly_in.py $(MAP)

clean:
	@rm -rf __pycache__
	@rm -rf **/__pycache__
	@rm -rf .mypy_cache

lint: install
	@$(UV) run flake8 .
	@$(UV) run mypy . --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs