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
    fun_str += f"- {function.name}( "
    for param in function.parameters:
        fun_str += f"{param}: {function.parameters[param].value}, "
    fun_str = fun_str[:-2]
    fun_str += f" ) : {function.description}\n"


base_prompt = (
"<|im_start|>system\n"
"You are a function calling system. Given a user request, "
"output ONLY a JSON object calling the correct "
"function, in this exact format:\n"
'{"name": "function_name", "parameters": {...}}\n'
"Available functions:\n"
f"{fun_str}"
"<|im_end|>\n"
"<|im_start|>user\n"
)

from pprint import pprint



def collect_tokens(state, token, allowed_tokens):
    if state == -1:
        return
    if state not in fsm.tier:
        return
    for ch in fsm.tier[state]:
        new_token = token + ch
        new_state = fsm.tier[state][ch]
        if new_token in set_data:
            allowed_tokens += [decoded_data[new_token]]
            collect_tokens(new_state, new_token, allowed_tokens) 


try:
    for promt in prompts:
        final_prompt = base_prompt + promt 
        final_prompt += "\n" + "<|im_start|>assistant"        
        ids = model.encode(final_prompt).tolist()[0]
        line = ""
        resutl = []
        while True:
            allowed_tokens = []
            state = fsm.current_state
            collect_tokens(fsm.current_state, "" ,allowed_tokens)
            logits = model.get_logits_from_input_ids(ids)
            filtred_logits = [float("-inf")] * len(logits)
            for token_id in allowed_tokens:
                filtred_logits[token_id] = logits[token_id]
            logits = filtred_logits
            m = logits.index(max(logits))
            ids += [m]
            line += data[m]

            print(data[m], end="", flush=True)
            if not fsm.update_state(data[m]):
                fsm.current_state = 0
                valid_json = json.loads(line)
                resutl += [{"prompt": promt, **valid_json}]
                print()
                break
    print(resutl)
except KeyboardInterrupt:
    pass
