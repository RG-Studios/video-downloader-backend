from flask import Flask, request, jsonify, send_file
from downloader import get_streams, download_video
import os

app = Flask(__name__)

@app.route("/api/info", methods=["GET"])
def get_video_info():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400
    streams = get_streams(url)
    return jsonify(streams)

@app.route("/api/download", methods=["GET"])
def download():
    url = request.args.get("url")
    quality = request.args.get("quality")
    name = request.args.get("name") or "video.mp4"

    filepath = download_video(url, quality, name)
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    from os import environ
    port = int(environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
