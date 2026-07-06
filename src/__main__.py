from llm_sdk import Small_LLM_Model
from rich.traceback import install
import json
install()

model = Small_LLM_Model()
with open(model.get_path_to_vocab_file(), 'r') as f:
    vocabulary = json.load(f)



prompt = "what the sum of 1 and 2"
ids = model.encode(prompt).tolist()[0]
print("prompt :" ,  prompt, sep="\n")
line = ""
try:
    while True:
        logits = model.get_logits_from_input_ids(ids)
        sort = sorted(logits, reverse=True)
        for i in range(10):
            m = logits.index(sort[i])
            now = model.decode(m)
            print( f"{now} :--index--: {m} :--logit--: {sort[i]}", end="\n", flush=True)
        exit()
        ids += [m]
        line += now
        if "[\end]" in line :
            break

except KeyboardInterrupt:
    pass
