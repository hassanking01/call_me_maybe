from pydantic import BaseModel
from enum import Enum
import argparse
class paramType(Enum):
    NUMBER = "number"
    INTEGER = "integer"
    STRING = "string"
    BOOLEAN = "boolean"

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

class myfsm:
    def __init__(self):
        self.current_state = 0
        self.tier = {}
        self.state = 0
    
    def create_tier(self, functions: list[Function]):
        first_part = '{"name": "'
        for c in first_part:
            self.tier[self.state] = {c: self.state + 1}
            self.state += 1
        saved = self.state
        params = '", "params": {'
        for function in functions:
            current = saved
            for c in function.name:
                if c in  self.tier.get(current, {}):
                    current = self.tier[current][c]
                else:
                    self.tier.setdefault(current, {}).update({c: self.state + 1})
                    self.state += 1
                    current = self.state
            for c in params:
                self.tier[self.state] = {c: self.state + 1}
                self.state += 1
            for idx , param in enumerate(function.parameters):
                for c in '"' + param + '": ':
                    self.tier[self.state] = {c: self.state + 1}
                    self.state += 1

                # TODO MAKE ALL PARAMS TYPES
                match function.parameters[param]:
                    
                    case paramType.NUMBER:
                        for c in '-0123456789':
                            if c == '-':
                                self.tier.setdefault(self.state, {}).update({c: self.state + 1})
                            elif c == '0':
                                self.tier.setdefault(self.state, {}).update({c: self.state + 2})
                            else:
                                self.tier.setdefault(self.state, {}).update({c: self.state + 3})
                        for c in '0123456789':
                            if c == '0':
                                self.tier.setdefault(self.state + 1 , {}).update({c: self.state + 2})
                            else:
                                self.tier.setdefault(self.state + 1, {}).update({c: self.state + 3})
                        self.tier.setdefault(self.state + 2, {}).update({".": self.state + 4})
                        for c in ".0123456789":
                            if c == ".":
                                self.tier.setdefault(self.state + 3, {}).update({c: self.state + 4})
                            else:
                                self.tier.setdefault(self.state + 3, {}).update({c: self.state + 3})
                        for c in "012345789":
                            self.tier.setdefault(self.state + 4, {}).update({c: self.state + 5})
                        
                        for c in "012345789":
                            self.tier.setdefault(self.state + 5, {}).update({c: self.state + 5})
                        self.state += 5
                    case paramType.INTEGER:
                        pass
                    case paramType.STRING:
                        pass
                    case paramType.BOOLEAN:
                        pass
                
                if idx < len(function.parameters) -1:
                    for c in ", ":
                        self.tier.setdefault(self.state, {}).update( {c: self.state + 1})
                        self.state += 1
                else:
                    self.tier.setdefault(self.state, {}).update({"}": self.state + 1})
                    self.state += 1
                    self.tier.setdefault(self.state, {}).update({"}": -1})

    def update_state(self, generated_token: str):
        for c in generated_token:
            if c in self.tier[self.current_state]:
                self.current_state =  self.tier[self.current_state][c]
                if self.current_state == -1:
                    return False
        return True
                    