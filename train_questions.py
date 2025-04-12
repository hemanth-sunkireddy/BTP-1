import numpy as np
from sentence_transformers import SentenceTransformer

# Load the model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Load the dataset
questions_file = "generated_questions.txt"
questions = [line.strip() for line in open(questions_file, "r") if line.strip()]

# Encode all questions
question_embeddings = np.array(model.encode(questions)).astype("float32")

# Save embeddings and questions
np.save("Data/questions_embeddings.npy", question_embeddings)
with open("questions_list.txt", "w") as f:
    f.write("\n".join(questions))

print("Embeddings saved successfully!")
