from src.utils import Parser
from pathlib import Path
from llm_sdk import Small_LLM_Model



model = Small_LLM_Model()
ids = model.encode("|").tolist()[0]
l = model.get_logits_from_input_ids(ids)

