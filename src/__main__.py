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
for k in vocabulary:
    data[vocabulary[k]] = model.decode(vocabulary[k])
f = get_functions(parser)
prompts = get_prompts(parser)


fsm = myfsm()
fsm.create_tier(f)

for key, value in fsm.tier.items():
    print(key , value)

































exit()
fun_str = ""
for function in f:
    fun_str += f"{function.name}("
    for param in function.parameters:
        fun_str += f"{param}:{function.parameters[param].value},"
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
try:
    result = "["
    for promt in prompts:
        final_prompt = base_prompt + promt
        final_prompt += "{\n"
        final_prompt += f'"prompt":"{promt}",\n"name": "'
        ids = model.encode(final_prompt).tolist()[0]
        stack = ["{"]
        line = "{"
        line += f'"prompt":"{promt}",\n"name": "'
        print(line, end="" , flush=True)
        while True:
            logits = model.get_logits_from_input_ids(ids)
            m = logits.index(max(logits))
            ids += [m]
            line += data[m]
            if "{" in data[m]:
                stack += ["{"]
            if "}" in data[m]:
                stack.pop()
            print(data[m], end="", flush=True)
            if not stack:
                break
        result += line + ","
    result = result[:-1]
    result += "]"
    obj = json.loads(result)
    
except KeyboardInterrupt:
    pass
