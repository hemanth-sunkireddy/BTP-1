import subprocess

def extract_and_stitch(video_path, segments, output_path):

    try:
        # Step 1: Extract each segment and save as temporary files
        temp_files = []
        for i, (start, end) in enumerate(segments):
            temp_file = f"temp_segment_{i}.mp4"
            temp_files.append(temp_file)
            command = [
                "ffmpeg",
                "-i", video_path,
                "-ss", str(start),  # Start time
                "-to", str(end),    # End time
                "-c", "copy",       # Copy codec (no re-encoding)
                temp_file
            ]
            subprocess.run(command, check=True)
        
        # Step 2: Create a text file listing all segments
        concat_file = "concat_list.txt"
        with open(concat_file, "w") as f:
            for temp_file in temp_files:
                f.write(f"file '{temp_file}'\n")
        
        # Step 3: Stitch the segments together
        command = [
            "ffmpeg",
            "-f", "concat",       # Concatenate mode
            "-safe", "0",         # Allow unsafe file paths
            "-i", concat_file,    # Input list of files
            "-c", "copy",         # Copy codec
            output_path
        ]
        subprocess.run(command, check=True)
        
        print(f"Video successfully saved to {output_path}")
    
    except subprocess.CalledProcessError as e:
        print(f"Error during FFmpeg processing: {e}")
    
    finally:
        # Cleanup temporary files
        import os
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        if os.path.exists(concat_file):
            os.remove(concat_file)

# Example Usage
video_path = "video/Adiyogi.mp4"  # Path to your video file
segments = [(30, 60), (120, 150), (200, 240)]  # Start and end times (in seconds)
output_path = "video/stitched_adiyogi.mp4"  # Path to save the final stitched video

extract_and_stitch(video_path, segments, output_path)
