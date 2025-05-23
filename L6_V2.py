import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the model and FAISS index
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
faiss_index = faiss.read_index("Data/sentence_embeddings.index")

# Load lecture sentences
with open('Data/sentences.txt', 'r') as file:
    lecture_sentences = file.readlines()
lecture_sentences = [line.strip() for line in lecture_sentences if line.strip()]

# Get student's question
student_question = input("Enter your question: ")
question_embedding = np.array(model.encode([student_question])).astype('float32')

# Search all sentences (max number can be total sentences in the index)
distances, indices = faiss_index.search(question_embedding, len(lecture_sentences))

# Define a distance threshold (lower means more similar)
distance_threshold = 0.7

related_sentences = []
for j in range(len(indices[0])):
    i = indices[0][j]
    distance = distances[0][j]
    sentence = lecture_sentences[i]
    
    # Check if the sentence is below the distance threshold and is not a question
    if distance > 0 and distance <= distance_threshold and not sentence.strip().endswith('?'):
        related_sentences.append((sentence, distance))


# Display related sentences with distances
print("\n Related Sentences:")
for sentence, distance in related_sentences:
    print(f"- {sentence} - {distance:.4f}")