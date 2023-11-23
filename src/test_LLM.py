# from transformers import pipeline

# pipe = pipeline("text-generation", model="adept/persimmon-8b-base")
# print("SUCCESS PIPE")
# Load model directly
import time
from transformers import AutoModelForCausalLM, LlamaTokenizer, AutoTokenizer

print("SUCCESS IMPORT")
start = time.time()
tokenizer = LlamaTokenizer.from_pretrained("adept/persimmon-8b-chat")
print("SUCCESS LOAD TOKENIZER", time.time() - start)
start = time.time()
model = AutoModelForCausalLM.from_pretrained("adept/persimmon-8b-chat")
print("SUCCESS LOAD MODEL", time.time() - start)
start = time.time()
tokenizer.save_pretrained("model/persimmon-8b-base")
model.save_pretrained("model/persimmon-8b-base")
print("SUCCESS SAVE", time.time() - start)