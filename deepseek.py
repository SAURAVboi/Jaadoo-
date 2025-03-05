import subprocess
import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import urllib.parse
import time

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Configuration (Customize these)
CONTACTS = {
    "john": "+1234567890",
    "emma": "+0987654321",
    "mom": "+1122334455"
}

APP_PATHS = {
    "calculator": "calc.exe",  # Windows
    "notepad": "notepad.exe",
    "photoshop": r"C:\Program Files\Adobe\Photoshop\photoshop.exe",
    # Add Mac/Linux paths as needed
}

def listen_to_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            print(f"You: {text}")
            return text.lower()
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand.")
            return None
        except sr.RequestError:
            print("Speech Recognition service is down.")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

def run_deepseek(prompt):
    process = subprocess.Popen(
        ["ollama", "run", "deepseek-r1:1.5b"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True
    )
    response, _ = process.communicate(input=prompt)
    return response.strip()

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def open_website(url):
    webbrowser.open(url)
    speak_text(f"Opening {url.split('//')[-1].split('/')[0]}")

def open_application(app_name):
    if app_name in APP_PATHS:
        try:
            os.startfile(APP_PATHS[app_name])
            speak_text(f"Opening {app_name}")
        except Exception as e:
            speak_text(f"Failed to open {app_name}")
    else:
        speak_text(f"Application {app_name} not configured")

def send_whatsapp_message(contact_name):
    if contact_name in CONTACTS:
        speak_text("What message would you like to send?")
        message = listen_to_speech()
        if message:
            encoded_message = urllib.parse.quote(message)
            url = f"https://web.whatsapp.com/send?phone={CONTACTS[contact_name]}&text={encoded_message}"
            open_website(url)
            time.sleep(2)  # Wait for WhatsApp Web to load
            speak_text(f"Message ready to send to {contact_name}. Press enter to send.")
    else:
        speak_text(f"Contact {contact_name} not found in contacts")

def handle_command(command):
    # Basic commands
    if "open google" in command:
        open_website("https://google.com")
    
    elif "open file" in command:
        file_name = command.split("open file")[-1].strip()
        file_path = os.path.join(os.getcwd(), file_name)
        if os.path.exists(file_path):
            os.startfile(file_path)
            speak_text(f"Opening {file_name}")
        else:
            speak_text("File not found")
    
    elif "play music" in command:
        song_name = command.split("play music")[-1].strip()
        open_website(f"https://www.youtube.com/results?search_query={urllib.parse.quote(song_name)}")
    
    # Advanced commands
    elif "send whatsapp message to" in command:
        contact = command.split("send whatsapp message to")[-1].strip()
        send_whatsapp_message(contact)
    
    elif "open application" in command:
        app_name = command.split("open application")[-1].strip()
        open_application(app_name)
    
    elif "search for" in command:
        query = command.split("search for")[-1].strip()
        open_website(f"https://google.com/search?q={urllib.parse.quote(query)}")
    
    elif any(word in command for word in ["exit", "quit", "stop"]):
        speak_text("Goodbye!")
        exit()
    
    else:
        # Fallback to AI
        response = run_deepseek(command)
        print(f"AI: {response}")
        speak_text(response)

if __name__ == "__main__":
    speak_text("Jarvis activated. How can I assist you today?")
    while True:
        user_input = listen_to_speech()
        if user_input:
            handle_command(user_input)