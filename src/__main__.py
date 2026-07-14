from rich.traceback import install
install()
from llm_sdk import Small_LLM_Model
import json
from src.utils import Function, paramType, Parser, myfsm

parser = Parser()

def get_functions(args: Parser) -> list[Function]:
    with open(args.functions_definition) as f:
        data = json.load(f)
    functions = []
    d = {'number':paramType.NUMBER, 'string': paramType.STRING}
    for function in data:
        functions += [Function(
            name=function['name'],
            description=function['description'],
            parameters={
                k: paramType(function['parameters'][k]['type']) for k in function['parameters'] 
            }
        )]
    return functions

def save_output(args: Parser):
    pass

def get_prompts(args: Parser):
    prompts = []
    with  open(args.input) as f:
        data = json.load(f)
        prompts = [key['prompt'] for key in data ]
    return prompts

model = Small_LLM_Model()
with open(model.get_path_to_vocab_file(), 'r') as f:
    vocabulary = json.load(f)

data = {}
set_data = set()
decoded_data = {}
for k in vocabulary:
    data[vocabulary[k]] = model.decode(vocabulary[k])
    set_data.add(data[vocabulary[k]])
    decoded_data[data[vocabulary[k]]] = vocabulary[k]
f = get_functions(parser)
prompts = get_prompts(parser)


fsm = myfsm()
fsm.create_tier(f)

































fun_str = ""
for function in f:
    fun_str += f"{function.name}("
    for param in function.parameters:
        fun_str += f"{param}: {function.parameters[param].value},"
    fun_str = fun_str[:-1]
    fun_str += f") : {function.description}\n"

base_prompt = "you are a function calling system here" \
f" are the tools:\n{fun_str}" \
"output should be like this example\n" \
"{\n"\
'"prompt": "What is the sum of 2 and 3?",\n'\
'"name": "fn_add_numbers",\n'\
'"parameters": {"a": 2.0, "b": 3.0}\n'
"}"
from pprint import pprint
pprint(fsm.tier, indent=4)

try:
    result = "["
    for promt in prompts:
        print(promt)
        final_prompt = base_prompt + promt
        final_prompt += "{\n"
        final_prompt += f'"prompt":"{promt}",\n"name": "'
        ids = model.encode(final_prompt).tolist()[0]
        stack = ["{"]
        line = ""
        while True:
            token = ""
            allowed_tokens = []
            t = []
            state = fsm.current_state
            while True:
                flag = False
                d = fsm.tier[state]
                if len(d) == 1:
                    for key in d:
                        token += key
                        if token in set_data:
                            allowed_tokens += [decoded_data[token]]
                            t += [token]
                        else:
                            flag = True
                            break
                        state = fsm.tier[state][key]
                        flag = state == -1                            
                else:
                    for key in d:
                        allowed_tokens += [decoded_data[key]]
                    flag = True
                if flag:
                    break
            logits = model.get_logits_from_input_ids(ids)
            filtred_logits = [float("-inf")] * len(logits)
            for token in allowed_tokens:
                filtred_logits[token] = logits[token]
            logits = filtred_logits
            m = logits.index(max(logits))
            ids += [m]
            line += data[m]
            flag = False
            for c in data[m]:
                if c in fsm.tier[fsm.current_state]:
                    fsm.current_state =  fsm.tier[fsm.current_state][c]
                    flag = fsm.current_state == -1

            print(data[m], end="", flush=True)
            if flag:
                break
    
except KeyboardInterrupt:
    pass
