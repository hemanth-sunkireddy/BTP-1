# import re
# import json
# from datetime import datetime, timedelta
# from Levenshtein import ratio

# def srt_to_list(srt_file):
#     """Parses the SRT file and extracts subtitles with timestamps."""
#     with open(srt_file, 'r', encoding='utf-8') as file:
#         content = file.read().strip()
    
#     srt_entries = []
#     blocks = re.split(r'\n\n', content)
#     for block in blocks:
#         lines = block.split('\n')
#         if len(lines) < 3:
#             continue
#         index = int(lines[0].lstrip("\ufeff"))
#         timestamp = lines[1]
#         text = ' '.join(lines[2:])
#         start_time, end_time = map(parse_srt_timestamp, timestamp.split(' --> '))
#         srt_entries.append({"index": index, "start": start_time, "end": end_time, "text": text})
#     return srt_entries

# def parse_srt_timestamp(timestamp):
#     """Converts SRT timestamp to seconds."""
#     time_obj = datetime.strptime(timestamp, "%H:%M:%S,%f")
#     return timedelta(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second, microseconds=time_obj.microsecond).total_seconds()

# def load_json(json_file):
#     """Loads JSON file containing word timestamps."""
#     with open(json_file, 'r', encoding='utf-8') as file:
#         return json.load(file)

# def align_phrases_to_words(srt_entries, word_data):
#     """Aligns phrases from the SRT file to words in the JSON file, handling substitutions and eliminations."""
#     aligned_data = []
#     word_index = 0
    
#     for entry in srt_entries:
#         phrase_words = entry['text'].split()
#         start_time, end_time = None, None
#         matched_words = []
        
#         for phrase_word in phrase_words:
#             best_match = None
#             best_score = 0.0
#             best_index = None
            
#             while word_index < len(word_data):
#                 word = word_data[word_index]
#                 score = ratio(phrase_word.lower(), word['text'].lower())
                
#                 if score > best_score:
#                     best_score = score
#                     best_match = word
#                     best_index = word_index
                
#                 if score > 0.8:  # Acceptable similarity threshold
#                     break
                
#                 word_index += 1
            
#             if best_match:
#                 matched_words.append(best_match)
#                 if start_time is None:
#                     start_time = best_match['start']
#                 end_time = best_match['end']
#                 word_index = best_index + 1  # Move to the next word
        
#         if matched_words:
#             aligned_data.append({
#                 "index": entry['index'],
#                 "srt_start": entry['start'],
#                 "srt_end": entry['end'],
#                 "calc_start": start_time,
#                 "calc_end": end_time,
#                 "text": entry['text']
#             })
    
#     return aligned_data

# def calculate_difference(aligned_data):
#     """Calculates the timestamp difference between SRT and word-level JSON."""
#     count=0
#     count2=0
#     for entry in aligned_data:
#         srt_duration = entry['srt_end'] - entry['srt_start']
#         calculated_duration = entry['calc_end'] - entry['calc_start']
#         difference = abs((entry['srt_start'] - entry['calc_start']) + (entry['srt_end'] - entry['calc_end'])) / 2
#         if (difference>0.4):
#             count2+=1
#         if (abs(entry['srt_start']-entry['calc_start'])>=0.4 or abs(entry['srt_end'] - entry['calc_end'])>=0.4):
#             count+=1
#         print(f"SRT Index: {entry['index']}")
#         print(f"SRT Start: {entry['srt_start']:.3f}, SRT End: {entry['srt_end']:.3f}")
#         print(f"Calculated Start: {entry['calc_start']:.3f}, Calculated End: {entry['calc_end']:.3f}")
#         print(f"Time Difference: {difference:.3f} seconds\n")
#     print(f"condition1: {count} out of {len(aligned_data)} phrases has timestamp error more than 40ms")
#     print(f"condition2: {count2} out of {len(aligned_data)} phrases has timestamp error more than 40ms")
# # Example usage:
# srt_entries = srt_to_list("text/actual_2.srt")
# word_data = load_json("text/audio_2_only_words_mfa.json")
# aligned_data = align_phrases_to_words(srt_entries, word_data)
# calculate_difference(aligned_data)


import re
import json
import pandas as pd
from datetime import datetime, timedelta
from Levenshtein import ratio

def srt_to_list(srt_file):
    """Parses the SRT file and extracts subtitles with timestamps."""
    with open(srt_file, 'r', encoding='utf-8') as file:
        content = file.read().strip()
    
    srt_entries = []
    blocks = re.split(r'\n\n', content)
    for block in blocks:
        lines = block.split('\n')
        if len(lines) < 3:
            continue
        index = int(lines[0].lstrip("\ufeff"))
        timestamp = lines[1]
        text = ' '.join(lines[2:])
        start_time, end_time = map(parse_srt_timestamp, timestamp.split(' --> '))
        srt_entries.append({"index": index, "start": start_time, "end": end_time, "text": text})
    return srt_entries

def parse_srt_timestamp(timestamp):
    """Converts SRT timestamp to seconds."""
    time_obj = datetime.strptime(timestamp, "%H:%M:%S,%f")
    return timedelta(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second, microseconds=time_obj.microsecond).total_seconds()

def load_json(json_file):
    """Loads JSON file containing word timestamps."""
    with open(json_file, 'r', encoding='utf-8') as file:
        return json.load(file)

def align_phrases_to_words(srt_entries, word_data):
    """Aligns phrases from the SRT file to words in the JSON file, handling substitutions and eliminations."""
    aligned_data = []
    word_index = 0
    
    for entry in srt_entries:
        phrase_words = entry['text'].split()
        start_time, end_time = None, None
        matched_words = []
        
        for phrase_word in phrase_words:
            best_match = None
            best_score = 0.0
            best_index = None
            
            while word_index < len(word_data):
                word = word_data[word_index]
                score = ratio(phrase_word.lower(), word['text'].lower())
                
                if score > best_score:
                    best_score = score
                    best_match = word
                    best_index = word_index
                
                if score > 0.8:  # Acceptable similarity threshold
                    break
                
                word_index += 1
            
            if best_match:
                matched_words.append(best_match)
                if start_time is None:
                    start_time = best_match['start']
                end_time = best_match['end']
                word_index = best_index + 1  # Move to the next word
        
        if matched_words:
            aligned_data.append({
                "index": entry['index'],
                "srt_start": entry['start'],
                "srt_end": entry['end'],
                "calc_start": start_time,
                "calc_end": end_time,
                "text": entry['text']
            })
    
    return aligned_data

def calculate_difference(aligned_data, excel_filename="audio_3_timestamp_accuracy_mfa.xlsx"):
    """Calculates the timestamp difference and stores results in an Excel file."""
    count = 0
    count2 = 0
    data = []

    for entry in aligned_data:
        srt_duration = entry['srt_end'] - entry['srt_start']
        calculated_duration = entry['calc_end'] - entry['calc_start']
        difference = abs((entry['srt_start'] - entry['calc_start']) + (entry['srt_end'] - entry['calc_end'])) / 2

        if difference > 0.04:
            count2 += 1
        if abs(entry['srt_start'] - entry['calc_start']) >= 0.04 or abs(entry['srt_end'] - entry['calc_end']) >= 0.04:
            count += 1

        data.append([
            entry['index'],
            entry['srt_start'],
            entry['srt_end'],
            entry['calc_start'],
            entry['calc_end'],
            difference,
            entry['text']
        ])

    print(f"condition1: {count} out of {len(aligned_data)} phrases has timestamp error more than 40ms")
    print(f"condition2: {count2} out of {len(aligned_data)} phrases has timestamp error more than 40ms")

    # Create DataFrame for aligned data
    df = pd.DataFrame(data, columns=[
        "Index", "SRT Start", "SRT End", "Calculated Start", "Calculated End", "Time Difference", "Text"
    ])

    # Create a summary DataFrame
    summary_df = pd.DataFrame({
        "Condition": ["Condition 1", "Condition 2"],
        "Count": [count, count2]
    })

    # Save to Excel with multiple sheets
    with pd.ExcelWriter(excel_filename, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Aligned Data", index=False)
        summary_df.to_excel(writer, sheet_name="Summary", index=False)

    print(f"Excel file saved as {excel_filename}")

# Example usage:
srt_entries = srt_to_list("text/actual_3.srt")
word_data = load_json("text/audio_3_only_words_mfa.json")
aligned_data = align_phrases_to_words(srt_entries, word_data)
calculate_difference(aligned_data)
