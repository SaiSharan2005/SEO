from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import os
import nltk
from funtions import *
nltk.download('punkt')

app = FastAPI()

# Directory to store uploaded videos
UPLOAD_DIRECTORY = "uploaded_videos"

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

# Configure CORS to allow specific origins or allow all
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins or specify a list like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    # Validate the file type
    if not file.filename.endswith(('.mp4', '.avi', '.mov', '.mkv')):
        return {"error": "Invalid file type. Only video files are allowed."}

    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)

    # Save the uploaded video file
    with open(file_path, "wb") as video_file:
        video_file.write(await file.read())

    return {"filename": file.filename, "message": "Video uploaded successfully."}

@app.post("/keyword-with-keybert/")
async def keyword_with_keybert(file: UploadFile = File(...)):
    # Validate the file type
    if not file.filename.endswith(('.mp4', '.avi', '.mov', '.mkv')):
        return {"error": "Invalid file type. Only video files are allowed."}

    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    audio_path = os.path.join(UPLOAD_DIRECTORY, file.filename.split(".")[0]+".wav")

    # Save the uploaded video file
    with open(file_path, "wb") as video_file:
        video_file.write(await file.read())
    
    video_to_wav(file_path,audio_path)
    text = wav_to_text(audio_path)
    keyWords = generate_keywords_with_keybert(text)
    return {"keywords": keyWords, "message": "Keywords Generated successfully."}

# New route that accepts both video and seed keywords
@app.post("/keyword-with-keybert-seed/")
async def keyword_with_keybert_seed(file: UploadFile = File(...), seed_keywords: str = Form(...)):
    """
    Extract keywords from the video using KeyBERT, incorporating a list of seed keywords provided by the user.
    
    :param file: The uploaded video file.
    :param seed_keywords: A comma-separated list of seed keywords provided as a form field.
    """
    # Validate the file type
    if not file.filename.endswith(('.mp4', '.avi', '.mov', '.mkv')):
        return {"error": "Invalid file type. Only video files are allowed."}

    # Save the uploaded video
    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    audio_path = os.path.join(UPLOAD_DIRECTORY, file.filename.split(".")[0]+".wav")

    with open(file_path, "wb") as video_file:
        video_file.write(await file.read())

    # Convert video to audio (wav) and extract text
    video_to_wav(file_path, audio_path)
    text = wav_to_text(audio_path)

    # Process the seed keywords input (comma-separated list)
    seed_keywords_list = [keyword.strip() for keyword in seed_keywords.split(',') if keyword.strip()]

    # Generate keywords using the provided seed keywords and the extracted text
    keyWords = extract_keywords_with_seeds(text, seed_keywords_list)

    return {"keywords": keyWords, "seed_keywords": seed_keywords_list, "message": "Keywords Generated successfully with seed keywords."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
