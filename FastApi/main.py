from fastapi import FastAPI, File, UploadFile
from funtions import *
import os
import nltk

nltk.download('punkt')

app = FastAPI()

# Directory to store uploaded videos
UPLOAD_DIRECTORY = "uploaded_videos"

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

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

    # Save the uploaded video file
    with open(file_path, "wb") as video_file:
        video_file.write(await file.read())
    
    # video_to_wav(file.filename,UPLOAD_DIRECTORY+'/'+'test.wav')
    text = wav_to_text(UPLOAD_DIRECTORY+'/'+'test.wav')
    keyWords = generate_keywords(text)

    return {"keywords": keyWords, "message": "Keywords Generated successfully."}



import nltk
nltk.data.path.append('/home/sharan/miniconda3/nltk_data')  # Add custom path if needed
nltk.download('punkt', download_dir='/home/sharan/miniconda3/nltk_data')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
