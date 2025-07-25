from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route("/api/info", methods=["POST"])
def get_info():
    url = request.json.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        ydl_opts = {"quiet": True, "skip_download": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video = []
            audio = []

            for fmt in info.get("formats", []):
                if fmt.get("vcodec") != "none" and fmt.get("acodec") == "none":
                    video.append({
                        "quality": fmt.get("format_note"),
                        "ext": fmt.get("ext"),
                        "url": fmt.get("url")
                    })
                elif fmt.get("acodec") != "none" and fmt.get("vcodec") == "none":
                    audio.append({
                        "quality": fmt.get("abr", "unknown"),
                        "ext": fmt.get("ext"),
                        "url": fmt.get("url")
                    })

            return jsonify({
                "title": info.get("title"),
                "video": video,
                "audio": audio
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
