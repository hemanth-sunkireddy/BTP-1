import ffmpeg
import os

# Define input and output directories
input_folder = "Data"
output_folder = "audios"

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Set the desired sample rate (16000 Hz or 32000 Hz)
sample_rate = "16000"  # Change this to "32000" if needed

# Loop through all .mp4 files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".mp4"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename.replace(".mp4", ".wav"))

        print(f"Processing: {input_path} -> {output_path}")
        
        # Extract audio
        input_video = ffmpeg.input(input_path)
        output_audio = ffmpeg.output(input_video.audio, output_path, ac=1, ar=sample_rate)
        ffmpeg.run(output_audio, overwrite_output=True)
        
        # Probe the generated audio file for details
        audio_info = ffmpeg.probe(output_path, v="error", select_streams="a", show_entries="stream=codec_name,codec_type,sample_rate,channels,bit_rate,duration")
        
        codec_name = audio_info['streams'][0]['codec_name']
        sample_rate = int(audio_info['streams'][0]['sample_rate'])
        channels = int(audio_info['streams'][0]['channels'])
        bit_rate = audio_info['streams'][0].get('bit_rate', 'N/A')
        duration_sec = float(audio_info['streams'][0]['duration'])
        duration_ms = duration_sec * 1000
        
        print(f"Audio extracted: {output_path}")
        print(f"Codec: {codec_name}, Sample Rate: {sample_rate} Hz, Channels: {channels}, Bit Rate: {bit_rate}, Duration: {duration_ms} ms\n")

print("Video to Audio converted successfully!.")