import os
import tempfile
from uuid import uuid4
from pytubefix import YouTube
import openai
from dotenv import load_dotenv

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def download_youtube_audio(youtube_url: str):
    """Download YouTube audio-only stream as an .mp4 and return its path + title."""
    print("📥 Downloading audio:", youtube_url)
    yt = YouTube(youtube_url, use_oauth=False, allow_oauth_cache=False)
    print("🎞️ Title:", yt.title)

    # pick the best audio-only stream container (usually mp4 or webm)
    stream = yt.streams.filter(only_audio=True).order_by("abr").desc().first()
    if not stream:
        raise Exception("No audio‐only stream available.")

    # use a temp directory so we don't worry about permissions
    tmpdir = tempfile.mkdtemp()
    out_path = os.path.join(tmpdir, f"{uuid4()}.{stream.subtype}")

    stream.download(output_path=tmpdir, filename=os.path.basename(out_path))
    print("✅ Downloaded to:", out_path)
    return out_path, yt.title

def transcribe_with_whisper(audio_path: str) -> str:
    """Use the new openai.audio.transcriptions.create interface (openai>=1.0.0)."""
    with open(audio_path, "rb") as audio_file:
        transcription = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json"
        )
    return {
        "text": transcription.text,
        "segments": transcription.segments  # list of segment objects
    }

def translate_transcript(transcript: str, target_language: str) -> str:
    """Use the new openai.chat.completions.create interface (openai>=1.0.0)."""
    system_prompt = (
        f"You are a professional translator. Translate the following transcript into {target_language}. "
        "Preserve meaning and context; return only the translated text."
    )
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": transcript}
        ]
    )
    # access the content via the .message attribute
    return response.choices[0].message.content

