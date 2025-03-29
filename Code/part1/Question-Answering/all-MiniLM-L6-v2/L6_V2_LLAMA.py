import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

# Load an open-source model for question classification
model_name = "facebook/bart-large-mnli"  # Open-source model
classifier = pipeline("zero-shot-classification", model=model_name, tokenizer=model_name)

def classify_question(question):
    labels = ["Vague", "Clear"]
    result = classifier(question, candidate_labels=labels)
    label = result['labels'][0]
    return label

# Load the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
index_file = "lecture_embeddings.index"
model_file = "faiss_model.pkl"
sentences_file = "sentences.txt"

def load_sentences(file_path):
    with open(file_path, 'r') as file:
        sentences = [line.strip() for line in file if line.strip()]
    return sentences

lecture_sentences = load_sentences(sentences_file)

if os.path.exists(model_file):
    print("Loading FAISS model from file...")
    with open(model_file, 'rb') as f:
        faiss_index = pickle.load(f)
else:
    if os.path.exists(index_file):
        print("Loading existing FAISS index...")
        faiss_index = faiss.read_index(index_file)
    else:
        print("Creating FAISS index...")
        sentence_embeddings = np.array(model.encode(lecture_sentences)).astype('float32')
        faiss_index = faiss.IndexFlatL2(sentence_embeddings.shape[1])
        faiss_index.add(sentence_embeddings)
        faiss.write_index(faiss_index, index_file)
        print("FAISS index saved.")
    
    with open(model_file, 'wb') as f:
        pickle.dump(faiss_index, f)
    print("FAISS model saved.")

while True:
    # Get student's question
    student_question = input("Enter your question (or type 'exit' to quit): ")
    if student_question.lower() == 'exit':
        break
    result = classify_question(student_question)
    
    if "Vague" in result:
        print("Your question seems unclear. Please provide more details.")
        
    else:
        print("Your question is clear. Proceeding with the answer...")

        question_embedding = np.array(model.encode([student_question])).astype('float32')
        
        distances, indices = faiss_index.search(question_embedding, len(lecture_sentences))
        
        distance_threshold = 0.7
        related_sentences = [
            (lecture_sentences[i], distances[0][j])
            for j, i in enumerate(indices[0])
            if 0 < distances[0][j] <= distance_threshold and not lecture_sentences[i].endswith('?')
        ]
        
        print("\nRelated Sentences:")
        if(len(related_sentences) == 0):
            print("NO related sentences found...")
        for sentence, distance in related_sentences:
            print(f"- {sentence} - {distance:.4f}")