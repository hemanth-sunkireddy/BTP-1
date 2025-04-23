import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# Example usage
test_question = "What is Data Systems?"
clear, similarity_score = is_question_clear(test_question)

if clear:
    print(f"✅ The question is clear (Similarity: {similarity_score:.2f})")
else:
    print(f"❌ The question is unclear (Similarity: {similarity_score:.2f})")
