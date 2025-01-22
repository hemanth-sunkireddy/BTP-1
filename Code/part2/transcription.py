import whisper

# Load the Whisper model
model = whisper.load_model("turbo")

result = model.transcribe("audio/lec_1.wav")

print(result["text"])

with open("text/transcription.txt", "w") as file:
    file.write(result["text"])
