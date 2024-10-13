import speech_recognition as sr
import pyttsx3
import requests
import webbrowser

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Replace with your actual API key

GEMINI_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=4)

        try:
            text = recognizer.recognize_google(audio)
            print(text)
            return text 
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None

def respond(text):
    engine.say(text)
    engine.runAndWait()

def call_gemini_api(prompt):
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }
    
    response = requests.post(GEMINI_URL, headers=headers, params={'key': API_KEY}, json=data)
    
    if response.status_code == 200:
        result = response.json()
        print(result)
        generated_text = result["candidates"][0]["content"]["parts"][0]["text"].replace("*","").replace("\n","")
        return generated_text
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def process_command(command):
    if command:
        command = command.lower()

        # Check for keywords to open specific websites
        if command.startswith("open google"):
            webbrowser.open("https://www.google.com")
            respond("Opening Google.")
        elif command.startswith("open youtube"):
            webbrowser.open("https://www.youtube.com")
            respond("Opening YouTube.")
        elif command.startswith("open facebook"):
            webbrowser.open("https://www.facebook.com")
            respond("Opening Facebook.")
        else:
            # Call the Gemini API for other commands
            response = call_gemini_api(command) 
            if response:
                respond(response)
            else:
                respond("Sorry, I didn't understand that. Please try again.")

def main():
    while True:
        command = listen()
        if command is None:
            continue  
        process_command(command)

if __name__ == "__main__":
    main()
