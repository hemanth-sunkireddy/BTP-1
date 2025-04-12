import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import re
import os
from tqdm import tqdm  # ✅ Import tqdm for progress bar

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

        # Check for timestamp lines
        timestamp_match = re.match(r'(\d{2}:\d{2}:\d{2}[.,]\d{3}) --> (\d{2}:\d{2}:\d{2}[.,]\d{3})', line)
        if timestamp_match:
            current_timestamp = timestamp_match.group(1).replace(',', '.') + ' --> ' + timestamp_match.group(2).replace(',', '.')
            continue

        # Skip empty lines and cue identifiers
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
srt_dir = 'Data/SRT-Files'

# Initialize lists for all sentences, timestamps, and filenames
all_sentences = []
all_timestamps = []
all_filenames = []

# Process all SRT files with tqdm
srt_files = [f for f in os.listdir(srt_dir) if f.endswith('.srt')]
for file_name in tqdm(srt_files, desc="📂 Processing SRT files"):
    file_path = os.path.join(srt_dir, file_name)
    sentences, timestamps = extract_sentences_from_srt(file_path)
    all_sentences.extend(sentences)
    all_timestamps.extend(timestamps)
    all_filenames.extend([file_name] * len(sentences))  # associate each sentence with its file

# Encode sentences into embeddings
print("🧠 Encoding sentences into embeddings...")
sentence_embeddings = np.array(model.encode(all_sentences)).astype('float32')

# Create FAISS index
embedding_dimension = sentence_embeddings.shape[1]
faiss_index = faiss.IndexFlatL2(embedding_dimension)
faiss_index.add(sentence_embeddings)

# Save FAISS index
faiss.write_index(faiss_index, "Data/sentence_embeddings.index")

# Save metadata to file
metadata_path = 'Data/srt-embedding-metadata.tsv'
with open(metadata_path, 'w', encoding='utf-8') as file:
    file.write("filename\ttimestamp\tsentence\n")
    for fname, timestamp, sentence in zip(all_filenames, all_timestamps, all_sentences):
        clean_sentence = sentence.replace('\t', ' ').replace('\n', ' ')
        file.write(f"{fname}\t{timestamp}\t{clean_sentence}\n")

# ✅ Save sentences to a text file
sentences_txt_path = 'Data/sentences.txt'
with open(sentences_txt_path, 'w', encoding='utf-8') as file:
    for sentence in all_sentences:
        file.write(sentence.strip().replace('\n', ' ') + '\n')

# ✅ Summary
print(f"\n✅ Embeddings created for {len(all_sentences)} sentences from {len(srt_files)} SRT files.")
print("💾 FAISS index saved as 'Data/lecture_embeddings.index'")
print(f"📝 Metadata saved as '{metadata_path}'")
print(f"📄 Sentences saved as '{sentences_txt_path}'")
