import whisper_timestamped as whisper
import json
import os
import time
import librosa
import matplotlib.pyplot as plt

# Initialize model once
model = whisper.load_model("small", device="cpu")

# Function to transcribe and save files
def transcribe_audio(audio_path):

    # Measure audio duration
    duration = librosa.get_duration(path=audio_path)

    # Start time before transcription
    
    start_time = time.time()

    # Load audio
    audio = whisper.load_audio(audio_path)

    # Transcribe the audio
    result = whisper.transcribe(model, audio, language="en")

    # Calculate time taken
    transcribe_time = time.time() - start_time
    print(start_time,"-",time.time(),transcribe_time)
    return duration, transcribe_time

# Directory containing audio files
audio_dir = "Data3"
audio_files = [os.path.join(audio_dir, file) for file in os.listdir(audio_dir) if file.endswith(".wav")]

# Lists to store results
durations = []
times_taken = []

# Process each audio file
for audio_file in audio_files:
    duration, transcribe_time = transcribe_audio(audio_file)
    durations.append(duration)
    times_taken.append(transcribe_time)

print (durations,times_taken)

with open("test_data.txt", "w") as file:
    file.write("Durations: " + str(durations) + "\n")
    file.write("Time Taken: " + str(times_taken) + "\n")
# Plot duration vs transcription time
plt.figure(figsize=(8, 5))
plt.scatter(durations, times_taken, color='blue', label='Data Points')
plt.plot(durations, times_taken, linestyle='--', color='red', label='Trend')

plt.xlabel("Audio Duration (seconds)")
plt.ylabel("Transcription Time (seconds)")
plt.title("Audio Duration vs. Transcription Time")
plt.legend()
plt.grid()
plt.show()

