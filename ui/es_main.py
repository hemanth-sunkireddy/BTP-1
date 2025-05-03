import subprocess
import os
import numpy as np
import pickle
import json

def generate_extractive_summary():
    txt_path = "../extractive_summarization/data/my_data.txt"
    jsonl_path = "../extractive_summarization/data/my_data.jsonl"
    index_path = "../extractive_summarization/data/my_index.jsonl"
    processed_data_path = "../extractive_summarization/data/processed_data.jsonl"
    summary_model_ckpt = "../extractive_summarization/roberta/MatchSum_cnndm_roberta.ckpt"
    encoder_type = "roberta"

    # Step 1: Convert TXT to JSONL
    subprocess.run([
        "/home/sujal/miniconda3/envs/es_env/bin/python", "../extractive_summarization/my_convert_to_json.py",
        "--input_file", txt_path,
        "--output_file", jsonl_path
    ])

    # Step 2: Generate index
    subprocess.run([
        "/home/sujal/miniconda3/envs/es_env/bin/python", "../extractive_summarization/my_generate_index.py",
        "--input_jsonl", jsonl_path,
        "--output_index", index_path,
        "--k", "6"
    ])
    
    subprocess.run([
        "/home/sujal/miniconda3/envs/es_env/bin/python", "../extractive_summarization/preprocess/get_candidate.py",
        "--tokenizer=bert",
        "--data_path", jsonl_path,
        "--index_path", index_path,
        "--write_path", processed_data_path
    ])

    # Step 3: Run extractive summarization
    subprocess.run([
        "/home/sujal/miniconda3/envs/es_env/bin/python", "../extractive_summarization/my_es.py",
        "--processed_data", processed_data_path,
        "--ckpt", summary_model_ckpt,
        "--encoder", encoder_type
    ])

    # Load the result
    summary_file_path = "../extractive_summarization/data/my_extractive_summaries.txt"
    if os.path.exists(summary_file_path):
        # with open(summary_file_path, "r") as f:
        #     return f.read()
        pass
    else:
        return "Summary generation failed or no summary was created."

def write_sentences_to_file(data, filename='my_data.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        for item in data:
            if len(item) >= 3:
                f.write(item[2] + '\n')

def convert_to_sentence_dict(data):
    sentence_dict = {}
    for item in data:
        if len(item) == 3:
            filename, timestamp, sentence = item
            sentence_dict[sentence] = (filename, timestamp)
    return sentence_dict

def reconstruct_tuples_from_file(file_path, sentence_dict):
    reconstructed = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            sentence = line.strip()
            if sentence in sentence_dict:
                filename, timestamp = sentence_dict[sentence]
                reconstructed.append((filename, timestamp, sentence))
            else:
                print(f"Warning: Sentence not found in dictionary - '{sentence}'")
    return reconstructed

def clear_files():
    files_to_clear = ['../extractive_summarization/data/my_data.jsonl', '../extractive_summarization/data/my_index.jsonl', '../extractive_summarization/data/processed_data.jsonl']
    for file_path in files_to_clear:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.truncate(0)
            # print(f"Cleared: {file_path}")
        except Exception as e:
            print(f"Error clearing {file_path}: {e}")


# data=[('1.srt', '00:06:07.960 --> 00:06:12.370', 'As you can see, machine learning is a top skill in the jobs that involves AI skills.', np.float32(0.51018435)),
# ('1.srt', '00:02:55.280 --> 00:03:02.489', 'Machine learning consists of different types of learning, such as supervised learning, unsupervised learning, or reinforcement learning.', np.float32(0.5318663)),
# ('1.srt', '00:03:03.539 --> 00:03:06.799', 'Many machine learning models, they are coming from statistical learning.', np.float32(0.5381143)),
# ('1.srt', '00:00:07.940 --> 00:00:11.130', 'This video will talk about introduction to machine learning.', np.float32(0.5935633)),
# ('1.srt', '00:02:42.550 --> 00:02:48.879', 'So machine learning is part of data science and it is also a subfield of artificial intelligence.', np.float32(0.59998894)),
# ('1.srt', '00:05:36.290 --> 00:05:41.000', 'And here is the Google trend on the term on machine learning and software engineering.', np.float32(0.6220391)),
# ('1.srt', '00:03:07.229 --> 00:03:17.589', 'So machine learning extends the statistical learning by including more complex algorithms, which deal with more complex data and bigger data, and more efficient algorithms.', np.float32(0.6399534)),
# ('1.srt', '00:02:37.450 --> 00:02:42.409', 'Machine learning, we mentioned that machine learning several times during the talk about data science.', np.float32(0.6611352)),
# ('1.srt', '00:13:03.110 --> 00:13:05.670', 'Here are some few examples of machine learning tasks.', np.float32(0.66385615)),
# ('2.srt', '00:01:21.239 --> 00:01:24.949', 'It is one of the simplest kind of supervised learning model.', np.float32(0.67366815)),
# ('1.srt', '00:02:49.840 --> 00:02:54.140', 'It focuses on learning algorithms and building models and training them on the data.', np.float32(0.68865645))]


# write_sentences_to_file(data, './data/my_data.txt')
# my_dict=convert_to_sentence_dict(data)
# print()
# print("dictionary:")
# print(my_dict)
# print()
# reconstructed_data=reconstruct_tuples_from_file('./data/my_data.txt', my_dict)
# print()
# print("reconstructed data:")
# print(reconstructed_data)
# print()

clear_files()

# print("Here 1")
# generate_extractive_summary()
# with open('../extractive_summarization/data/related_results.pkl', 'rb') as f:
#     related_results = pickle.load(f)

with open('../extractive_summarization/data/related_results.json', 'r', encoding='utf-8') as f:
    related_results = json.load(f)

related_results = [tuple(entry) for entry in related_results]
# print("Here 2")

write_sentences_to_file(related_results, filename='../extractive_summarization/data/my_data.txt')
sentence_dict=convert_to_sentence_dict(related_results)
generate_extractive_summary()
summary_results=reconstruct_tuples_from_file('../extractive_summarization/data/my_extractive_summary.txt', sentence_dict)

# print("Here 3")

# with open('../extractive_summarization/data/summary_results.pkl', 'wb') as f:
#     pickle.dump(summary_results, f)
    
with open('../extractive_summarization/data/summary_results.json', 'w', encoding='utf-8') as f:
    json.dump(summary_results, f, ensure_ascii=False, indent=2)

# print("Here 4")
