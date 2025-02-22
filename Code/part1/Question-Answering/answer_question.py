import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

faiss_index = faiss.read_index("lecture_embeddings.index")

with open('processed_lecture_sentences.txt', 'r') as file:
    lecture_sentences = file.readlines()
lecture_sentences = [line.strip() for line in lecture_sentences]

student_question = input("Enter your question: ")
question_embedding = np.array(model.encode([student_question])).astype('float32')

top_k_similar_sentences = 2
distances, indices = faiss_index.search(question_embedding, top_k_similar_sentences)

print("\nTop-k similar sentences:")
for rank, sentence_index in enumerate(indices[0]):
    print(f"Rank {rank + 1}: {lecture_sentences[sentence_index]} (Distance Similarity: {distances[0][rank]:.4f})")
