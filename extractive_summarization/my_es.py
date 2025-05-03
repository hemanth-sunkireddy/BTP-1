import json
import torch
import numpy as np
import argparse
from model import MatchSum  # Import the model class from your repository's model.py
from transformers import BertTokenizer, RobertaTokenizer

def load_processed_data(processed_path):
    """Loads the processed JSONL file produced by get_candidate.py."""
    data = []
    with open(processed_path, "r") as f:
        for line in f:
            data.append(json.loads(line))
    return data

def to_tensor(batch):
    # Assumes batch is a 3D list: [batch_size, candidate_num, seq_len]
    if isinstance(batch[0][0], list):  # candidate_id case
        max_len = max(len(seq) for doc in batch for seq in doc)
        padded = [[[token for token in seq] + [0] * (max_len - len(seq)) for seq in doc] for doc in batch]
        return torch.tensor(padded, dtype=torch.long)
    else:  # text_id or summary_id case (1D list inside batch)
        max_len = max(len(seq) for seq in batch)
        padded = [seq + [0] * (max_len - len(seq)) for seq in batch]
        return torch.tensor(padded, dtype=torch.long)


def infer_document(model, data_item, device):
    """
    Runs model inference on a single document.
    data_item: a dict from the processed JSONL file containing:
        - 'text_id': tokenized document (list of ints)
        - 'candidate_id': list of candidate token id sequences (each a list of ints)
        - 'summary_id': tokenized summary (list of ints, dummy if not available)
    Returns the index (in candidate_id) of the candidate selected by the model.
    """
    text_ids = data_item["text_id"]
    candidate_ids = data_item["candidate_id"]
    summary_ids = data_item["summary_id"]

    # Convert to tensors and add batch dimension.
    text_tensor = to_tensor([text_ids]).to(device)                # Shape: [1, seq_len]
    candidate_tensor = to_tensor([candidate_ids]).to(device)        # Shape: [1, candidate_num, seq_len]
    summary_tensor = to_tensor([summary_ids]).to(device)            # Shape: [1, seq_len]

    model.eval()
    with torch.no_grad():
        output = model(text_tensor, candidate_tensor, summary_tensor)
    # output['score'] is of shape [1, candidate_num].
    scores = output["score"].squeeze(0).cpu().numpy()  # Now shape: [candidate_num]
    best_index = int(np.argmax(scores))
    return best_index, scores

def reconstruct_summary(data_item, candidate_index):
    """
    Reconstructs the extractive summary as a string using the candidate indices.
    data_item: processed document containing 'indices' and 'text'.
    candidate_index: index into data_item['indices'] corresponding to the best candidate.
    """
    # data_item["indices"] is a list of candidate groups (list of sentence indices).
    candidate_group = data_item["indices"][candidate_index]
    # Reassemble summary by fetching the original sentences.
    summary_sentences = [data_item["text"][i] for i in candidate_group]
    return "\n".join(summary_sentences)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--processed_data", type=str, required=True,
                        help="Path to the processed JSONL file produced by get_candidate.py")
    parser.add_argument("--ckpt", type=str, required=True,
                        help="Path to the pre-trained checkpoint (e.g., MatchSum_cnndm_bert.ckpt or roberta.ckpt)")
    parser.add_argument("--encoder", type=str, required=True,
                        choices=["bert", "roberta"], help="Select encoder: 'bert' or 'roberta'")
    args = parser.parse_args()

    # Set up device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Load pre-trained model checkpoint.
    model = torch.load(args.ckpt, map_location=device)
    model = model.to(device)
    model.eval()

    # Load processed candidate data.
    data = load_processed_data(args.processed_data)
    # print("Loaded {} documents.".format(len(data)))

    all_summaries = []
    for i, item in enumerate(data):
        best_index, scores = infer_document(model, item, device)
        summary_text = reconstruct_summary(item, best_index)
        all_summaries.append(summary_text)
        # print("Doc {}: Best candidate index: {}, Score: {:.4f}".format(i, best_index, scores[best_index]))
        # print("Extractive Summary:", summary_text)
        # print("-" * 80)

    # Write the extractive summaries to a file.
    with open("../extractive_summarization/data/my_extractive_summary.txt", "w") as f:
        for summary in all_summaries:
            f.write(summary + "\n")

if __name__ == "__main__":
    main()
