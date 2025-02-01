import contextlib
import sys
import wave
import webrtcvad
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate  

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

def plot_vad(audio, sample_rate, frames, vad):
    # Convert audio to numpy array for plotting
    audio_int = np.frombuffer(audio, dtype=np.int16)
    
    # Create a list for the VAD output (1 for speech, 0 for silence)
    vad_output = []
    timestamps = []  # To track timestamps for X-axis
    
    # Process each frame with the VAD
    for frame in frames:
        is_speech = vad.is_speech(frame.bytes, sample_rate)
        num_samples_in_frame = len(frame.bytes) // 2  # Convert from bytes to samples (16-bit audio)
        
        # Repeat the is_speech value for each sample in the frame
        vad_output.extend([is_speech] * num_samples_in_frame)
        timestamps.extend([frame.timestamp] * num_samples_in_frame)
    
    # Plotting the VAD output using scatter plot (dots instead of line)
    plt.figure(figsize=(16, 8))  # Adjust these values as needed for your screen resolution
    plt.plot(timestamps, vad_output, label="VAD (Speech: 1, Silence: 0)", color='blue', lw=0.5)  # lw controls line width
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
        sys.stderr.write(
            'Usage: example.py <aggressiveness> <path to wav file>\n')
        sys.exit(1)
    audio, sample_rate = read_wave(args[1])
    vad = webrtcvad.Vad(int(args[0]))
    frames = frame_generator(30, audio, sample_rate)
    frames = list(frames)
    # Plotting the Graph (X Axis is Frames in ms and Y Axis is Speech or Not)
    # plot_vad(audio, sample_rate, frames, vad)
    segments = vad_collector(sample_rate, 30, 300, vad, frames)
    
    # Combine all voiced segments into a single audio file
    combined_audio = b""
    for i, segment in enumerate(segments):
        path = 'chunk-%002d.wav' % (i,)
        # print(' Writing %s' % (path,))
        write_wave(path, segment, sample_rate)
        combined_audio += segment  # Combine the segments

    # # Write the combined audio to a new file
    # print('Writing combined audio to silence_remove.wav')
    # write_wave('silence_remove.wav', combined_audio, sample_rate)
    

if __name__ == '__main__':
    main(sys.argv[1:])
