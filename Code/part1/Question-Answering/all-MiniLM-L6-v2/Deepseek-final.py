from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

question = "What are you?"
labels = ["clear", "not clear"]

result = classifier(question, labels)
print(result)
