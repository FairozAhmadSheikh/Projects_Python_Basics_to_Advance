# pip install speechrecognition pyttsx3 pyaudio
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change to [0] for male voice

def speak(text):
    engine.say(text)
    engine.runAndWait()
