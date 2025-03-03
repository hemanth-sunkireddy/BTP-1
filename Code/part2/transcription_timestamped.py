import whisper_timestamped as whisper
import json
import os

# Initialize model once
model = whisper.load_model("small", device="cpu")

# Function to transcribe and save files
def transcribe_audio(audio_path):
    # Extract the base name without extension
    base_name = os.path.splitext(os.path.basename(audio_path))[0]

    # Load audio
    audio = whisper.load_audio(audio_path)

    # Transcribe the audio
    result = whisper.transcribe(model, audio, language="en")

    # Save result as a JSON file
    json_path = "text/"+f"{base_name}.json"
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(result, json_file, indent=2, ensure_ascii=False)

    # Function to format as SRT
    def format_srt(segments):
        srt = []
        for i, segment in enumerate(segments, start=1):
            start = format_time(segment['start'])
            end = format_time(segment['end'])
            text = segment['text']
            srt.append(f"{i}\n{start} --> {end}\n{text}\n")
        return "\n".join(srt)

    # Helper function to format time for SRT
    def format_time(seconds):
        milliseconds = int((seconds % 1) * 1000)
        seconds = int(seconds)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

    # Generate SRT content
    srt_content = format_srt(result["segments"])

    # Save result as an SRT file
    srt_path = "text/"+f"{base_name}.srt"
    with open(srt_path, "w", encoding="utf-8") as srt_file:
        srt_file.write(srt_content)

    print(f"Transcription saved as '{json_path}' and '{srt_path}'.")

# Directory containing audio files
audio_dir = "audio"
audio_files = [os.path.join(audio_dir, file) for file in os.listdir(audio_dir) if file.endswith(".wav")]

# Process each audio file
for audio_file in audio_files:
    transcribe_audio(audio_file)
