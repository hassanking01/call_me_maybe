from llm_sdk import Small_LLM_Model
from rich.traceback import install
import json
install()

model = Small_LLM_Model()
with open(model.get_path_to_vocab_file(), 'r') as f:
    vocabulary = json.load(f)

# print(vocabulary)




prompt = "give me random color for my merch [not after you give me final answer end the chat with '[\end]' so i know you stoped]"
ids = model.encode(prompt).tolist()[0]
print("prompt :" ,  prompt, sep="\n")
line = ""
try:
    while True:
        logits = model.get_logits_from_input_ids(ids)
        m = logits.index(max(logits))
        ids += [m]
        now = model.decode(m)
        line += now
        print( now, end="", flush=True)
        if "[\end]" in line :
            break

except KeyboardInterrupt:
    pass
