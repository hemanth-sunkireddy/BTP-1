from transformers import pipeline
from tqdm import tqdm

qg_pipeline = pipeline("text2text-generation", model="valhalla/t5-base-qg-hl")

input_file = "sentences.txt"
output_file = "generated_questions.txt"

with open(input_file, "r", encoding="utf-8") as file:
    sentences = [line.strip() for line in file if line.strip()]

with open(output_file, "w", encoding="utf-8") as out_file:
    for sentence in tqdm(sentences, desc="Generating Questions", unit="sentence"):
        questions = qg_pipeline(sentence, max_length=128, num_return_sequences=1)
        for q in questions:
            out_file.write(q["generated_text"] + "\n")  # Write each question on a new line

print("Question generation complete! Questions saved in 'generated_questions.txt'.")
