
# import streamlit as st
# import pysrt
# import base64
# import json
# import os

# # --- Load and encode the video ---
# def get_video_base64(video_path):
#     with open(video_path, 'rb') as f:
#         video_bytes = f.read()
#         encoded = base64.b64encode(video_bytes).decode()
#         return f"data:video/mp4;base64,{encoded}"

# # --- Parse SRT subtitles into dict format ---
# def parse_srt_to_dict(subs):
#     js_subs = []
#     for sub in subs:
#         start = sub.start.ordinal / 1000  # milliseconds to seconds
#         end = sub.end.ordinal / 1000
#         text = sub.text.replace('\n', ' ').replace('"', '\\"')
#         js_subs.append({'start': start, 'end': end, 'text': text})
#     return js_subs

# # --- Inputs ---
# video_path = "video1.mp4"
# srt_path = "1.srt"

# st.title("AI Video Answer System")

# question = st.text_input("Ask your question:")

# if question:
#     if not os.path.exists(video_path) or not os.path.exists(srt_path):
#         st.error("Video or subtitle file not found.")
#     else:
#         video_data_url = get_video_base64(video_path)
#         subs = pysrt.open(srt_path)
#         js_subs = parse_srt_to_dict(subs)
#         js_subs_json = json.dumps(js_subs)

#         st.markdown("### Video Answer:")

#         custom_html = f"""
#         <div style="text-align: center;">
#             <video id="video" width="700" controls>
#                 <source src="{video_data_url}" type="video/mp4">
#                 Your browser does not support the video tag.
#             </video>

#             <div id="subtitle-box" style="
#                 margin-top: 15px;
#                 font-size: 20px;
#                 font-weight: 500;
#                 background: #eee;
#                 padding: 10px;
#                 border-radius: 10px;
#                 min-height: 40px;
#                 color: #333;
#                 width: 700px;
#                 margin: 10px auto 0 auto;
#             ">Loading subtitles...</div>
#         </div>

#         <script>
#         const subtitles = {js_subs_json};

#         const video = document.getElementById('video');
#         const subtitleBox = document.getElementById('subtitle-box');

#         video.addEventListener('timeupdate', function () {{
#             const currentTime = video.currentTime;
#             const current = subtitles.find(s => currentTime >= s.start && currentTime <= s.end);
#             subtitleBox.innerText = current ? current.text : "";
#         }});
#         </script>
#         """

#         # Display the video with synced subtitles
#         st.components.v1.html(custom_html, height=600)


import streamlit as st
import pysrt
import base64
import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from video_sticher import stitch_video_from_segments
import csv
# import es_main
import pickle
import subprocess
import json

# Load the model and FAISS index
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
faiss_index = faiss.read_index("../Data/sentence_embeddings.index")


# Load embeddings and questions
question_embeddings = np.load("../Data/questions_embeddings.npy")



# Load lecture sentences
with open('../Data/sentences.txt', 'r') as file:
    lecture_sentences = file.readlines()
lecture_sentences = [line.strip() for line in lecture_sentences if line.strip()]

lecture_data = []
with open('../Data/srt-embedding-metadata.tsv', 'r', encoding='utf-8') as file:
    tsv_reader = csv.reader(file, delimiter='\t')
    for row in tsv_reader:
        if len(row) == 3:
            filename, timestamp, sentence = row
            lecture_data.append((filename.strip(), timestamp.strip(), sentence.strip()))


# --- Load and encode the video ---
def get_video_base64(video_path):
    with open(video_path, 'rb') as f:
        video_bytes = f.read()
        encoded = base64.b64encode(video_bytes).decode()
        return f"data:video/mp4;base64,{encoded}"

# --- Parse SRT subtitles into dict format ---
def parse_srt_to_dict(subs):
    js_subs = []
    for sub in subs:
        start = sub.start.ordinal / 1000  # milliseconds to seconds
        end = sub.end.ordinal / 1000
        text = sub.text.replace('\n', ' ').replace('"', '\\"')
        js_subs.append({'start': start, 'end': end, 'text': text})
    return js_subs

# --- Inputs ---
video_path = "stitched_output.mp4"
srt_path = "stitched_output.srt"

st.title("AI Video Answer System")
st.set_page_config(layout="wide")

question = st.text_input("Ask your question:")

def is_question_clear(query):
    """Check if a given question is clear based on similarity to existing questions."""
    query_embedding = model.encode([query]).astype("float32")
    similarities = cosine_similarity(query_embedding, question_embeddings)[0]
    
    max_similarity = np.max(similarities)  # Get highest similarity score
    return max_similarity >= 0.7, max_similarity

if question:
    question_embedding = np.array(model.encode([question])).astype('float32')
    # Search all sentences (max number can be total sentences in the index)
    distances, indices = faiss_index.search(question_embedding, len(lecture_sentences))

   
    
    is_clear, similarity_score = is_question_clear(question)
    if not is_clear:
        st.warning("The question is not related to the course. Please input a question related to the course content.")



    # Define a distance threshold (lower means more similar)
    distance_threshold = 0.7

    related_sentences = []
    related_results = []
    for j in range(len(indices[0])):
        i = indices[0][j]
        distance = distances[0][j]
        sentence = lecture_sentences[i]
        
        # Check if the sentence is below the distance threshold and is not a question
        if distance > 0 and distance <= distance_threshold and not sentence.strip().endswith('?'):
            related_sentences.append((sentence, distance))
            filename, timestamp, _ = lecture_data[i+1]
            related_results.append((filename, timestamp, sentence, distance))

    # with open('../extractive_summarization/data/related_results.pkl', 'wb') as f:
    #     pickle.dump(related_results, f)
    
    related_results = [
    (file, timestamp, text)
    for file, timestamp, text, _ in related_results
]
    with open('../extractive_summarization/data/related_results.json', 'w', encoding='utf-8') as f:
        json.dump(related_results, f, ensure_ascii=False, indent=2)

    
    # # Extractive Summarization
    # es_main.clear_files()
    # es_main.write_sentences_to_file(related_results, filename='../extractive_summarization/data/my_data.txt')
    # sentence_dict=es_main.convert_to_sentence_dict(related_results)
    # es_main.generate_extractive_summary()
    # summary_results=es_main.reconstruct_tuples_from_file('../extractive_summarization/data/my_extractive_summary.txt', sentence_dict)
    subprocess.run(["/home/sujal/miniconda3/envs/es_env/bin/python", "es_main.py"])
    
    # with open('../extractive_summarization/data/summary_results.pkl', 'rb') as f:
    #     summary_results = pickle.load(f)
        
    with open('../extractive_summarization/data/summary_results.json', 'r', encoding='utf-8') as f:
        summary_results = json.load(f)

    summary_results = [tuple(entry) for entry in summary_results]


    # stitch_video_from_segments(related_results)
    # stitch_video_from_segments(related_results,transition_type="fade_through_black",apply_transitions=False)
    stitch_video_from_segments(summary_results,pause_duration=1.0)
    if not os.path.exists(video_path) or not os.path.exists(srt_path):
        st.error("Video or subtitle file not found.")
    else:
        video_data_url = get_video_base64(video_path)
        subs = pysrt.open(srt_path)
        js_subs = parse_srt_to_dict(subs)
        js_subs_json = json.dumps(js_subs)

        st.markdown("### Video Answer:")

        custom_html = f"""
        <!-- Video -->
        <video id="video" controls>
            <source src="{video_data_url}" type="video/mp4">
            Your browser does not support the video tag.
        </video>

        <!-- Live subtitle box -->
        <div id="subtitle-box" style="
            font-size: 18px;
            font-weight: bold;
            background: #eef2f3;
            padding: 10px;
            border-radius: 8px;
            min-height: 30px;
            color: #333;
            text-align: center;
            margin-bottom: 10px;
        "></div>

        <!-- Scrollable subtitle list -->
        <div id="subtitle-list" style="
            height: 200px;
            background: yellow;
            border-radius: 10px;
            padding: 10px;
            border: 1px solid #ccc;
            font-family: sans-serif;
            font-size: 16px;
        ">
            <!-- Populated by JS -->
        </div>

        <script>
        const subtitles = {js_subs_json};
        const video = document.getElementById("video");
        const subtitleBox = document.getElementById("subtitle-box");
        const subtitleList = document.getElementById("subtitle-list");

        // Populate the subtitle list
        subtitleList.innerHTML = subtitles.map((sub, i) => `
        <div class="subtitle-line" id="sub-${{i}}" data-start="${{sub.start}}" data-end="${{sub.end}}" style="
            padding: 6px 8px;
            margin-bottom: 5px;
            border-radius: 5px;
            transition: all 0.3s ease;
        ">${{sub.text}}</div>
        `).join("");

        video.addEventListener("timeupdate", () => {{
        const currentTime = video.currentTime;
        let activeIndex = -1;

        subtitles.forEach((sub, i) => {{
            const line = document.getElementById("sub-" + i);
            if (currentTime >= sub.start && currentTime <= sub.end) {{
            line.style.backgroundColor = "#d1eaff";
            line.style.fontWeight = "bold";
            subtitleBox.innerText = sub.text;
            activeIndex = i;
            }} else {{
            line.style.backgroundColor = "";
            line.style.fontWeight = "normal";
            }}
        }});

        if (activeIndex >= 0) {{
            const activeLine = document.getElementById("sub-" + activeIndex);
            const container = document.getElementById("subtitle-list");
            const offsetTop = activeLine.offsetTop - container.offsetTop - container.clientHeight / 2 + activeLine.clientHeight / 2;
            container.scrollTop = offsetTop;
        }}
        }});
        </script>
        """
        st.components.v1.html(custom_html, width=1500, height=900)