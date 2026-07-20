FILE=""
run:
	uv run -m src
install:
	mkdir -p ~/goinfre/call_me_maybe/.venv 
	uv sync


debug:
	uv run -m pdb $(FILE)