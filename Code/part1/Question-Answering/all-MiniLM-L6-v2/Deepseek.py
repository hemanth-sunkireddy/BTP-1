from transformers import AutoTokenizer, AutoModelForCausalLM


model_name = "deepseek-ai/deepseek-llm-7b-chat"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def classify_question_deepseek(question):
    prompt = f"""
    You are an AI trained to classify questions as either "Clear" or "Unclear."
    If the question is well-formed and specific, classify it as "Clear."
    If the question is vague, ambiguous, or lacks context, classify it as "Unclear."

    Question: "{question}"
    Classification:
    """
    
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(**inputs, max_length=100)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    
    if "Unclear" in response:
        return "Unclear"
    return "Clear"


question = "What is the thing that makes it work?"
print(classify_question_deepseek(question))

question = "How does the gradient descent algorithm optimize neural networks?"
print(classify_question_deepseek(question))

