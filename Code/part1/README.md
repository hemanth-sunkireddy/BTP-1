## 🎵 Video to Audio Conversion

This script extracts audio from multiple `.mp4` video files and saves them as `.wav` files with specified audio parameters.

---

## ✅ Prerequisites

Make sure you have `ffmpeg-python` installed. You can install it using:

```bash
pip install ffmpeg-python
```

---

## 📂 Input and Output

### 📥 Input
- Folder: `Data/`
- File Type: `.mp4` video files
- Example:
  ```
  Data/
  ├── video1.mp4
  ├── lecture2.mp4
  └── sample3.mp4
  ```

### 📤 Output
- Folder: `audios/` (automatically created if it doesn't exist)
- File Type: `.wav` audio files
- Example:
  ```
  audios/
  ├── video1.wav
  ├── lecture2.wav
  └── sample3.wav
  ```

Each output file corresponds to an input `.mp4` file with the same base filename.

---

## 🛠️ Audio Configuration

- Sample Rate: **16000 Hz** (you can change it to 32000 Hz in the script)
- Channels: **1 (Mono)**
- Codec: **PCM 16-bit**
- Bit Rate: ~256 kbps (may vary)

---

## 🚀 Usage

1. Place your `.mp4` files in the `Data/` folder.
2. Run the script using:

```bash
python3 video_to_audio.py
```

3. Extracted `.wav` files will be saved in the `audios/` folder.
4. The terminal will display details of each extracted audio file (codec, sample rate, duration, etc.).

---

## 📚 Documentation

- ffmpeg-python: [https://kkroening.github.io/ffmpeg-python/](https://kkroening.github.io/ffmpeg-python/)



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

## Dividing Large Audio files into smaller chunks
1. Speech boundaries (Sentence structure along with punctuation or Pause-based)
    * If the speech contains noticeable pauses (silent gaps between sentences), we'll set a threshold for the duration of the pause that qualifies as a sentence boundary.
    * Then combine smaller chunks into their nearest chunks with monitoring max and min durations of the audio file.
    * If there is a pause then remove in between the sentences. And add small padding silence at both ends of the remaining audio at that window.



* Update the torch version to latest.