from moviepy.editor import VideoFileClip
import speech_recognition as sr
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from keybert import KeyBERT

# Download the required NLTK data files
nltk.download('punkt')

# print(sr.__version__)
r = sr.Recognizer()

kw_model = KeyBERT()


def video_to_wav(input_video_path, output_audio_path):
    try:
        # Load the video file
        video = VideoFileClip(input_video_path)
        
        # Extract audio from the video
        audio = video.audio
        
        # Write the audio to a WAV file
        audio.write_audiofile(output_audio_path, codec='pcm_s16le')
        
        print(f"Audio successfully extracted and saved to {output_audio_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
# video_to_wav('abc1.mp4', 'output_audio.wav')

def wav_to_text(file_path):
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio_text = r.record(source)
    
    try:
        response_text = r.recognize_google(audio_text)
    except sr.RequestError as e:
        # API was unreachable or unresponsive
        print(f"API request failed: {e}")
        return "API request failed"
    except sr.UnknownValueError:
        # Speech was unintelligible
        print("Google Speech Recognition could not understand the audio")
        return "Speech not recognized"
    
    return response_text




def generate_keywords(text):
    # Tokenize the input text
    words = word_tokenize(text.lower())
    
    # Remove stopwords and non-alphabetic tokens
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in words if word.isalpha() and word not in stop_words]
    
    # Count the frequency of each keyword
    keyword_freq = Counter(keywords)
    
    # Sort keywords by frequency and return the most common ones
    most_common_keywords = keyword_freq.most_common(12)  # Top 12 keywords
    return [keyword for keyword, _ in most_common_keywords]

# Input text
# text = """Hello guys welcome to Amit Thinks in this video we  will learn how to download and install the current MySQL version we will install MySQL Server  shell as well as Workbench let's start after installing you can also refer to a free 3 hours  MySQL tutorial the link is in the description of this video Let's start! Go to the web browser  I am using Chrome you can use any web browser on Google type MySQL and uh press enter open  the official website myql.com here it is Click downloads go below and click here MySQL Community
# downloads now go to MySQL installer for Windows the following is the current version okay  8.0.37 and for Windows two versions are visible it's written 32-bit but  works for both 32-bit as well as 64-bit Windows 11 operating system I'll go  for the second one Okay click the download button now here click no thanks just start  my download started here it is let's wait 296 MB the download is successful click and  click open minimize now the installation will start now let us choose a setup type the  installation started I'll go for custom
# click next now under select products click on  MySQL servers click it again and reach here click the arrow to drag now go to Applications  MySQL workbench and do the same drag and do the same for Shell drag it click next okay it will  also check the requirements and it will install the following as well you may or may not get  this requirement if you're already having this redistributable package it won't get installed  click execute we were not having it so it is installing click I agree install successful click close we  have installed it click next now
# it will install MySQL click  execute one by one it will install we have installed it click next click  next again type in networking the port number is 3306 click next Authentication Method  Keep it at default that means strong and it is recommended click next now you need  to set the password root means the admin you are the admin of the MySQL on this  system on your system so add a password some people got stuck here and were unable  to set a strong password so you can use my password this is only on the local system not  on the server so we can use any password click
# next you can also use your password as I told  before click next Windows service click next file permissions yes keep it as it is the default  click next the last step apply configuration click execute the configuration is  successful and the installation also click finish next it will also open  MySQL Workbench when I'll click finish no problem okay it is opening here it is workbench  let us set the path it was in C drive program files MySQL Server bin and that's it this is  the complete path copy minimize go to start
# type type environment and click here that  is edit the system environment variables click open under system properties Advanced  click environment variables under system variables go to path double click click  new and right-click paste the same MySQL bin path Okay click okay okay and the  last okay now go to start type CMD open it now let us verify the installation  we have completed the installation mysql --version and we successfully  installed 8.0.37 now let us begin the server type the command mysql -u u means  user so our user was root and -p p means
# password when I'll press enter it will ask  the same password so I'll mention the same password here it is successful now let us type some quick commands show databases  semicolon these are the default databases let us quickly create a new database  create databases database name let's say my database name is amitdb you can add any name press  enter and we created it because it's written query okay now type the same command show databases and  you can see amitdb database is visible that means we successfully created it let us know the path  of this database it will be under C drive Program
# Data if you're not getting this because it would  be hidden on Windows 11 go to view show and click on this option hidden items I'll uncheck and it  will vanish you can see I'll just click hidden items and it's visible here go inside go to MySQL  server and here is your data folder click continue here is your amitdb same amitdb database you can  always take a backup from here so you should know this path okay guys so we have created a database  okay now we can open workbench also click here enter the same password select save password  and click okay we are inside MySQL workbench
# workbench is like a UI for MySQL if you don't  want to type these commands you can directly go here you can also type commands here if you want a  free MySQL to tutorial as well as MySQL workbench tutorial refer the link in the description of  this video thank you for watching the video"""

# # Generate and print keywords
# keywords = generate_keywords(text)
# print("Keywords:", keywords)


def generate_keywords_with_ranking(text):
    # Tokenize the input text
    words = word_tokenize(text.lower())
    
    # Remove stopwords and non-alphabetic tokens
    stop_words = set(stopwords.words('english'))
    keywords = [word for word in words if word.isalpha() and word not in stop_words]
    
    # Count the frequency of each keyword
    keyword_freq = Counter(keywords)
    
    # Calculate SEO ranking based on frequency
    total_keywords = sum(keyword_freq.values())  # Total number of keywords in the text
    
    # Create a list of keywords with their frequency and SEO ranking score
    keyword_ranking = []
    for keyword, freq in keyword_freq.items():
        ranking_score = round((freq / total_keywords) * 100, 2)  # SEO score based on frequency
        keyword_ranking.append((keyword, freq, ranking_score))
    
    # Sort keywords by ranking score (highest score first)
    keyword_ranking.sort(key=lambda x: x[2], reverse=True)
    
    return keyword_ranking

# # Input text
# text = """Hello guys welcome to Amit Thinks in this video we  will learn how to download and install the current MySQL version we will install MySQL Server  shell as well as Workbench let's start after installing you can also refer to a free 3 hours  MySQL tutorial the link is in the description of this video Let's start! Go to the web browser  I am using Chrome you can use any web browser on Google type MySQL and uh press enter open  the official website myql.com here it is Click downloads go below and click here MySQL Community
# downloads now go to MySQL installer for Windows the following is the current version okay  8.0.37 and for Windows two versions are visible it's written 32-bit but  works for both 32-bit as well as 64-bit Windows 11 operating system I'll go  for the second one Okay click the download button now here click no thanks just start  my download started here it is let's wait 296 MB the download is successful click and  click open minimize now the installation will start now let us choose a setup type the  installation started I'll go for custom
# click next now under select products click on  MySQL servers click it again and reach here click the arrow to drag now go to Applications  MySQL workbench and do the same drag and do the same for Shell drag it click next okay it will  also check the requirements and it will install the following as well you may or may not get  this requirement if you're already having this redistributable package it won't get installed  click execute we were not having it so it is installing click I agree install successful click close we  have installed it click next now
# it will install MySQL click  execute one by one it will install we have installed it click next click  next again type in networking the port number is 3306 click next Authentication Method  Keep it at default that means strong and it is recommended click next now you need  to set the password root means the admin you are the admin of the MySQL on this  system on your system so add a password some people got stuck here and were unable  to set a strong password so you can use my password this is only on the local system not  on the server so we can use any password click
# next you can also use your password as I told  before click next Windows service click next file permissions yes keep it as it is the default  click next the last step apply configuration click execute the configuration is  successful and the installation also click finish next it will also open  MySQL Workbench when I'll click finish no problem okay it is opening here it is workbench  let us set the path it was in C drive program files MySQL Server bin and that's it this is  the complete path copy minimize go to start
# type type environment and click here that  is edit the system environment variables click open under system properties Advanced  click environment variables under system variables go to path double click click  new and right-click paste the same MySQL bin path Okay click okay okay and the  last okay now go to start type CMD open it now let us verify the installation  we have completed the installation mysql --version and we successfully  installed 8.0.37 now let us begin the server type the command mysql -u u means  user so our user was root and -p p means
# password when I'll press enter it will ask  the same password so I'll mention the same password here it is successful now let us type some quick commands show databases  semicolon these are the default databases let us quickly create a new database  create databases database name let's say my database name is amitdb you can add any name press  enter and we created it because it's written query okay now type the same command show databases and  you can see amitdb database is visible that means we successfully created it let us know the path  of this database it will be under C drive Program
# Data if you're not getting this because it would  be hidden on Windows 11 go to view show and click on this option hidden items I'll uncheck and it  will vanish you can see I'll just click hidden items and it's visible here go inside go to MySQL  server and here is your data folder click continue here is your amitdb same amitdb database you can  always take a backup from here so you should know this path okay guys so we have created a database  okay now we can open workbench also click here enter the same password select save password  and click okay we are inside MySQL workbench
# workbench is like a UI for MySQL if you don't  want to type these commands you can directly go here you can also type commands here if you want a  free MySQL to tutorial as well as MySQL workbench tutorial refer the link in the description of  this video thank you for watching the video"""

# # Generate keywords with SEO ranking
# keywords_with_ranking = generate_keywords_with_ranking(text)

# # Print keywords with their frequency and SEO ranking
# print("Keyword | Frequency | SEO Ranking (%)")
# for keyword, freq, rank in keywords_with_ranking:
#     print(f"{keyword} | {freq} | {rank}%")


def generate_keywords_with_keybert():
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=10)
    return keywords