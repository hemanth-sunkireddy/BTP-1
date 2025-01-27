# Tasks
* Extraction of Audios from Videos and Run the VAD algorithm. [Implemented Silero and WebRTC algorithms]
* Run the VAD algorithm on our extracted audios and plot those with VAD decisions.

## Helpful Content
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
