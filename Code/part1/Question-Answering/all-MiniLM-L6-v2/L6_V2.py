import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

genai.configure(api_key="AIzaSyDPH5O8RY31uu0MDs5fPctNKmfXeACNfJA")

def classify_question(question):
    prompt = (
        "This is an online course on Machine Learning. Your task is to classify the given question as 'Vague' or 'Clear'.\n\n"
        "1. If the question is 'Clear', simply return: 'Clear'.\n"
        "2. If the question is 'Vague', return: 'Vague' followed by a clear reason explaining *why* it is vague "
        "and *how* the student can improve it.\n\n"
        f"Question: {question}\n\n"
        "Response:"
    )

    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    
    return response.text.strip()


# Load the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
index_file = "lecture_embeddings.index"
sentences_file = "sentences.txt"

def load_sentences(file_path):
    with open(file_path, 'r') as file:
        sentences = [line.strip() for line in file if line.strip()]
    return sentences

lecture_sentences = load_sentences(sentences_file)

print("Loading existing FAISS index...")
faiss_index = faiss.read_index(index_file)

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