# Load model directly
from transformers import AutoModelForCausalLM, AutoTokenizer
# model = AutoModelForCausalLM.from_pretrained("tiiuae/falcon-40b", trust_remote_code=True)
model = "tiiuae/falcon-40b"

tokenizer = AutoTokenizer.from_pretrained(model)
print("SUCCESS LOAD")
# model.save_pretrained("model/falcon-40b")
tokenizer.save_pretrained("model/falcon-40b-tokenizer")
print("SUCCESS SAVE")