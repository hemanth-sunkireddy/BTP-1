## Related Information
* A mono audio file has 1 channel, while a stereo audio file has 2 channels.
* We are using sample rate of 16000 Hz for our project and 1 channel `.wav` file.

### Frame:
* A frame is a small window or block of audio data that you process at a time. 
* It typically represents a slice of audio data, usually around 20-30 milliseconds in duration.
* frame_duration_ms = 30 in `webrtc.py`.

* The frame_generator function slices the raw audio data into frames of equal length (in this case, 30ms), and each frame is passed to the VAD to check if speech is detected.
Frame Duration: The duration of each frame is crucial because too short or too long frames can affect VAD performance. For speech detection, typically, frames of 10-30ms are used.

### Chunk:
* A chunk refers to a sequence of frames that are grouped together. In the context of your code, after speech is detected, a chunk is essentially the collection of frames that are continuously classified as containing speech.
* A chunk can vary in length depending on the audio being processed and the settings of the VAD. You can think of chunks as "continuous sections of speech" between silences.

### Segment:
* A segment is a longer portion of the audio that represents a piece of speech, with chunks of speech data that have been detected together.
* A segment can consist of multiple chunks, where chunks are continuous frames of detected speech. After collecting the chunks, you combine them to form a segment.


## WebRTC Algorithm
we will use **PyWebRTC model**.
1. Install Py-WebRTC
    `pip install webrtcvad`
2. Run
    `python3 webrtc.py <aggressiveness> <path to wav file>`
<!-- 3. The Generated output will be `silence_remove.wav` -->

* set its aggressiveness mode, which is an integer between 0 and 3. 0 is the least aggressive about filtering out non-speech, 3 is the most aggressive.
* Give it a short segment ("frame") of audio.
* We are using frame duration is 30ms.
* And also for every chunk we are adding padding duration of 300ms = 0.3sec.
* The WebRTC VAD only accepts:
    * 16-bit mono PCM audio.
    * sampled at 8000, 16000, 32000 or 48000 Hz. 
    * A frame must be either 10, 20, or 30 ms in duration.


## Observations:
1. WebRTC algorithm removes Silence Part but includes speech and noise parts.
2. Silero-VAD Algorithm removes Both Silence and Noise Parts.

## Dividing Large Audio files into smaller chunks
1. Speech boundaries (Sentence structure along with punctuation or Pause-based)
    * If the speech contains noticeable pauses (silent gaps between sentences), we'll set a threshold for the duration of the pause that qualifies as a sentence boundary.
    * Then combine smaller chunks into their nearest chunks with monitoring max and min durations of the audio file.
    * If there is a pause then remove in between the sentences. And add small padding silence at both ends of the remaining audio at that window.



### NLP Models
1. all-MiniLM-L6-v2 is a distilled model (~22M parameters) and small model — works with L2 distance (lower value = more similar).
2. bge-base-en-v1.5 is a more accurate model (~450M parameters) — it gives similarity scores directly (higher value = more similar).
3. MiniLM embeddings are not strictly normalized by default (~22M size), so cosine similarity can vary, and many implementations approximate it with L2 distance.
4. BGE-base embeddings (~450M size) should be normalized to unit vectors, so that dot product between embeddings corresponds to cosine similarity.
5. Threshold for all-miniLM-L6-v2 we kept as 0.7 after analysing few QA.