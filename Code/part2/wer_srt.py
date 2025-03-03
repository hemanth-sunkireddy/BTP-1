import pysrt
import editdistance
import re

def preprocess_text(text):
    """
    Preprocess text by:
    1. Converting to lowercase
    2. Removing punctuation
    3. Splitting into words
    """
    text = re.sub(r'[^\w\s]', '', text.lower())
    return text.split()

def get_srt_text(srt_file):
    subs = pysrt.open(srt_file)
    return ' '.join([sub.text for sub in subs])

def calculate_wer(reference_file, hypothesis_file):
   
    ref_text = get_srt_text(reference_file)
    hyp_text = get_srt_text(hypothesis_file)
    
    ref_words = preprocess_text(ref_text)
    hyp_words = preprocess_text(hyp_text)
    
    
    distance = editdistance.eval(ref_words, hyp_words)
    
    # Calculate WER
    wer = distance / len(ref_words)
    
    return {
        'reference_words': len(ref_words),
        'hypothesis_words': len(hyp_words),
        'edit_distance': distance,
        'word_error_rate': wer,
        'error_rate_percentage': wer * 100
    }

def main():
    reference_srt = 'text/actual_1.srt'
    hypothesis_srt = 'text/transcribed_1.srt'
    
    try:
        wer_results = calculate_wer(reference_srt, hypothesis_srt)
        
        print("Word Error Rate (WER) Analysis:")
        print(f"Reference Words: {wer_results['reference_words']}")
        print(f"Hypothesis Words: {wer_results['hypothesis_words']}")
        print(f"Edit Distance: {wer_results['edit_distance']}")
        print(f"WER: {wer_results['word_error_rate']:.4f}")
        print(f"WER Percentage: {wer_results['error_rate_percentage']:.2f}%")
    
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()