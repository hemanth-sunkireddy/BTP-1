import ffmpeg

# Ask the user for the input video file path
input_file = input("Please enter the path to the video file (e.g., 'index.mp4'): ")

# Set the desired sample rate (32000 Hz or 48000 Hz)
sample_rate = '48000'  # You can change this to '32000' if you prefer that sample rate

# Input the video file
input_video = ffmpeg.input(input_file)

# Extract audio, force mono, and set the sample rate (48000 Hz by default)
output_audio = ffmpeg.output(input_video.audio, 'output_audio.wav', ac=1, ar=sample_rate)

# Execute the command to extract audio
ffmpeg.run(output_audio)

# Now probe the generated audio file for detailed information
audio_info = ffmpeg.probe('output_audio.wav', v='error', select_streams='a', show_entries='stream=codec_name,codec_type,sample_rate,channels,bit_rate,duration')

# Print the relevant information
codec_name = audio_info['streams'][0]['codec_name']
sample_rate = int(audio_info['streams'][0]['sample_rate'])
channels = int(audio_info['streams'][0]['channels'])
bit_rate = audio_info['streams'][0].get('bit_rate', 'N/A')  # Bitrate might not be available for uncompressed audio like WAV
duration_sec = float(audio_info['streams'][0]['duration'])
duration_ms = duration_sec * 1000  # Convert to milliseconds

# Print the relevant information
print(f"Audio Codec: {codec_name}")
print(f"Sample Rate: {sample_rate} Hz")
print(f"Channels: {channels}")
print(f"Bit Rate: {bit_rate}")
print(f"Duration: {duration_ms} ms")
