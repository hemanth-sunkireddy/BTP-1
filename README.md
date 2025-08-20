# BTP 1 - Automatic multimodal question and answering for video lectures

**Presentation:** [Canva](https://www.canva.com/design/DAGhsnSEdRo/IxsYfXwTJMAf6B7icCmBbQ/view?utm_content=DAGhsnSEdRo&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hb2715aa87e)

**Demo:** [Youtube](https://www.youtube.com/watch?v=EWW-C-lGbvo)

**Dataset:** [Coursera Website](https://www.coursera.org/learn/introduction-to-machine-learning-supervised-learning/home/week/1)

## Project description
This work involves synthesizing a video from a set of video lectures that answers the question raised by the student. This contains following objectives.
1. Select a video lectures set that containing SRTs.
2. Study and implement the voice activity detection (VAD) algorithm.
3. Extract the speech segments from the VAD output.
4. Identify the spoken content in text form using ASR for each segment.
5. Obtain the sentence specific time stamps.
6. Create answer summary.
7. Identify video parts corresponding to the answer summary.
8. Stitch the summary video segments to obtain natural like video.

## Guide
Chiranjeevi Yarra (Spoken Language Forensics & Informatics (SLFI) group - LTRC)

## Running in Local
### Prerequisities
1. FFMPEG:  `pip3 install ffmpeg-python`
2. PyTorch: `pip3 install torch torchvision`
3. Transformers: ` pip3 install transformers`
4. Sentence Transfomers: `pip3 install -U sentence-transformers`
5. Faiss: `pip3 install faiss-cpu`
6. Silero VAD: `pip3 install silero-vad`
7. SoundFile: `pip3 install soundfile`
8. Sox: `pip3 install sox`
9. Streamlit: `pip3 install streamlit`
10. pysrt: `pip3 install pysrt`
11. moviepy: `pip3 install moviepy==1.0.3`

* Note: We require `ffmpeg` in system also.
So please install through `apt install ffmpeg` (Linux) or `brew install ffmpeg` (Mac)

### Steps
1. Place the input videos inside this folder `Data/Videos` with naming as `1.mp4 2.mp4 ....`
2. Run `video-to-audio-converter.py` file.
3. Output Audio files in `Data/Audios` directory.
4. Now run `voice-activity-detection.ipynb` file.
5. Output Audio Chunk files in `Data/Audio-Chunks` directory.

7. Now place SRT files in `Data/SRT-Files` directory.
8. Run `srt_to_embeddings.ipynb` file.
9. Output Sentences generated in `sentences.txt`, embeddings of sentences in `sentence_embeddings.index` and 
    related mapping in `srt-embedding-metadata.tsv` file.
10. Run `QA.ipynb` to get related sentences and corresponding video number for the question.
---

## Audio Configuration

- Sample Rate: **16000 Hz** (you can change it to 32000 Hz in the script)
- Channels: **1 (Mono)**
- Codec: **PCM 16-bit**
- Bit Rate: ~256 kbps (may vary)
---

# Voice Activity Detection
* Converting Audio into smaller chunks - Removing Silent Portions - Silero VAD Algorithm

1. Run `silero-vad.ipynb` file.
2. Output Audio Chunks will be generated automatically in `Data/Audio-Chunks` folder



## Question Classifier Output
![Classify Question Image](assets/Classify-Question.png)

## Finding Related Sentences for Question Output
![Related Sentences output](assets/Related-Sentences-Output.png)

## Voice Activity Detector Output
![Voice Activity Detector Output](assets/Voice-Activity-Detector-Output.png)
