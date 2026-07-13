# from src.utils import Parser
# from pathlib import Path
# from llm_sdk import Small_LLM_Model



# model = Small_LLM_Model()
# ids = model.encode("|").tolist()[0]
# l = model.get_logits_from_input_ids(ids)

last_token = [0.1 , 0.2]

vocabulary_tokens = [
    [0.3 , 0.4], 
    [0.9 , 0.6], 
    [0.7 , 0.7], 
    [0.6 , 0.8] 
]

for y, token in enumerate(vocabulary_tokens):
    for x, number in enumerate(last_token):
        vocabulary_tokens[y][x] *= number