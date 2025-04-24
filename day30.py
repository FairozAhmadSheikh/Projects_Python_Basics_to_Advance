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

def run_assistant():
    talk("Hello Mohammed! I'm your Python Assistant. How can I help you today?")
    while True:
        command = take_command()

        if 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk(f"Current time is {time}")

        elif 'wikipedia' in command:
            talk("Searching Wikipedia...")
            topic = command.replace('wikipedia', '')
            info = wikipedia.summary(topic, sentences=2)
            talk(info)

        elif 'play' in command:
            song = command.replace('play', '')
            talk(f"Playing {song}")
            pywhatkit.playonyt(song)

        elif 'open notepad' in command:
            os.system("notepad")

        elif 'joke' in command:
            talk(pyjokes.get_joke())

        elif 'stop' in command or 'exit' in command:
            talk("Goodbye! See you later.")
            break

        elif command == "none":
            talk("I didn’t catch that. Please repeat.")

        else:
            talk("Sorry, I don't understand. Try saying something else.")
if __name__ == "__main__":
    run_assistant()