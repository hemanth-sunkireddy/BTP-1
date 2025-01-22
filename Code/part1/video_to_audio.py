import ffmpeg

# Ask the user for the input audio file path
input_file = input("Please enter the path to the video file (e.g., 'index.mp4'): ")

# Input the video file
input_video = ffmpeg.input(input_file)

# Extract audio and output as a .wav file
output_audio = ffmpeg.output(input_video.audio, 'output_audio.wav')

# Execute the command
ffmpeg.run(output_audio)
