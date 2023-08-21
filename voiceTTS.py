import openai
import requests
import speech_recognition as sr
from elevenlabs import generate, play

openai.api_key = "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"
# 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

# Set your API key here
ELEVENLABS_API_KEY = "ce1843626b13073800e1c7739cce6fe9"

# Replace with your Rasa server URL
RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"

# Initialize the speech recognition object
recognizer = sr.Recognizer()

# elevenlabs implementation
# Function to generate speech from text and play it
def speak(audio_text, voice="Bella", model="eleven_monolingual_v1"):
    audio = generate(text=audio_text, voice=voice, model=model, api_key=ELEVENLABS_API_KEY)
    play(audio)


def make_response_humanlike(response_text):
    # Add pauses and intonations for natural speech
    response_text = " ".join(response_text.split())  # Remove extra spaces
    response_text = response_text + ","  # Add a comma for a natural pause
    return response_text


# Function to capture user input from the microphone
def takeCommand():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query
    except Exception as e:
        print(e)
        print("Unable to recognize your voice.")
        return None


# Function to send a POST request to Rasa server and process response
def process_response(message):
    response = requests.post(RASA_SERVER_URL, json={"sender": "user", "message": message})

    if response.status_code == 200:
        response_data = response.json()
        if response_data:
            response_message = response_data[0].get('text', 'No response text')
            return response_message
        else:
            return "Empty response from the server."
    else:
        return "Failed to get a valid response from the server."


# Main conversation loop
while True:
    user_query = takeCommand()

    if user_query:
        print('USER :', user_query)

        response_message = process_response(user_query)

        print("BOT :", response_message)
        speak(response_message)

    else:
        print("Waiting for user input...")




