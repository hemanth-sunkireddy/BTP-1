import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

with open('lecture_sentences.txt', 'r') as file:
    lecture_sentences = file.readlines()
lecture_sentences = [line.strip() for line in lecture_sentences if line.strip()]

sentence_embeddings = np.array(model.encode(lecture_sentences)).astype('float32')

embedding_dimension = sentence_embeddings.shape[1]
faiss_index = faiss.IndexFlatL2(embedding_dimension)
faiss_index.add(sentence_embeddings)

faiss.write_index(faiss_index, "lecture_embeddings.index")

with open('processed_lecture_sentences.txt', 'w') as file:
    file.write('\n'.join(lecture_sentences))

print(f"Embeddings Created for sentences and index created with {len(lecture_sentences)} sentences.")
