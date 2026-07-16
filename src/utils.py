from pydantic import BaseModel
from enum import Enum
import argparse
import json
from llm_sdk import Small_LLM_Model

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
                        self.tier.setdefault(self.state, {}).update({'"': self.state + 1})
                        self.tier.setdefault(self.state + 1, {}).update({None: self.state + 2})
                        self.state += 2
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

    def update_state(self, generated_token: str, allowed_tokens):
        if allowed_tokens:
            for c in generated_token:
                if c in self.tier[self.current_state]:
                    self.current_state =  self.tier[self.current_state][c]
                    if self.current_state == -1:
                        return False
        else:
            if '"' in generated_token:
                self.current_state = self.tier[self.current_state][None]
        return True

class Model:
    def __init__(self, parser: Parser):
        self.parser = parser
        self.prompts: list[str] = []
        self.functions: list[Function] = []
        self.model = Small_LLM_Model()
        self.fsm = myfsm()
        self.get_functions()
        self.get_prompts()
        self.fsm.create_tier(self.functions)
        self.functions_str = ""
        self._creat_str_functions()
        self.base_prompt = (
            "<|im_start|>system\n"
            "You are a function calling system. Given a user request, "
            "output ONLY a JSON object calling the correct "
            "function, in this exact format:\n"
            '{"name": "function_name", "parameters": {...}}\n'
            "Available functions:\n"
            f"{self.functions_str}"
            "<|im_end|>\n"
            "<|im_start|>user\n"
            )
        print(self.base_prompt)
        exit()
        self.set_data = set()
        self.data = {}
        self.decoded_data = {}
        self.get_vocabulary()
        self.final_result = []
    
    def get_vocabulary(self):
        with open(self.model.get_path_to_vocab_file()) as vocab_file:
            bad_vocab_json = json.load(vocab_file)
        for key in bad_vocab_json:
            token = self.model.decode(bad_vocab_json[key])
            self.decoded_data[token] = bad_vocab_json[key]
            self.data[bad_vocab_json[key]] = token
            self.set_data.add(token)

    def _creat_str_functions(self):
        for function in self.functions:
            self.functions_str += f"- {function.name}( "
            for param in function.parameters:
                self.functions_str += f"{param}: {function.parameters[param].value}, "
            self.functions_str = self.functions_str[:-2]
            self.functions_str += f" ) : {function.description}\n"

    def get_functions(self) -> list[Function]:
        with open(self.parser.functions_definition) as f:
            data = json.load(f)
        for function in data:
            self.functions += [Function(
                name=function['name'],
                description=function['description'],
                parameters={
                    k: paramType(function['parameters'][k]['type']) for k in function['parameters'] 
                }
            )]

    def collect_tokens(self, state, token, allowed_tokens):
        if state == -1:
            return
        if state not in self.fsm.tier:
            return
        for ch in self.fsm.tier[state]:
            if not ch:
                return
            new_token = token + ch
            new_state = self.fsm.tier[state][ch]
            if new_token in self.set_data:
                allowed_tokens += [self.decoded_data[new_token]]
                self.collect_tokens(new_state, new_token, allowed_tokens) 

    def save_output(self):
        pass

    def get_prompts(self):
        with  open(self.parser.input) as f:
            data = json.load(f)
            self.prompts = [key['prompt'] for key in data ]

    def run(self):
        for promt in self.prompts:
            final_prompt = self.base_prompt + promt
            final_prompt += "<|im_end|>" 
            final_prompt += "\n" + "<|im_start|>assistant"        
            ids = self.model.encode(final_prompt).tolist()[0]
            line = ""
            while True:
                allowed_tokens = []
                self.collect_tokens(self.fsm.current_state, "" ,allowed_tokens)
                logits = self.model.get_logits_from_input_ids(ids)
                filtred_logits = [float("-inf")] * len(logits)
                if allowed_tokens:
                    for token_id in allowed_tokens:
                        filtred_logits[token_id] = logits[token_id]
                    logits = filtred_logits
                m = logits.index(max(logits))
                ids += [m]
                line += self.data[m]

                print(self.data[m], end="", flush=True)
                if not self.fsm.update_state(self.data[m], allowed_tokens):
                    self.fsm.current_state = 0
                    valid_json = json.loads(line)
                    self.final_result += [{"prompt": promt, **valid_json}]
                    print()
                    break