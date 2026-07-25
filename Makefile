FILE=""
run:
	uv run -m src
install:
	mkdir -p ~/goinfre/call_me_maybe/.venv 
	uv sync
lint:
	uv run -m flake8 src
	uv run -m mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs src

lint-strict:
	uv run -m flake8 src
	uv run -m mypy --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs src

debug:
	uv run -m pdb $(FILE) --functions_definition="moulinette/data/input/functions_definition.json" --input="moulinette/data/input/function_calling_tests.json"
