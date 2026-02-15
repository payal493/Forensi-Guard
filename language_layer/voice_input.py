import speech_recognition as sr

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone(device_index=1) as source:
        print("\n🎤 Speak now...")
        
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.energy_threshold = 300  # mic sensitivity
        recognizer.pause_threshold = 1     # pause before stopping

        print("Listening...")

        audio = recognizer.listen(source, phrase_time_limit=6)

    try:
        text = recognizer.recognize_google(audio, language="en-IN")
        print("\nYou said:", text)
        return text

    except sr.UnknownValueError:
        print("❌ Could not understand audio. Try again.")
        return None

    except sr.RequestError:
        print("❌ Network error. Check internet connection.")
        return None
