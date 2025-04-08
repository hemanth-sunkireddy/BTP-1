import subprocess

def convert_to_mono(input_file, output_file, sample_rate=16000):
    command = [
        "ffmpeg",
        "-i", input_file,
        "-ac", "1",  # Convert to mono
        "-ar", str(sample_rate),  # Set sample rate to 16000 Hz
        output_file
    ]
    subprocess.run(command, check=True)
    print(f"Converted {input_file} to mono with sample rate {sample_rate} Hz and saved as {output_file}")

# Example usage
convert_to_mono("../vad/audio_3.wav", "output_mono.wav")
