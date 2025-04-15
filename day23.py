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
def wish_user():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your assistant. How can I help you?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("🧠 Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
    except Exception as e:
        print("❌ Sorry, say that again...")
        return "None"
    return query.lower()

def run_jarvis():
    wish_user()
    while True:
        query = take_command()

        if "wikipedia" in query:
            import wikipedia
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif "open youtube" in query:
            webbrowser.open("https://youtube.com")

        elif "open google" in query:
            webbrowser.open("https://google.com")

        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif "open notepad" in query:
            os.system("notepad")

        elif "open calculator" in query:
            os.system("calc")

        elif "exit" in query or "stop" in query:
            speak("Goodbye!")
            break

        else:
            speak("I didn't understand. Please try again.")

if __name__ == "__main__":
    run_jarvis()