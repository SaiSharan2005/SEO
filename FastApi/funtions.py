from transformers import BartForConditionalGeneration, BartTokenizer
from moviepy.editor import VideoFileClip
import speech_recognition as sr
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from keybert import KeyBERT
import string

# NLTK and model initialization
nltk.download('punkt')
nltk.download('stopwords')

r = sr.Recognizer()
kw_model = KeyBERT()
stop_words = set(stopwords.words('english'))
punctuation = set(string.punctuation)

# Load BART model and tokenizer
bart_model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
bart_tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

# Functions
def video_to_wav(input_video_path, output_audio_path):
    try:
        video = VideoFileClip(input_video_path)
        audio = video.audio
        audio.write_audiofile(output_audio_path, codec='pcm_s16le')
        print(f"Audio successfully extracted and saved to {output_audio_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def wav_to_text(file_path):
    with sr.WavFile(file_path) as source:
        audio_text = r.record(source)
    try:
        return r.recognize_google(audio_text)
    except sr.RequestError as e:
        print(f"API request failed: {e}")
        return "API request failed"
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
        return "Speech not recognized"

def summarize_text_with_bart(text, max_length=130, min_length=30):
    inputs = bart_tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = bart_model.generate(inputs, max_length=max_length, min_length=min_length, length_penalty=2.0, num_beams=4, early_stopping=True)
    return bart_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def generate_keywords_with_bart(text):
    """
    Integrates BART summarization with keyword generation.
    1. Summarizes the text using BART.
    2. Extracts keywords from the summary.
    """
    # Summarize the text
    summarized_text = summarize_text_with_bart(text)
    print("Summarized Text:", summarized_text)
    
    # Tokenize and extract keywords
    words = word_tokenize(summarized_text.lower())
    keywords = [word for word in words if word.isalpha() and word not in stop_words]
    keyword_freq = Counter(keywords)
    most_common_keywords = keyword_freq.most_common(12)
    return [keyword for keyword, _ in most_common_keywords]

def seo_rank_for_keywords(text, keywords):
    """
    Ranks keywords (both seed and generated) based on their frequency in the provided text.
    
    :param text: The input text to analyze.
    :param keywords: A list of keywords to rank.
    :return: A list of keywords ranked by their frequency in the text.
    """
    # Tokenize the input text and convert to lowercase
    words = word_tokenize(text.lower())
    
    # Create a frequency count for the words in the text
    word_freq = Counter(words)
    
    # Rank the keywords based on their frequency in the text
    keyword_ranking = []
    for keyword in keywords:
        keyword_lower = keyword.lower()
        frequency = word_freq.get(keyword_lower, 0)
        keyword_ranking.append((keyword, frequency))
    
    # Sort the keywords by their frequency (descending order)
    keyword_ranking.sort(key=lambda x: x[1], reverse=True)
    
    return keyword_ranking

def generate_keywords_with_bart_and_seeds(text, seed_keywords):
    """
    Combines BART summarization-based keywords with seed keywords provided by the user,
    Ranks all keywords (seed and BART-generated) based on their frequency in the transcribed text (SEO rank).
    
    :param text: The input text to process.
    :param seed_keywords: A list of seed keywords to include in the final keyword list.
    :return: A combined list of keywords and their SEO rankings.
    """
    # Generate keywords from BART summarization
    bart_keywords = generate_keywords_with_bart(text)
    print("BART-Generated Keywords:", bart_keywords)
    
    # Combine seed and BART keywords
    combined_keywords = bart_keywords + seed_keywords
    
    # Rank the combined keywords based on SEO (frequency in the text)
    keyword_ranking = seo_rank_for_keywords(text, combined_keywords)
    print("SEO Ranking of All Keywords:", keyword_ranking)
    
    # Remove duplicates from the combined keywords list
    final_keywords = list(set(bart_keywords + seed_keywords))
    
    return final_keywords, keyword_ranking

# Example Usage
if __name__ == "__main__":
    # Extract text from video
    video_to_wav("input_video.mp4", "output_audio.wav")
    transcribed_text = wav_to_text("output_audio.wav")

    # Seed keywords provided by the user
    seed_keywords = ["artificial intelligence", "deep learning", "NLP"]

    # Generate keywords with BART integration and seed keywords
    combined_keywords, keyword_ranking = generate_keywords_with_bart_and_seeds(transcribed_text, seed_keywords)
    print("Final Keywords (BART + Seed):", combined_keywords)
    print("SEO Ranking of All Keywords:", keyword_ranking)
