import yt_dlp

URLS = ['https://www.youtube.com/watch?v=wDgQdr8ZkTw']

ydl_opts = {
    'format': 'mp3/bestaudio/best',
    'outtmpl': '1fsadgbsa.%(ext)s',
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }]
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    error_code = ydl.download(URLS)
    print("done")