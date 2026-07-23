FILE=""
run:
	uv run -m src
install:
	mkdir -p ~/goinfre/call_me_maybe/.venv 
	uv sync


debug:
	uv run -m pdb $(FILE) --functions_definition="moulinette/data/input/functions_definition.json" --input="moulinette/data/input/function_calling_tests.json"