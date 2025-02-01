# Tasks
* Extraction of Audios from Videos and Run the VAD algorithm. [Implemented Silero and WebRTC algorithms]
* Run the VAD algorithm on our extracted audios and plot those with VAD decisions.

## Dividing Large Audio files into smaller chunks
1. Speech boundaries (Sentence structure along with punctuation or Pause-based)
    * If the speech contains noticeable pauses (silent gaps between sentences), we'll set a threshold for the duration of the pause that qualifies as a sentence boundary.
    * Then combine smaller chunks into their nearest chunks with monitoring max and min durations of the audio file.

### Tomorrow task
1. In the Plotted graph identify silence part of threshold value and Display total count of silence values and which parts and the remaining everything in the graphs on atleast 10 videos.
2. If 90% of frames in the sliding window are speech, it accumulates them; if 90% are silence, it yields the accumulated speech as a chunk.
3. If there is a pause then remove in between the sentences. And add small padding silence at both ends of the audio.
4. Continous silence parts vs Continous non-silence parts.
5. Instead of just check for frames where Voiced frames sum upto 10sec.