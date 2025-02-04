import contextlib
import sys
import wave
import webrtcvad
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate

from definitions import silence_threshold, chunk_min_dur, chunk_max_dur, sample_rate

def read_wave(path):
    """Reads a .wav file. Takes the path, and returns (PCM audio data, sample rate)."""
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
    """Writes a .wav file. Takes path, PCM audio data, and sample rate."""
    with contextlib.closing(wave.open(path, 'wb')) as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio)

class Frame(object):
    """Represents a "frame" of audio data."""
    def __init__(self, bytes, timestamp, duration):
        self.bytes = bytes
        self.timestamp = timestamp
        self.duration = duration

def frame_generator(frame_duration_ms, audio, sample_rate):
    """Generates audio frames from PCM audio data."""
    n = int(sample_rate * (frame_duration_ms / 1000.0) * 2)
    offset = 0
    timestamp = 0.0
    duration = (float(n) / sample_rate) / 2.0
    while offset + n < len(audio):
        yield Frame(audio[offset:offset + n], timestamp, duration)
        timestamp += duration
        offset += n

def silent_periods_collector(sample_rate, vad, frames, silence_threshold_seconds=silence_threshold):
    """Filters out voiced audio frames and collects continuous silence chunks of more than `silence_threshold_seconds`."""
    silent_frames = []
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
                    start_min, start_sec = divmod(start_time, 60)
                    end_min, end_sec = divmod(end_time, 60)
                    table.append([
                        chunk_count,
                        f"{int(start_min):02}:{int(start_sec):02}",
                        f"{int(end_min):02}:{int(end_sec):02}",
                        f"{duration:.2f} seconds"
                    ])
                    last_silence_timestamp = None
                    start_time = None
                    end_time = None
                else:
                    last_silence_timestamp = None
                    start_time = None
                    end_time = None
            total_silence_duration = 0

        else:
            if last_silence_timestamp == None:
                start_time = frame.timestamp
                last_silence_timestamp = start_time
            else:
                end_time = frame.timestamp
                duration = end_time - start_time
                if duration >= silence_threshold_seconds:
                    chunk_count += 1
                    start_min, start_sec = divmod(start_time, 60)
                    end_min, end_sec = divmod(end_time, 60)
                    table.append([
                        chunk_count,
                        f"{int(start_min):02}:{int(start_sec):02}",
                        f"{int(end_min):02}:{int(end_sec):02}",
                        f"{duration:.2f} seconds"
                    ])
                    last_silence_timestamp = None
                    start_time = None
                    end_time = None
            total_silence_duration += frame.duration
            silent_frames.append(frame)

    headers = ["Chunk Num", "Start Time (min)", "End Time (min)", "Duration"]
    print(tabulate(table, headers=headers, tablefmt="rounded_grid"))
    print("Total Chunks Which are Continous Silent:", chunk_count)
    return silent_frames

def plot_vad(sample_rate, frames, vad):
    vad_output = []
    timestamps = []
    
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
    plt.ylim([-0.1, 1.1])
    plt.tight_layout()
    step_size = 100
    x_ticks = np.arange(min(timestamps), max(timestamps), step_size)
    plt.xticks(x_ticks)
    plt.show()

def main(args):
    if len(args) != 2:
        sys.stderr.write('Command Structure:python3 webrtc.py <aggressiveness> <path to wav file>\n')
        sys.exit(1)
    
    audio, sample_rate = read_wave(args[1])
    vad = webrtcvad.Vad(int(args[0]))
    frames = frame_generator(30, audio, sample_rate)
    frames = list(frames)

    # plot_vad( sample_rate, frames, vad)
    print("Continous silence frames which are more than silence threshold")
    silent_periods_collector(sample_rate, vad, frames)

def vad_collector(sample_rate, frame_duration_ms,padding_duration_ms, vad, frames, speech_threshold_seconds=30):
    """Filters out non-voiced audio frames and collects continuous speech chunks of speech with silence removed."""
    num_padding_frames = int(padding_duration_ms / frame_duration_ms)
    voiced_frames = []
    total_speech_duration = 0
    chunk_count = 0
    start_time = None
    end_time = None
    table = []

    for frame in frames:
        is_speech = vad.is_speech(frame.bytes, sample_rate)
        
        if is_speech:
            if total_speech_duration == 0:
                start_time = frame.timestamp
            total_speech_duration += frame.duration
            voiced_frames.append(frame)

        # Check if we've collected more than 30 seconds of speech
        if total_speech_duration >= speech_threshold_seconds:
            chunk_count += 1
            end_time = frame.timestamp + frame.duration  # End time is the current frame's timestamp + its duration
            duration = end_time - start_time  # Calculate the duration of the chunk in seconds

            # Convert start_time and end_time from seconds to minutes:seconds format
            start_min, start_sec = divmod(start_time, 60)
            end_min, end_sec = divmod(end_time, 60)

            # Append the chunk details as a list (not a dict)
            table.append([
                chunk_count,
                f"{int(start_min):02}:{int(start_sec):02}",
                f"{int(end_min):02}:{int(end_sec):02}",
                f"{duration:.2f} seconds"
            ])

            # Yield the combined voiced frames (this is the chunk with silence removed)
            yield b''.join([f.bytes for f in voiced_frames])

            # Reset after yielding the chunk
            total_speech_duration = 0
            voiced_frames = []  # Clear the voiced frames for the next chunk

    # Yield any remaining voiced frames at the end if they exist
    if voiced_frames:
        # Calculate the last chunk's end time and duration
        end_time = frames[-1].timestamp + frames[-1].duration
        duration = end_time - start_time
        
        # Convert start_time and end_time from seconds to minutes:seconds format
        start_min, start_sec = divmod(start_time, 60)
        end_min, end_sec = divmod(end_time, 60)

        table.append([
            "Final",
            f"{int(start_min):02}:{int(start_sec):02}",
            f"{int(end_min):02}:{int(end_sec):02}",
            f"{duration:.2f} seconds"
        ])

        # Yield the last chunk
        yield b''.join([f.bytes for f in voiced_frames])

    # Print the table with the chunk details at the end
    headers = ["Chunk Num", "Start Time (min)", "End Time (min)", "Duration"]
    print(tabulate(table, headers=headers, tablefmt="rounded_grid"))


if __name__ == '__main__':
    main(sys.argv[1:])
