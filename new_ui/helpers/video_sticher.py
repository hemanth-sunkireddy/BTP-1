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

def create_continuous_srt(clips_info, output_filename="./data/output/stitched_output.srt", transition_sec=1.0):
    srt_lines = []
    current_time = 0.0

    for idx, (duration, sentence, start, video_file) in enumerate(clips_info, start=1):
        start_time = format_srt_timestamp(current_time)
        end_time = format_srt_timestamp(current_time + duration)
        srt_lines.append(f"{idx}\n{start_time} --> {end_time}\n{sentence}\n")
        current_time += duration + transition_sec  # Account for pause
    with open(output_filename, "w") as f:
        f.write("\n".join(srt_lines))

def parse_timestamp(timestamp_str):
    start, end = timestamp_str.split(" --> ")
    return start.strip(), end.strip()

def stitch_video_from_segments(segment_list, srt_filename="./data/output/stitched_output.srt", pause_duration=1.0):
    clips = []
    clips_info = []
    sources = set()

    for idx, (filename, timestamp, sentence, distance) in enumerate(segment_list):
        lecture_no = os.path.splitext(filename)[0]
        video_file = "./data/videos/" + lecture_no + ".mp4"
        start, end = parse_timestamp(timestamp)
        sources.add("Lecture - " + lecture_no)

        try:
            clip = VideoFileClip(video_file).subclip(start, end)

            # Resize black screen to match clip size
            if idx > 0:
                black_clip = ColorClip(size=clip.size, color=(0, 0, 0), duration=pause_duration)
                black_clip = black_clip.set_fps(clip.fps)
                clips.append(black_clip)

            clips.append(clip)
            clips_info.append((clip.duration, sentence, start, video_file))
        except Exception as e:
            print(f"Error processing segment ({filename}, {timestamp}): {e}")

    if not clips:
        print("No valid clips found.")
        return

    final_clip = concatenate_videoclips(clips, method="chain")

    final_clip.write_videofile(
        "./data/output/stitched_output.mp4",
        codec="libx264",
        preset="ultrafast",
        threads=4,
        audio_codec="aac"
    )

    create_continuous_srt(clips_info, output_filename=srt_filename, transition_sec=pause_duration)

    return clips_info, sources