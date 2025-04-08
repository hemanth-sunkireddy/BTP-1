from sentence_transformers import CrossEncoder

# Load the model
model = CrossEncoder("cross-encoder/nli-deberta-v3-base")

question = "What are you?"
labels = ["clear", "not clear"]

# Convert the question into a pairwise classification format
pairs = [(question, label) for label in labels]

# Get scores (higher score means stronger relation)
scores = model.predict(pairs)

# Ensure we extract scalar values
clarity_score, unclear_score = map(float, scores)

# Display scores in a simple format
print(f"Clarity Score: {clarity_score:.2f}")
print(f"Unclear Score: {unclear_score:.2f}")
