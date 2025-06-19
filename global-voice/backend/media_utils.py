# backend/media_utils.py
import os
import ffmpeg
from uuid import uuid4
from pytubefix import YouTube

def download_youtube_audio(youtube_url: str, output_dir: str = "temp"):
    """Downloads lowest-res YouTube video, extracts audio, and returns MP3 path and title."""

    print("📥 Downloading from:", youtube_url)

    try:
        yt = YouTube(
            youtube_url,
            use_oauth=False,
            allow_oauth_cache=False
        )
        print("🎞️ Video title:", yt.title)

        stream = yt.streams.get_lowest_resolution()
        if not stream:
            raise ValueError("No suitable stream found.")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        video_path = os.path.join(output_dir, f"{uuid4()}.mp4")
        audio_path = os.path.join(output_dir, f"{uuid4()}.mp3")

        stream.download(output_path=output_dir, filename=os.path.basename(video_path))
        print("✅ Video downloaded:", video_path)

        # Extract audio
        ffmpeg.input(video_path).output(audio_path).run(overwrite_output=True)
        print("🎧 Audio extracted:", audio_path)

        # Clean up original video
        os.remove(video_path)

        return audio_path, yt.title

    except Exception as e:
        print(f"🔥 ERROR: {e}")
        raise
