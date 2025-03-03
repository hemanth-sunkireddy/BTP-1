import jiwer

# reference = "the quick brown fox jumps over the lazy dog"
# hypothesis = "the quick brown fox jump over lazy dog"
ref_file="text/actual_1.txt"
hyp_file="text/transcribed_1.txt"

with open(ref_file, 'r', encoding='utf-8') as f1, \
    open(hyp_file, 'r', encoding='utf-8') as f2:
    reference = f1.read()
    hypothesis = f2.read()
wer = jiwer.wer(reference, hypothesis)
print(f"WER: {wer:.2%}")

