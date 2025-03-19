from transformers import pipeline

qg_pipeline = pipeline("text2text-generation", model="valhalla/t5-base-qg-hl")


with open("sentences.txt", "r", encoding="utf-8") as file:
    sentences = file.readlines()


output_questions = []
for sentence in sentences:
    sentence = sentence.strip()
    if sentence:
        questions = qg_pipeline(sentence, max_length=128, num_return_sequences=1)
        print(questions)
        output_questions.append(f"Sentence: {sentence}")
        for idx, q in enumerate(questions, 1):
            output_questions.append(f"Q{idx}: {q['generated_text']}")
        output_questions.append("")


with open("generated_questions.txt", "w", encoding="utf-8") as output_file:
    output_file.write("\n".join(output_questions))

print("Question generation complete! Questions saved in 'generated_questions.txt'.")
