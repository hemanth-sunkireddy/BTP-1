# from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx
# import os
# import datetime

# def format_srt_timestamp(seconds):
#     """Convert seconds to SRT timestamp format: HH:MM:SS,mmm"""
#     td = datetime.timedelta(seconds=seconds)
#     total_seconds = int(td.total_seconds())
#     milliseconds = int((td.total_seconds() - total_seconds) * 1000)
#     hours, remainder = divmod(total_seconds, 3600)
#     minutes, seconds = divmod(remainder, 60)
#     return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"

# def create_continuous_srt(clips_info, output_filename="stitched_output.srt", transition_sec=1.0):
#     """
#     clips_info: List of tuples (clip_duration, sentence)
#     transition_sec: Duration of transitions (e.g., fade) to account for.
#     """
#     srt_lines = []
#     current_time = 0.0

#     for idx, (duration, sentence) in enumerate(clips_info, start=1):
#         start_time = format_srt_timestamp(current_time)
#         end_time = format_srt_timestamp(current_time + duration)
#         srt_lines.append(f"{idx}\n{start_time} --> {end_time}\n{sentence}\n")
#         current_time += duration + transition_sec  # Add transition time after each clip

#     with open(output_filename, "w") as f:
#         f.write("\n".join(srt_lines))

# # Function to parse timestamp string to (start, end)
# def parse_timestamp(timestamp_str):
#     start, end = timestamp_str.split(" --> ")
#     return start.strip(), end.strip()

# # Function to normalize audio of a clip
# def normalize_audio(clip, target_dB=20.0):
#     current_volume = clip.audio.max_volume()
#     gain = target_dB - current_volume
#     return clip.volumex(10 ** (gain / 20))

# # Function to apply transitions
# def apply_transition(clip1, clip2, transition_type):
#     if transition_type == "fade_through_black":
#         return concatenate_videoclips([clip1.fadeout(1), clip2.fadein(1)], method="compose")
#     elif transition_type == "fade":
#         return concatenate_videoclips([clip1.fadeout(1), clip2.fadein(1)])
#     elif transition_type == "flip":
#         return concatenate_videoclips([clip1, clip2.fx(vfx.rotate, angle=180)])
#     elif transition_type == "fold":
#         return concatenate_videoclips([clip1, clip2.fx(vfx.slide_out, 1, 'left')])
#     else:
#         return concatenate_videoclips([clip1, clip2])

# # Main function to stitch clips from multiple videos
# def stitch_video_from_segments(segment_list, transition_type="fade_through_black", srt_filename="stitched_output.srt"):
#     video_cache = {}
#     clips = []
#     clips_info = []  # To store (duration, sentence) for SRT

#     for filename, timestamp, sentence, distance in segment_list:
#         video_file = "../Data/Videos/"+os.path.splitext(filename)[0] + ".mp4"
#         start, end = parse_timestamp(timestamp)

#         if video_file not in video_cache:
#             try:
#                 video_cache[video_file] = VideoFileClip(video_file)
#             except FileNotFoundError:
#                 print(f"Video file '{video_file}' not found. Skipping.")
#                 continue

#         try:
#             clip = video_cache[video_file].subclip(start, end)
#             normalized_clip = normalize_audio(clip)
#             clips.append(normalized_clip)
#             clips_info.append((normalized_clip.duration, sentence))  # Capture info for SRT
#         except Exception as e:
#             print(f"Error processing segment ({filename}, {timestamp}): {e}")

#     if not clips:
#         print("No valid clips found.")
#         return

#     final_clip = clips[0]
#     for i in range(1, len(clips)):
#         final_clip = apply_transition(final_clip, clips[i], transition_type)

#     final_clip.write_videofile("stitched_output.mp4", codec="libx264")

#     # Create the updated SRT file
#     create_continuous_srt(clips_info, output_filename=srt_filename, transition_sec=1.0)


# # Example input: list of (filename, timestamp, sentence, distance)
# # segments = [
# #     ("1.srt", "00:00:10.000 --> 00:00:20.000", "Some sentence", 0.5),
# #     ("1.srt", "00:00:30.000 --> 00:00:40.000", "Another sentence", 0.3),
# #     # Add more tuples as needed
# # ]

# # stitch_video_from_segments(segments, transition_type="fade_through_black")


# from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx
# import os
# import datetime

# def format_srt_timestamp(seconds):
#     td = datetime.timedelta(seconds=seconds)
#     total_seconds = int(td.total_seconds())
#     milliseconds = int((td.total_seconds() - total_seconds) * 1000)
#     hours, remainder = divmod(total_seconds, 3600)
#     minutes, seconds = divmod(remainder, 60)
#     return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"

# def create_continuous_srt(clips_info, output_filename="stitched_output.srt", transition_sec=1.0):
#     srt_lines = []
#     current_time = 0.0

#     for idx, (duration, sentence) in enumerate(clips_info, start=1):
#         start_time = format_srt_timestamp(current_time)
#         end_time = format_srt_timestamp(current_time + duration)
#         srt_lines.append(f"{idx}\n{start_time} --> {end_time}\n{sentence}\n")
#         current_time += duration + transition_sec

#     with open(output_filename, "w") as f:
#         f.write("\n".join(srt_lines))

# def parse_timestamp(timestamp_str):
#     start, end = timestamp_str.split(" --> ")
#     return start.strip(), end.strip()

# def apply_transition(clip1, clip2, transition_type):
#     if transition_type == "fade_through_black":
#         return concatenate_videoclips([clip1.fadeout(1), clip2.fadein(1)], method="compose")
#     elif transition_type == "fade":
#         return concatenate_videoclips([clip1.fadeout(1), clip2.fadein(1)])
#     elif transition_type == "flip":
#         return concatenate_videoclips([clip1, clip2.fx(vfx.rotate, angle=180)])
#     elif transition_type == "fold":
#         return concatenate_videoclips([clip1, clip2.fx(vfx.slide_out, 1, 'left')])
#     else:
#         return concatenate_videoclips([clip1, clip2])

# def stitch_video_from_segments(segment_list, transition_type=None, srt_filename="stitched_output.srt", apply_transitions=False):
#     clips = []
#     clips_info = []

#     for filename, timestamp, sentence, distance in segment_list:
#         video_file = "../Data/Videos/" + os.path.splitext(filename)[0] + ".mp4"
#         start, end = parse_timestamp(timestamp)

#         try:
#             clip = VideoFileClip(video_file).subclip(start, end)
#             clips.append(clip)
#             clips_info.append((clip.duration, sentence))
#         except Exception as e:
#             print(f"Error processing segment ({filename}, {timestamp}): {e}")

#     if not clips:
#         print("No valid clips found.")
#         return

#     if apply_transitions and transition_type:
#         final_clip = clips[0]
#         for i in range(1, len(clips)):
#             final_clip = apply_transition(final_clip, clips[i], transition_type)
#     else:
#         final_clip = concatenate_videoclips(clips, method="chain")  # Fastest option

#     final_clip.write_videofile(
#         "stitched_output.mp4",
#         codec="libx264",
#         preset="ultrafast",
#         threads=4,
#         audio_codec="aac"
#     )

#     create_continuous_srt(clips_info, output_filename=srt_filename, transition_sec=(1.0 if apply_transitions else 0.0))


# # ✅ Example input
# # segments = [
# #     ("1.srt", "00:00:10.000 --> 00:00:20.000", "Some sentence", 0.5),
# #     ("1.srt", "00:00:30.000 --> 00:00:40.000", "Another sentence", 0.3),
# # ]

# # # ✅ Call function (without transitions for maximum speed)
# # stitch_video_from_segments(
# #     segments,
# #     transition_type="fade_through_black",  # Optional
# #     apply_transitions=True  # Set to True to enable transitions (slower)
# # )


from moviepy.editor import VideoFileClip, concatenate_videoclips, ColorClip
import os
import datetime

def format_srt_timestamp(seconds):
    td = datetime.timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    milliseconds = int((td.total_seconds() - total_seconds) * 1000)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"

def create_continuous_srt(clips_info, output_filename="stitched_output.srt", transition_sec=1.0):
    srt_lines = []
    current_time = 0.0

    for idx, (duration, sentence) in enumerate(clips_info, start=1):
        start_time = format_srt_timestamp(current_time)
        end_time = format_srt_timestamp(current_time + duration)
        srt_lines.append(f"{idx}\n{start_time} --> {end_time}\n{sentence}\n")
        current_time += duration + transition_sec  # Account for pause
    with open(output_filename, "w") as f:
        f.write("\n".join(srt_lines))

def parse_timestamp(timestamp_str):
    start, end = timestamp_str.split(" --> ")
    return start.strip(), end.strip()

def stitch_video_from_segments(segment_list, srt_filename="stitched_output.srt", pause_duration=1.0):
    clips = []
    clips_info = []

    for idx, (filename, timestamp, sentence) in enumerate(segment_list):
        video_file = "../Data/Videos/" + os.path.splitext(filename)[0] + ".mp4"
        start, end = parse_timestamp(timestamp)

        try:
            clip = VideoFileClip(video_file).subclip(start, end)

            # Resize black screen to match clip size
            if idx > 0:
                black_clip = ColorClip(size=clip.size, color=(0, 0, 0), duration=pause_duration)
                black_clip = black_clip.set_fps(clip.fps)
                clips.append(black_clip)

            clips.append(clip)
            clips_info.append((clip.duration, sentence))
        except Exception as e:
            print(f"Error processing segment ({filename}, {timestamp}): {e}")

    if not clips:
        print("No valid clips found.")
        return

    final_clip = concatenate_videoclips(clips, method="chain")

    final_clip.write_videofile(
        "stitched_output.mp4",
        codec="libx264",
        preset="ultrafast",
        threads=4,
        audio_codec="aac"
    )

    create_continuous_srt(clips_info, output_filename=srt_filename, transition_sec=pause_duration)


# # ✅ Example input
# segments = [
#     ("1.srt", "00:00:10.000 --> 00:00:20.000", "Some sentence", 0.5),
#     ("1.srt", "00:00:30.000 --> 00:00:40.000", "Another sentence", 0.3),
# ]

# # ✅ Run with 1s black break between clips
# stitch_video_from_segments(
#     segments,
#     pause_duration=1.0
# )
