import pyttsx3

engine = pyttsx3.init()

# ensure engine initializes properly
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

def speak(text):
    """
    Speak safety alert aloud.
    """

    voices = engine.getProperty('voices')

    # select a working voice
    if voices:
        engine.setProperty('voice', voices[0].id)

    engine.say(text)
    engine.runAndWait()
