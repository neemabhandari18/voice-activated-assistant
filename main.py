import speech_recognition as sr      # Speech-to-text
import pyttsx3                       # Text-to-speech
import datetime                      # Time & date utilities
import wikipedia                     # Wikipedia summaries
import webbrowser                    # Open URLs
import os                            # Run system commands

# ── 1. INITIALIZE SPEECH ENGINES ─────────────────────────────────────────────
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# ── 2. speak() ───────────────────────────────────────────────────────────────
def speak(text: str) -> None:
    """Convert text to speech and also print to console."""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# ── 3. listen() ──────────────────────────────────────────────────────────────
def listen() -> str:
    """Listen from mic and convert to lowercase string."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
    except sr.RequestError:
        speak("Internet error. Please check your connection.")
    return ""

# ── 4. greet_user() ──────────────────────────────────────────────────────────
def greet_user():
    """Greet user based on time of day."""
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("How can I assist you today?")

# ── 5. run_assistant() ───────────────────────────────────────────────────────
def run_assistant() -> None:
    greet_user()

    while True:
        command = listen()

        # Time
        if "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {current_time}")

        # Date
        elif "date" in command:
            current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
            speak(f"Today is {current_date}")

        # Wikipedia
        elif "wikipedia" in command:
            topic = command.replace("wikipedia", "").strip()
            if topic:
                speak(f"Searching Wikipedia for {topic}")
                try:
                    result = wikipedia.summary(topic, sentences=2)
                    speak(result)
                except wikipedia.exceptions.DisambiguationError:
                    speak("Too many results. Please be more specific.")
                except wikipedia.exceptions.PageError:
                    speak("Sorry, I couldn't find anything.")
            else:
                speak("What should I search on Wikipedia?")

        # Google Search
        elif "search" in command:
            query = command.replace("search", "").strip()
            if query:
                url = f"https://www.google.com/search?q={query}"
                speak(f"Searching Google for {query}")
                webbrowser.open(url)
            else:
                speak("What should I search for?")

        # Open Google
        elif "open google" in command:
            speak("Opening Google...")
            webbrowser.open("https://www.google.com")

        # Open YouTube
        elif "open youtube" in command:
            speak("Opening YouTube...")
            webbrowser.open("https://www.youtube.com")

        # Open Notepad (Windows only)
        elif "open notepad" in command:
            speak("Opening Notepad...")
            os.system("notepad.exe")

        # Open Calculator (Windows)
        elif "open calculator" in command:
            speak("Opening Calculator...")
            os.system("calc.exe")

        # Exit
        elif "exit" in command or "quit" in command:
            speak("Goodbye!")
            break

        # Unknown Command
        elif command:
            speak("Sorry, I don't understand that command.")

# ── 6. MAIN ENTRY ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_assistant()
