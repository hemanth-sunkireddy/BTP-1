import json
import argparse

def convert_text_to_jsonl(input_file, output_file):
    """
    Reads a text file containing one sentence per line and outputs
    a JSONL file with one document. Each document is represented by:
      - "text": a list of sentences
      - "summary": an empty list (or you can add a dummy summary if desired)
    """
    with open(input_file, "r", encoding="utf-8") as f:
        # Read all lines, stripping any extra whitespace/newlines.
        sentences = [line.strip() for line in f if line.strip()]

    # Prepare the document dictionary. If you have a gold summary add it;
    # otherwise, use an empty list.
    document = {
        "text": sentences,
        "summary": []  # or you could use [""] if a non-empty value is required
    }

    # Write as one JSON object per line (here only one document).
    with open(output_file, "a", encoding="utf-8") as out_f:
        out_f.write(json.dumps(document) + "\n")

    print(f"Converted {len(sentences)} sentences into {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert a text file (one sentence per line) into a JSONL file."
    )
    parser.add_argument("--input_file", type=str, required=True,
                        help="Path to the input text file containing sentences.")
    parser.add_argument("--output_file", type=str, required=True,
                        help="Path to save the output JSONL file.")

    args = parser.parse_args()
    convert_text_to_jsonl(args.input_file, args.output_file)
