import json
import argparse
from transformers import BertTokenizer, BertModel
import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def encode_sentences(sentences, tokenizer, model):
    encoded = []
    for sent in sentences:
        inputs = tokenizer.encode_plus(sent, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)  # tuple output in older versions
        # Extract CLS token (first token) from last_hidden_state
        last_hidden_state = outputs[0]  # outputs[0] is last_hidden_state
        cls_embedding = last_hidden_state[0][0]  # [batch_idx=0][CLS]
        encoded.append(cls_embedding.numpy())
    return np.vstack(encoded)

def select_topk_sentences(sentences, k=5):
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased")
    model.eval()

    if len(sentences) <= k:
        return list(range(len(sentences)))

    # Encode all sentences
    sentence_vectors = encode_sentences(sentences, tokenizer, model)

    # Compute cosine similarity to the centroid
    centroid = np.mean(sentence_vectors, axis=0, keepdims=True)
    sims = cosine_similarity(sentence_vectors, centroid).flatten()

    # Pick top-k sentences
    topk_indices = sims.argsort()[-k:][::-1]
    return sorted(topk_indices.tolist())

def main(args):
    index_data = []

    with open(args.input_jsonl, "r", encoding="utf-8") as f:
        for line in f:
            doc = json.loads(line)
            sentences = doc.get("text", [])
            topk_ids = select_topk_sentences(sentences, args.k)
            index_data.append({"sent_id": topk_ids})

    with open(args.output_index, "w", encoding="utf-8") as out_f:
        for entry in index_data:
            out_f.write(json.dumps(entry) + "\n")

    print(f"Generated index file with top-{args.k} sentences per document.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_jsonl", type=str, required=True,
                        help="Path to input JSONL with documents.")
    parser.add_argument("--output_index", type=str, required=True,
                        help="Path to save output index.jsonl.")
    parser.add_argument("--k", type=int, default=5,
                        help="Number of top sentences to select per document.")
    args = parser.parse_args()
    main(args)
