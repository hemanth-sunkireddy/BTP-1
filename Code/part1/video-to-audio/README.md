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
4. The output audio file has 1 channel (Mono), Audio codec is PCM 16, a sample rate of 16000 Hz and Bit rate of 256.000kbits/s.

* Documentation of FFMPEG-Python: https://kkroening.github.io/ffmpeg-python/