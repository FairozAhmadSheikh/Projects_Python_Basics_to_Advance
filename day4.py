import pyttsx3

def text_to_speech(text):
    """Convert text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Get user input
text = input("Enter text to convert to speech: ")
text_to_speech(text)
