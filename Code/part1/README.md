# Video to Audio Conversion

This script extracts audio from a video file and saves it as a `.wav` file.

## Prerequisites

Make sure you have `ffmpeg-python` installed. You can install it with:

```bash
pip install ffmpeg-python
```

## Usage
1. Run the `video_to_audio.py` script in the terminal:
    `python3 video_to_audio.py`
2. When prompted, enter the full path of the video file (e.g., path/to/video.mp4).
3. The audio will be extracted and saved as output_audio.wav in the same directory where the script is located.

# VAD Algorithm
we will use the **Silero Voice Activity Detection (VAD) model** to extract speech from an audio file, removing silent portions.

1. Install Silero VAD:
    `pip install silero-vad`
2. Additional dependencies:
    * **Soundfile:** To handle reading and writing audio files.
        * `pip install soundfile`
    * **Sox:** For audio processing and manipulation.
        * `pip install sox`
3. Run `silero-vad.ipynb` file and the generated output will be `only_speech.wav` 