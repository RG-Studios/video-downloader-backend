from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pytube import YouTube
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "YouTube Downloader Backend Running"

@app.route('/fetch', methods=['POST'])
def fetch_options():
    data = request.json
    url = data.get('url')

    try:
        yt = YouTube(url)
        streams = yt.streams

        video_streams = []
        audio_streams = []

        for stream in streams:
            if stream.mime_type.startswith("video") and stream.resolution:
                video_streams.append({
                    "itag": stream.itag,
                    "resolution": stream.resolution,
                    "mime": stream.mime_type
                })
            elif stream.mime_type.startswith("audio"):
                audio_streams.append({
                    "itag": stream.itag,
                    "bitrate": stream.abr,
                    "mime": stream.mime_type
                })

        return jsonify({
            "title": yt.title,
            "video": video_streams,
            "audio": audio_streams
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download')
def download_video():
    url = request.args.get('url')
    video_itag = request.args.get('video_itag')
    audio_itag = request.args.get('audio_itag')
    filename = request.args.get('filename', 'video.mp4')

    try:
        yt = YouTube(url)
        video_stream = yt.streams.get_by_itag(int(video_itag))
        audio_stream = yt.streams.get_by_itag(int(audio_itag))

        video_file = "video.mp4"
        audio_file = "audio.mp4"

        video_stream.download(filename=video_file)
        audio_stream.download(filename=audio_file)

        final_file = filename

        # Merge using ffmpeg
        os.system(f'ffmpeg -y -i "{video_file}" -i "{audio_file}" -c:v copy -c:a aac "{final_file}"')

        # Clean up temp files
        os.remove(video_file)
        os.remove(audio_file)

        return send_file(final_file, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
