import argparse


class Parser:
    def __init__(self) -> None:
        parser = argparse.ArgumentParser(
            "call_me_maybe",
            usage=(
                "uv run -m src "
                "[--functions_definition <function_definition_file>]"
                " [--input <input_file>] [--output <output_file>]"
            ),
        )
        parser.add_argument(
            "-f",
            "--functions_definition",
            default="data/input/functions_definition.json",
        )
        parser.add_argument(
            "-n",
            "--model_name",
            default="Qwen/Qwen3-0.6B"
        )
        parser.add_argument(
            "-i",
            "--input",
            default="data/input/function_calling_tests.json"
        )
        parser.add_argument(
            "-o",
            "--output",
            default="data/output/function_calls.json"
        )
        args = parser.parse_args()
        self.input: str = args.input
        self.output: str = args.output
        self.functions_definition: str = args.functions_definition
        self.model_name: str = args.model_name
