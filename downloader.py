# backend/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pytube import YouTube
from fastapi.responses import RedirectResponse
from urllib.parse import quote

app = FastAPI()

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your GitHub Pages URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/fetch")
async def fetch_streams(request: Request):
    data = await request.json()
    url = data.get("url")
    try:
        yt = YouTube(url)
        streams = yt.streams

        video_streams = []
        audio_streams = []

        for stream in streams:
            if stream.type == "video" and stream.resolution:
                video_streams.append({
                    "itag": stream.itag,
                    "resolution": stream.resolution,
                    "mime": stream.mime_type,
                })
            elif stream.type == "audio":
                audio_streams.append({
                    "itag": stream.itag,
                    "bitrate": stream.abr,
                    "mime": stream.mime_type,
                })

        return {
            "title": yt.title,
            "video": video_streams,
            "audio": audio_streams
        }
    except Exception as e:
        print(f"Error: {e}")
        return {"error": "Unable to fetch video details"}

@app.get("/download")
async def download_video(url: str, video_itag: str, audio_itag: str, filename: str):
    try:
        yt = YouTube(url)
        video_stream = yt.streams.get_by_itag(video_itag)
        audio_stream = yt.streams.get_by_itag(audio_itag)

        # Pick video if only one is requested
        final_stream = video_stream or audio_stream

        return RedirectResponse(final_stream.url)
    except Exception as e:
        print(f"Download Error: {e}")
        return {"error": "Failed to generate download link"}
