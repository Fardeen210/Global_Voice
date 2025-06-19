# backend/api.py
from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .media_utils import (
    download_youtube_audio, 
    transcribe_with_whisper, 
    translate_transcript,
)
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/process_youtube")
def process_youtube_link(url: str = Query(...), lang: str = Query(default="en")):
    audio_path = None
    try:
        audio_path, title = download_youtube_audio(url)
        transcript = transcribe_with_whisper(audio_path)
        translation = translate_transcript(transcript, lang)

        return {
            "title": title,
            "original_transcript": transcript,
            "translated_transcript": translation,
            "target_language": lang
        }

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"🔥 Server error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to Global Voice API!"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Validate file type
    allowed_types = ["audio/", "video/"]
    if not any(file.content_type.startswith(t) for t in allowed_types):
        raise HTTPException(status_code=400, detail="Only audio and video files are allowed")
    
    # Validate file size (10MB limit)
    max_size = 10 * 1024 * 1024  # 10MB
    contents = await file.read()
    if len(contents) > max_size:
        raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")
    
    return {"filename": file.filename, "size": len(contents)}

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Global Voice API"}

