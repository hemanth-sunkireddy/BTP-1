import subprocess

# List of input WAV files
wav_files = ["Data3/900.wav", "Data3/550.wav"]
output_file = "Data3/1450.wav"

# Create a text file listing all input WAV files
with open("input.txt", "w") as f:
    for file in wav_files:
        f.write(f"file '{file}'\n")

# Run ffmpeg command to concatenate the WAV files
subprocess.run(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "input.txt", "-c", "copy", output_file])

print(f"Merged file saved as {output_file}")
