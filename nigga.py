from src.utils import FSM, Function, Parser, paramType
from llm_sdk import Small_LLM_Model
import json
from pprint import pprint


token = "hello there \" what u doing \""
resutl = 0
print(token)

print([c for c in token])
print([i for i in range(len(token))])
print(token[:resutl + 1])
print(resutl)



























































exit()

model = Small_LLM_Model()


vocabulary_path = model.get_path_to_vocab_file()

with open(vocabulary_path) as vocabulary_file:
    bad_vocabulary = json.load(vocabulary_file) 
    good_vocabulary = {model.decode(bad_vocabulary[key]):bad_vocabulary[key] for key in bad_vocabulary}

set_data = set(good_vocabulary.keys())
all_token_string = []
for token in set_data:
    if token.startswith('\\"'):
        all_token_string += [token]



fsm = FSM()

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

p = Parser()

fsm.create_tier(get_functions(p))
pprint(fsm.tier, indent=4)
exit()
def collect_tokens(state, token, allowed_tokens):
    if state == -1:
        return
    if state not in fsm.tier:
        return
    for ch in fsm.tier[state]:
        new_token = token + ch
        new_state = fsm.tier[state][ch]
        if new_token in set_data:
            allowed_tokens += [new_token]
            collect_tokens(new_state, new_token, allowed_tokens) 

test = []

for key in fsm.tier[13]:
        new_stat = fsm.tier[13][key]
        if key in set_data:
            test += [key]
        collect_tokens(new_stat, key, test)


print(test)