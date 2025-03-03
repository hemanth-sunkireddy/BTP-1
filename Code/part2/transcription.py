import whisper

model = whisper.load_model("turbo")

result = model.transcribe("audio/sample_aud1.wav")

print(result["text"])

with open("text/transcribed_1.txt", "w") as file:
    file.write(result["text"])


with open("text/transcribed_1.srt", "w") as srt_file:
    for i, segment in enumerate(result["segments"]):
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]

        start_time = f"{int(start // 3600):02}:{int((start % 3600) // 60):02}:{int(start % 60):02},{int((start % 1) * 1000):03}"
        end_time = f"{int(end // 3600):02}:{int((end % 3600) // 60):02}:{int(end % 60):02},{int((end % 1) * 1000):03}"
        srt_file.write(f"{i + 1}\n")
        srt_file.write(f"{start_time} --> {end_time}\n")
        srt_file.write(f"{text.strip()}\n\n")

