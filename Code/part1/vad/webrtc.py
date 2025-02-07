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
    silence_timings = []  # This will store the [start_time, end_time, duration] for each silence period
    total_silence_duration = 0
    chunk_count = 0
    start_time = None
    end_time = None
    table = []  # This is the table for printing

    last_silence_timestamp = None

    for frame in frames:
        is_speech = vad.is_speech(frame.bytes, sample_rate)

        if is_speech:  # Speech
            if last_silence_timestamp is not None:
                end_time = frame.timestamp
                duration = end_time - start_time
                if duration >= silence_threshold_seconds:
                    chunk_count += 1
                    # Append [start_time, end_time, duration] to silence_timings rounded to 2 decimal places
                    silence_timings.append([round(start_time, 2), round(end_time, 2), round(duration, 2)])
                    # Add the formatted row to the table
                    start_min, start_sec = divmod(start_time, 60)
                    end_min, end_sec = divmod(end_time, 60)
                    table.append([
                        chunk_count,
                        f"{int(start_min):02}:{int(start_sec):02}",
                        f"{int(end_min):02}:{int(end_sec):02}",
                        f"{duration:.2f} seconds"
                    ])
            total_silence_duration = 0
            last_silence_timestamp = None
            start_time = None
            end_time = None
        else:  # Silence
            if last_silence_timestamp is None:
                start_time = frame.timestamp
                last_silence_timestamp = start_time

            total_silence_duration += frame.duration
            silent_frames.append(frame)

    # Check if there's any silence at the end after the last speech segment
    if last_silence_timestamp is not None:
        end_time = frames[-1].timestamp  # The last frame's timestamp
        duration = end_time - start_time
        if duration >= silence_threshold_seconds:
            chunk_count += 1
            silence_timings.append([round(start_time, 2), round(end_time, 2), round(duration, 2)])
            # Add the formatted row to the table
            start_min, start_sec = divmod(start_time, 60)
            end_min, end_sec = divmod(end_time, 60)
            table.append([
                chunk_count,
                f"{int(start_min):02}:{int(start_sec):02}",
                f"{int(end_min):02}:{int(end_sec):02}",
                f"{duration:.2f} seconds"
            ])

    # Print the table with the chunk details
    headers = ["Chunk Num", "Start Time (min)", "End Time (min)", "Duration"]
    print(tabulate(table, headers=headers, tablefmt="rounded_grid"))

    print(f"Total Chunks Which are Continuous Silent: {chunk_count}")

    # Return the list of silence periods [start_time, end_time, duration] rounded to 2 decimal points
    return silence_timings



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



def vad_collector(sample_rate, vad, frames, silence_timings, chunk_min_dur=chunk_min_dur, chunk_max_dur=chunk_max_dur):
    """Filters out non-voiced audio frames and collects continuous speech chunks of speech with silence removed."""
    silence_timings = silence_timings
    total_speech_duration = 0
    chunk_count = 0
    start_time = None
    end_time = None
    current_frames = []
    segments = []
    chunk_details = []  # This will store chunk info for printing in tabular format
    continous_silence = 0

    for frame in frames:
        is_speech = vad.is_speech(frame.bytes, sample_rate)
        if total_speech_duration == 0:
            start_time = frame.timestamp

        if is_speech:  # Speech frame
            continous_silence = 0
            current_frames.append(frame)
            total_speech_duration += frame.duration

            # If speech duration reaches chunk_max_dur, cut the chunk and create a new one
            if total_speech_duration >= chunk_max_dur:
                end_time = frame.timestamp + frame.duration
                duration = end_time - start_time
                chunk_count += 1
                segments.append(b''.join([f.bytes for f in current_frames]))  # Add the chunk

                # Store chunk details for tabulation
                start_min, start_sec = divmod(start_time, 60)
                end_min, end_sec = divmod(end_time, 60)
                chunk_details.append([
                    chunk_count,
                    f"{int(start_min):02}:{int(start_sec):02}",
                    f"{int(end_min):02}:{int(end_sec):02}",
                    f"{duration:.2f} seconds"
                ])

                # Reinitialize for next chunk
                current_frames = []
                total_speech_duration = 0
                start_time = None  # Ready for the next chunk

        else:  # Silence frame
            total_speech_duration += frame.duration
            current_frames.append(frame)
            # If we've passed the chunk_min_dur threshold and encounter silence
            if total_speech_duration >= chunk_min_dur:
                end_time = frame.timestamp
                duration = end_time - start_time
                continous_silence += frame.duration
                
                # If silence is detected, cut the chunk at this point
                if duration >= chunk_min_dur and duration <= chunk_max_dur:
                    if continous_silence >= silence_threshold:
                        chunk_count += 1
                        segments.append(b''.join([f.bytes for f in current_frames]))  # Add the chunk

                        # Store chunk details for tabulation
                        start_min, start_sec = divmod(start_time, 60)
                        end_min, end_sec = divmod(end_time, 60)
                        chunk_details.append([
                            chunk_count,
                            f"{int(start_min):02}:{int(start_sec):02}",
                            f"{int(end_min):02}:{int(end_sec):02}",
                            f"{duration:.2f} seconds"
                        ])

                        # Reinitialize for the next chunk
                        current_frames = []
                        total_speech_duration = 0
                        start_time = None  # Ready for the next chunk


    # If there are any remaining frames, output them as the last chunk
    if current_frames:
        end_time = frames[-1].timestamp + frames[-1].duration
        duration = end_time - start_time
        chunk_count += 1
        segments.append(b''.join([f.bytes for f in current_frames]))  # Add the final chunk

        # Store the final chunk's details for tabulation
        start_min, start_sec = divmod(start_time, 60)
        end_min, end_sec = divmod(end_time, 60)
        chunk_details.append([
            "Final",
            f"{int(start_min):02}:{int(start_sec):02}",
            f"{int(end_min):02}:{int(end_sec):02}",
            f"{duration:.2f} seconds"
        ])

    # Print the chunk details in a table format using tabulate
    headers = ["Chunk Num", "Start Time (min)", "End Time (min)", "Duration"]
    print("\nChunks Details:")
    print(tabulate(chunk_details, headers=headers, tablefmt="rounded_grid"))

    return segments



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
    silence_timings = silent_periods_collector(sample_rate, vad, frames)
    
    segments = vad_collector(sample_rate, vad, frames, silence_timings)
    for i, segment in enumerate(segments):
        path = 'chunk-%002d.wav' % (i,)
        # print(' Writing %s' % (path,))
        write_wave(path, segment, sample_rate)

if __name__ == '__main__':
    main(sys.argv[1:])
