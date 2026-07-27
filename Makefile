run:
	uv run -m src
install:
	uv sync
lint:
	uv run -m flake8 src
	uv run -m mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs -p src

lint-strict:
	uv run -m flake8 src
	uv run -m mypy --strict -p src

debug:
	uv run -m pdb -m src
clean:
	rm -rf .mypy_cache
	uv run -m pyclean --debris all -- .