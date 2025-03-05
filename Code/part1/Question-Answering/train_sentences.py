import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import re

# Initialize Sentence-BERT model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Function to extract sentences from .vtt file
def extract_sentences_from_vtt(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    sentences = []
    skip_next = False
    for line in lines:
        line = line.strip()
        # Skip empty lines and timestamp lines
        if not line or re.match(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}', line):
            continue
        # Skip lines with only numbers (cue identifiers)
        if line.isdigit():
            continue
        sentences.append(line)
    return sentences

# Process lecture.vtt file
vtt_file = 'lecture1.vtt'
lecture_sentences = extract_sentences_from_vtt(vtt_file)

# Encode sentences into embeddings
sentence_embeddings = np.array(model.encode(lecture_sentences)).astype('float32')

# Create FAISS index
embedding_dimension = sentence_embeddings.shape[1]
faiss_index = faiss.IndexFlatL2(embedding_dimension)
faiss_index.add(sentence_embeddings)

# Save FAISS index and processed sentences
faiss.write_index(faiss_index, "lecture_embeddings.index")
with open('processed_lecture_sentences.txt', 'w') as file:
    file.write('\n'.join(lecture_sentences))

print(f"Embeddings created for {len(lecture_sentences)} sentences from {vtt_file}.")