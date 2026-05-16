clean:
	@rm -rf __pycache__
	@rm -rf **/__pycache__
	@rm -rf .mypy_cache

lint:
	uv run flake8
	uv run mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs