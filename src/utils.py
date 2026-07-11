from pydantic import BaseModel
from enum import Enum
import argparse
class paramType(Enum):
    NUMBER = "number"
    INTEGER = "integer"
    STRING = "string"

class Function(BaseModel):
    name: str
    description: str
    parameters: dict[str, paramType]

class Parser:
    def __init__(self):
        parser = argparse.ArgumentParser('call_me_maybe', usage='uv run -m src [--functions_definition <function_definition_file>] [--input <input_file>] [--\
        output <output_file>]')
        parser.add_argument(
            '-f',
            '--functions_definition',
            default="data/input/functions_definition.json"
            )
        parser.add_argument(
            '-i',
            '--input',
            default="data/input/function_calling_tests.json"
            )
        parser.add_argument(
            '-o',
            '--output',
            default='data/output/function_calls.json')
        args = parser.parse_args()
        self.input: str = args.input
        self.output: str = args.output
        self.functions_definition: str = args.functions_definition
    