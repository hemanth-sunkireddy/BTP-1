def extract_srt_text(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as srt_file, \
         open(output_file, 'w', encoding='utf-8') as txt_file:
        
        for line in srt_file:
            if '-->' in line or line.strip().isdigit():
                continue
            if line.strip():
                txt_file.write(line.strip() + ' ')

extract_srt_text('text/actual_3.srt', 'text/actual_3.txt')