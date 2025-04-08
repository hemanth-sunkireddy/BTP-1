import subprocess

# Paths to your input WAV files
file1 = "../Data2/900sec.wav"
file2 = "../Data2/900sec.wav"
output = "merged_output.wav"

# Create a temporary text file with the list of files to concatenate
with open("file_list.txt", "w") as file_list:
    file_list.write(f"file '{file1}'\n")
    file_list.write(f"file '{file2}'\n")

# Use ffmpeg to concatenate the WAV files using the text file
subprocess.run([
    "ffmpeg",
    "-f", "concat",  # Specify concat demuxer
    "-safe", "0",    # Allow unsafe file paths (useful if files are outside the current directory)
    "-i", "file_list.txt",  # Input is the text file listing files to concatenate
    "-acodec", "pcm_s16le",  # Specify codec for WAV
    "-ar", "16000",  # Sample rate (optional, default is 44100)
    "-ac", "1",      # Number of audio channels (Mono)
    output
])

# Clean up the temporary text file
import os
os.remove("file_list.txt")

print(f"Merged file saved as {output}")
