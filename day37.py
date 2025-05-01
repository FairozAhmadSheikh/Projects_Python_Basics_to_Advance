# pip install pytube openai-whisper transformers torch
# # Ubuntu/Debian
# sudo apt install ffmpeg

## Windows (via Chocolatey)
# choco install ffmpeg
import whisper
from pytube import YouTube
from transformers import pipeline
import os

# Download YouTube video
def download_video(url, output_path='downloads'):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    out_file = stream.download(output_path=output_path)
    print(f"🎧 Downloaded: {out_file}")
    return out_file