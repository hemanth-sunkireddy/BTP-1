import matplotlib.pyplot as plt

# Given data
# video_duration = [1.02,3.75,10.26,20.01,30.0,40.05,50.04,124.02,281.58,656.4]
# audio_decode_time = [1.9470982551574707,2.236215829849243,2.926987409591675,4.59657096862793,8.741004228591919,7.570902585983276,9.268781423568726,25.47396445274353,55.76341104507446,136.96675205230713]

video_duration = [1.02, 3.03, 5.01, 10.02, 20.01, 30.0, 40.02, 50.01, 60.0, 125.01, 280.02, 650.01, 1801.14]
audio_decode_time = [1.8068888187408447, 2.0778377056121826, 2.72623610496521, 2.912597179412842, 4.800200700759888, 7.316509962081909, 8.122992753982544, 9.500887870788574, 13.072041273117065, 27.45095133781433, 57.35416603088379, 135.15591168403625, 366.500568151474]
# Scatter plot
plt.figure(figsize=(10, 5))
plt.scatter(video_duration, audio_decode_time, color='b', marker='o')
plt.xlabel('Video Duration (seconds)')
plt.ylabel('Audio Decode Time (seconds)')
plt.title('Scatter Plot of Video Duration vs. Audio Decode Time')
plt.grid(True)
plt.show()

# Line plot
plt.figure(figsize=(10, 5))
plt.plot(video_duration, audio_decode_time, marker='o', linestyle='-')
plt.xlabel('Video Duration (seconds)')
plt.ylabel('Audio Decode Time (seconds)')
plt.title('Line Plot of Video Duration vs. Audio Decode Time')
plt.grid(True)
plt.show()

# Bar chart
plt.figure(figsize=(10, 5))
plt.bar(range(len(video_duration)), audio_decode_time, tick_label=[str(vd) for vd in video_duration], color='g')
plt.xlabel('Video Duration (seconds)')
plt.ylabel('Audio Decode Time (seconds)')
plt.title('Bar Chart of Video Duration vs. Audio Decode Time')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()
