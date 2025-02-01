# VAD Algorithm
## Silero VAD
we will use the **Silero Voice Activity Detection (VAD) model** to extract speech from an audio file, removing silent portions.

1. Install Silero VAD:
    `pip install silero-vad`
2. Additional dependencies:
    * **Soundfile:** To handle reading and writing audio files.
        * `pip install soundfile`
    * **Sox:** For audio processing and manipulation.
        * `pip install sox`
3. Run `silero-vad.ipynb` file.
4. Generated output will be `only_speech.wav`


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