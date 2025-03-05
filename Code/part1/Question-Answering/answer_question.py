import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the model and FAISS index
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
faiss_index = faiss.read_index("lecture_embeddings.index")

# Load lecture sentences
with open('processed_lecture_sentences.txt', 'r') as file:
    lecture_sentences = file.readlines()
lecture_sentences = [line.strip() for line in lecture_sentences if line.strip()]

# Get student's question
student_question = input("Enter your question: ")
question_embedding = np.array(model.encode([student_question])).astype('float32')

# Search all sentences (max number can be total sentences in the index)
distances, indices = faiss_index.search(question_embedding, len(lecture_sentences))

# Define a distance threshold (lower means more similar)
distance_threshold = 0.9

# Filter sentences based on the threshold
related_sentences = [(lecture_sentences[i], distances[0][j]) for j, i in enumerate(indices[0]) if distances[0][j] <= distance_threshold]

# Display related sentences
print("\nSentences within threshold:")
for rank, (sentence, distance) in enumerate(related_sentences, 1):
    print(f"Rank {rank}: {sentence} (Distance Similarity: {distance:.4f})")

print(f"\nFound {len(related_sentences)} related sentences.")
