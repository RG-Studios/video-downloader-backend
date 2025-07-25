from pytube import YouTube

def get_streams(url):
    yt = YouTube(url)
    video_streams = yt.streams.filter(progressive=True, file_extension='mp4')
    return {
        "title": yt.title,
        "streams": [
            {"itag": stream.itag, "resolution": stream.resolution}
            for stream in video_streams
        ]
    }

def download_video(url, itag, name):
    yt = YouTube(url)
    stream = yt.streams.get_by_itag(itag)
    path = stream.download(filename=name)
    return path
