from rich.traceback import install
install()
from llm_sdk import Small_LLM_Model
import json
from src.utils import Function, paramType, Parser, 

parser = Parser()





fun_str = ""



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
        final_prompt += "<|im_end|>" 
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
