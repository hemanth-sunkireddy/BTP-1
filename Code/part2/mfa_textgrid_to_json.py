import json
import re

def parse_text_file(file_path):
    data = []
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    intervals = re.findall(r'xmin = ([\d\.]+)\s+xmax = ([\d\.]+)\s+text = "(.*?)"', content, re.DOTALL)
    
    for xmin, xmax, text in intervals:
        text = text.strip()
        if text:  # Only add non-empty text entries
            data.append({
                "text": text,
                "start": float(xmin),
                "end": float(xmax)
            })
    
    return data

def save_to_json(data, output_path):
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage
input_file = "text/mfa_audio_2.txt"  # Change this to your actual file path
output_file = "text/audio_2_only_words_mfa.json"
data = parse_text_file(input_file)
save_to_json(data, output_file)

print("JSON file created successfully.")
