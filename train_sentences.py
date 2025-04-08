import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import re
import os

# Initialize Sentence-BERT model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Function to extract combined sentences with timestamps from .srt file
def extract_sentences_from_srt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    sentences = []
    timestamps = []
    current_sentence = ""
    current_timestamp = ""
    
    for line in lines:
        line = line.strip()
        
        # Check for timestamp lines (SRT uses commas for milliseconds)
        timestamp_match = re.match(r'(\d{2}:\d{2}:\d{2}[.,]\d{3}) --> (\d{2}:\d{2}:\d{2}[.,]\d{3})', line)
        if timestamp_match:
            current_timestamp = timestamp_match.group(1).replace(',', '.') + ' --> ' + timestamp_match.group(2).replace(',', '.')
            continue
        
        # Skip empty lines and cue identifiers (lines with only numbers)
        if not line or line.isdigit():
            continue
        
        # Add line to current sentence
        current_sentence += " " + line if current_sentence else line
        
        # If sentence ends, save it
        if re.search(r'[.!?]$', line):
            sentences.append(current_sentence.strip())
            timestamps.append(current_timestamp)
            current_sentence = ""
            current_timestamp = ""
    
    return sentences, timestamps

# Directory containing SRT files
srt_dir = 'complete_srt'

# Initialize lists for all sentences and timestamps
all_sentences = []
all_timestamps = []

# Process all SRT files
for file_name in os.listdir(srt_dir):
    if file_name.endswith('.srt'):
        file_path = os.path.join(srt_dir, file_name)
        sentences, timestamps = extract_sentences_from_srt(file_path)
        all_sentences.extend(sentences)
        all_timestamps.extend(timestamps)

# Encode sentences into embeddings
sentence_embeddings = np.array(model.encode(all_sentences)).astype('float32')

# Create FAISS index
embedding_dimension = sentence_embeddings.shape[1]
faiss_index = faiss.IndexFlatL2(embedding_dimension)
faiss_index.add(sentence_embeddings)

# Save FAISS index, processed sentences, and their timestamps
faiss.write_index(faiss_index, "lecture_embeddings.index")

with open('sentences.txt', 'w', encoding='utf-8') as file:
    for sentence, timestamp in zip(all_sentences, all_timestamps):
        file.write(f"{sentence}\n")

print(f"Embeddings created for {len(all_sentences)} combined sentences from {len(os.listdir(srt_dir))} SRT files.")