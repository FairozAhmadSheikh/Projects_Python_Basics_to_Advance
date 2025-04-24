# pip install pyttsx3 speechrecognition wikipedia pywhatkit pyjokes datetime
# pip install pyaudio

import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import pywhatkit
import pyjokes
import os

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice

def talk(text):
    print("🗣️ Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def take_command():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        audio = listener.listen(source)
        try:
            command = listener.recognize_google(audio)
            print("🧑‍💻 You:", command)
        except sr.UnknownValueError:
            return "None"
    return command.lower()