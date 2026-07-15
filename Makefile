FILE=""
run:
	uv run -m src
install:
	uv sync


debug:
	uv run -m pdb $(FILE)