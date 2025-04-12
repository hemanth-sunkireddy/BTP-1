import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer



# Load the model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
index_file = "Data/sentence_embeddings.index"
sentences_file = "Data/sentences.txt"

def load_sentences(file_path):
    with open(file_path, 'r') as file:
        sentences = [line.strip() for line in file if line.strip()]
    return sentences

lecture_sentences = load_sentences(sentences_file)

print("Loading existing FAISS index...")
faiss_index = faiss.read_index(index_file)

