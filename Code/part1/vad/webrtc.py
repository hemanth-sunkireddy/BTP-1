import contextlib
import sys
import wave
import webrtcvad
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

from definitions import silence_threshold, chunk_min_dur, chunk_max_dur, sample_rate

def read_wave(path):
    with contextlib.closing(wave.open(path, 'rb')) as wf:
        num_channels = wf.getnchannels()
        assert num_channels == 1
        sample_width = wf.getsampwidth()
        assert sample_width == 2
        sample_rate = wf.getframerate()
        assert sample_rate in (8000, 16000, 32000, 48000)
        pcm_data = wf.readframes(wf.getnframes())
        return pcm_data, sample_rate

def write_wave(path, audio, sample_rate):
    with contextlib.closing(wave.open(path, 'wb')) as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio)

class Frame(object):
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration

def frame_generator(frame_duration_ms, audio, sample_rate):
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate) / 2.0
    while offset + n < len(audio):
        yield Frame(audio[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    milliseconds = (seconds - int(seconds)) * 1000
    return f"{int(minutes):02}:{int(seconds):02}.{milliseconds:04.1f}"

def silent_periods_collector(sample_rate, vad, frames, silence_threshold_seconds=silence_threshold):
    silent_frames = []
    silence_timings = []
    total_silence_duration = 0
    chunk_count = 0
    start_time = None
    end_time = None
    table = []
    last_silence_timestamp = None

    for frame in frames:
        is_speech = vad.is_speech(frame.bytes, sample_rate)

        if is_speech:
            if last_silence_timestamp is not None:
                end_time = frame.timestamp
                duration = end_time - start_time
                if duration >= silence_threshold_seconds:
                    chunk_count += 1
                    silence_timings.append([round(start_time, 3), round(end_time, 3), round(duration, 3)])
                    table.append([
                        chunk_count,
                        format_time(start_time),
                        format_time(end_time),
                        f"{duration:.3f} seconds"
                    ])
            total_silence_duration = 0
            last_silence_timestamp = None
            start_time = None
            end_time = None
        else:
            if last_silence_timestamp is None:
                start_time = frame.timestamp
                last_silence_timestamp = start_time

            total_silence_duration += frame.duration
            silent_frames.append(frame)

    if last_silence_timestamp is not None:
        end_time = frames[-1].timestamp
        duration = end_time - start_time
        if duration >= silence_threshold_seconds:
            chunk_count += 1
            silence_timings.append([round(start_time, 3), round(end_time, 3), round(duration, 3)])
            table.append([
                chunk_count,
                format_time(start_time),
                format_time(end_time),
                f"{duration:.3f} seconds"
            ])

    headers = ["Chunk Num", "Start Time (min:sec.ms)", "End Time (min:sec.ms)", "Duration"]
    print(tabulate(table, headers=headers, tablefmt="rounded_grid"))
    print(f"Total Chunks Which are Continuous Silent: {chunk_count}")

    return silence_timings


def plot_vad(sample_rate, frames, vad, chunk_details):
    vad_output = []
    timestamps = []
    # print(chunk_details[1][2])
    for frame in frames:
        is_speech = vad.is_speech(frame.bytes, sample_rate)
        num_samples_in_frame = len(frame.bytes) // 2
        vad_output.extend([is_speech] * num_samples_in_frame)
        timestamps.extend([frame.timestamp] * num_samples_in_frame)
    
    plt.figure(figsize=(16, 8))
    plt.plot(timestamps, vad_output, label="VAD (Speech: 1, Silence: 0)", color='blue', lw=0.5)
    plt.title('VAD Output (1 = Speech, 0 = Silence)')
    plt.xlabel('Time [s]')
    plt.ylabel('VAD')
    for chunk in chunk_details:
        minutes, seconds = map(int, chunk[2].split(":"))
        time_in_seconds = minutes * 60 + seconds
        plt.scatter(time_in_seconds, -0.001, color='red', marker='.', s=20)  # Mark on x-axis below VAD plot
        # plt.text(time_in_seconds, 0, f"{time_in_seconds:.0f}s", color='red', ha='center', fontsize=10)


    plt.ylim([-0.1, 1.1])
    plt.tight_layout()
    step_size = 100
    x_ticks = np.arange(min(timestamps), max(timestamps), step_size)
    plt.xticks(x_ticks)
    plt.show()



def vad_collector(sample_rate, vad, frames, silence_timings, chunk_min_dur=chunk_min_dur, chunk_max_dur=chunk_max_dur):
    """Filters out non-voiced audio frames and collects continuous speech chunks with silence removed."""
    total_speech_duration = 0
    chunk_count = 0
    start_time = None
    end_time = None
    current_frames = []
    segments = []
    chunk_details = []  # Stores chunk info for tabulation
    continuous_silence = 0

    for frame in frames:
        is_speech = vad.is_speech(frame.bytes, sample_rate)
        if total_speech_duration == 0:
            start_time = frame.timestamp

        if is_speech:  # Speech frame
            continuous_silence = 0
            current_frames.append(frame)
            total_speech_duration += frame.duration

            # If speech duration reaches chunk_max_dur, finalize the chunk
            if total_speech_duration >= chunk_max_dur:
                end_time = frame.timestamp + frame.duration
                duration = end_time - start_time
                chunk_count += 1
                segments.append(b''.join([f.bytes for f in current_frames]))  # Add the chunk

                # Store chunk details
                chunk_details.append([
                    chunk_count,
                    format_time(start_time),
                    format_time(end_time),
                    f"{duration:.4f} seconds"
                ])

                # Reset for the next chunk
                current_frames = []
                total_speech_duration = 0
                start_time = None

        else:  # Silence frame
            total_speech_duration += frame.duration
            current_frames.append(frame)
            continuous_silence += frame.duration

            # If we've passed the chunk_min_dur threshold and encounter enough silence, finalize the chunk
            if total_speech_duration >= chunk_min_dur and continuous_silence >= silence_threshold:
                end_time = frame.timestamp
                duration = end_time - start_time
                chunk_count += 1
                segments.append(b''.join([f.bytes for f in current_frames]))  # Add the chunk

                # Store chunk details
                chunk_details.append([
                    chunk_count,
                    format_time(start_time),
                    format_time(end_time),
                    f"{duration:.4f} seconds"
                ])

                # Reset for the next chunk
                current_frames = []
                total_speech_duration = 0
                start_time = None

    # If there are remaining frames, output them as the final chunk
    if current_frames:
        end_time = frames[-1].timestamp + frames[-1].duration
        duration = end_time - start_time
        chunk_count += 1
        segments.append(b''.join([f.bytes for f in current_frames]))  # Add the final chunk

        # Store the final chunk's details
        chunk_details.append([
            "Final",
            format_time(start_time),
            format_time(end_time),
            f"{duration:.4f} seconds"
        ])

    # Print chunk details using tabulate
    headers = ["Chunk Num", "Start Time", "End Time", "Duration"]
    print("\nChunks Details:")
    print(tabulate(chunk_details, headers=headers, tablefmt="rounded_grid"))

    return segments, chunk_details
w



def main(args):
    if len(args) != 2:
        sys.stderr.write('Command Structure:python3 webrtc.py <aggressiveness> <path to wav file>\n')
        sys.exit(1)
    
    audio, sample_rate = read_wave(args[1])
    vad = webrtcvad.Vad(int(args[0]))
    frames = frame_generator(30, audio, sample_rate)
    frames = list(frames)

    
    print("Continous silence frames which are more than silence threshold")
    silence_timings = silent_periods_collector(sample_rate, vad, frames)
    
    segments, chunk_details = vad_collector(sample_rate, vad, frames, silence_timings)
    plot_vad( sample_rate, frames, vad, chunk_details)
    for i, segment in enumerate(segments):
        path = 'chunk-%002d.wav' % (i,)
        # print(' Writing %s' % (path,))
        write_wave(path, segment, sample_rate)

if __name__ == '__main__':
    main(sys.argv[1:])
