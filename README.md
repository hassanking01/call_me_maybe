*This project has been created as part of the 42 curriculum by hahchtar.*

# call_me_maybe - Introduction to Function Calling in LLMs

## Description
`call_me_maybe` is a Python project designed to convert natural language prompts into structured, machine-readable function calls using Large Language Models (LLMs) and constrained decoding.

The primary goal of this project is to achieve 100% syntactically valid JSON output matching predefined function schemas (defined in `functions_definition.json`), even when using small models such as Qwen3-0.6B.

## Instructions

### Prerequisites
- Python 3.10+
- `uv` package manager

### Installation
To install the required dependencies and set up the virtual environment:
```bash
make install
```
or manually:
```bash
uv sync
```

### Execution
Run the program with default arguments (`data/input/functions_definition.json` and `data/input/function_calling_tests.json`):
```bash
make run
```
or with custom arguments:
```bash
uv run python -m src --functions_definition <path_to_schema> --input <path_to_input> --output <path_to_output>
```

### Code Quality & Maintenance
- **Linting**: `make lint`
- **Strict Linting**: `make lint-strict`
- **Debugging**: `make debug`
- **Cleaning temporary files**: `make clean`

## Example Usage

### Input Prompt Example (`data/input/function_calling_tests.json`)
```json
[
  {
    "prompt": "What is the sum of 2 and 3?"
  }
]
```

### Output Result (`data/output/function_calls.json`)
```json
[
  {
    "prompt": "What is the sum of 2 and 3?",
    "name": "fn_add_numbers",
    "parameters": {
      "a": 2.0,
      "b": 3.0
    }
  }
]
```

## Algorithm Explanation
The program implements **constrained decoding** during token generation:
1. **Schema Parsing**: Reads available functions and their parameter types (numbers, strings, booleans, etc.) from `functions_definition.json`.
2. **Logit Masking**: At each generation step, the model predicts logits over the vocabulary. Unallowed tokens (tokens that break valid JSON syntax or violate the target argument schema) are masked by setting their logit values to negative infinity (`-inf`).
3. **Valid Token Sampling**: Only tokens that satisfy structural JSON formatting and schema typing are sampled, ensuring the generated output is 100% parseable JSON.

## Design Decisions
- **Pydantic Validation**: Used Pydantic schemas for parameter validation and data serialization.
- **Modular Structure**: Code is organized into `parser.py` (CLI options), `model.py` (LLM inference and decoding logic), and `utils.py`.
- **Graceful Error Handling**: Input files and JSON schemas are validated prior to execution to handle missing files or invalid JSON gracefully.

## Performance Analysis
- **Accuracy**: Near 100% schema compliance by enforcing strict logit constraints token-by-token.
- **Speed**: Efficient token masking keeps execution fast on small models like Qwen3-0.6B.
- **Reliability**: Completely eliminates JSON syntax errors and invalid parameter types.

## Challenges Faced
- **Tokenizer Vocabulary Mapping**: Matching model subword tokens to expected JSON structural tokens while accounting for leading space prefixes.
- **Dynamic Schema Enforcement**: Transitioning logit constraints smoothly between function name selection and argument parameter extraction.

## Testing Strategy
- Verified output against defined schemas in `functions_definition.json`.
- Tested edge cases including empty inputs, invalid JSON structure, and parameter type mismatches.
- Verified code quality using `flake8` and static typing with `mypy`.

## Resources
- **Pydantic Documentation**: [docs.pydantic.dev](https://docs.pydantic.dev/)
- **what is an LLM**:[medium.com](https://medium.com/data-science-at-microsoft/how-large-language-models-work-91c362f5b78f)
- **how LLM works**: [youtube.com](https://www.youtube.com/watch?v=7xTGNNLPyMI&t=2203s)
### AI Usage Statement
AI tools were used during this project to understand how LLMs work, learn about constrained decoding and function calling, and help create and format this README.md file.
