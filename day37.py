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

# Transcribe audio using Whisper
def transcribe_audio(file_path):
    model = whisper.load_model("base")
    print("🔊 Transcribing audio...")
    result = model.transcribe(file_path)
    return result['text']

# Summarize transcript
def summarize_text(text):
    print("🧠 Summarizing text...")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    summary = ""
    for chunk in chunks:
        result = summarizer(chunk, max_length=150, min_length=40, do_sample=False)
        summary += result[0]['summary_text'] + " "
    return summary.strip()