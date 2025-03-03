import json

# Load the input JSON file
with open("text/audio_3.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract words from segments
words_list = []
for segment in data.get("segments", []):
    words_list.extend(segment.get("words", []))

# Save the extracted words to a new JSON file
with open("text/audio_3_only_words.json", "w", encoding="utf-8") as file:
    json.dump(words_list, file, indent=4)