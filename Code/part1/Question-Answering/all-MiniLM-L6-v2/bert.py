import torch
from transformers import BertTokenizer, BertForSequenceClassification

model_name = "textattack/bert-base-uncased-imdb" 
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

def classify_question(question):
    inputs = tokenizer(question, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1).squeeze().tolist()
    
    labels = ["clear", "not clear"]
    predicted_label = labels[torch.argmax(logits)]
    confidence = max(probabilities)

    print(f"Predicted Label: {predicted_label} (Confidence: {confidence:.2f})")

# Example
question = "What is Linear Regression?"
classify_question(question)
