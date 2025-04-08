import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Load embeddings and questions
question_embeddings = np.load("questions_embeddings.npy")
with open("questions_list.txt", "r") as f:
    questions = [line.strip() for line in f if line.strip()]

def is_question_clear(query):
    """Check if a given question is clear based on similarity to existing questions."""
    query_embedding = model.encode([query]).astype("float32")
    similarities = cosine_similarity(query_embedding, question_embeddings)[0]
    
    max_similarity = np.max(similarities)  # Get highest similarity score
    return max_similarity >= 0.7, max_similarity

# Example usage
test_question = "What is a multilinear regression model?"
clear, similarity_score = is_question_clear(test_question)

if clear:
    print(f"✅ The question is clear (Similarity: {similarity_score:.2f})")
else:
    print(f"❌ The question is unclear (Similarity: {similarity_score:.2f})")
