# backend/api.py
from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from .media_utils import download_youtube_audio

app = FastAPI()

@app.get("/process_youtube")
def process_youtube_link(url: str = Query(...), lang: str = Query(default="en")):
    try:
        audio_path, title = download_youtube_audio(url)
        return {
            "message": f"Downloaded audio for: {title}",
            "path": audio_path
        }
    except Exception as e:
        print(f"🔥 ERROR: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Welcome to Global Voice API!"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    return {"filename": file.filename, "size": len(contents)}

