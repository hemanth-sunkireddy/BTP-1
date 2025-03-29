# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-llm-7b-chat")
model = AutoModelForCausalLM.from_pretrained("deepseek-ai/deepseek-llm-7b-chat")
print(model)