import requests
from elevenlabs import generate, play
import openai

openai.api_key = "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"
# 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

# Set your API key here
API_KEY_ELBS = "ce1843626b13073800e1c7739cce6fe9"

# Replace with your Rasa server URL
RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"


# elevenlabs implementation
def speak(audio_text, voice="Bella", model="eleven_monolingual_v1"):
    audio = generate(text=audio_text, voice=voice, model=model, api_key=API_KEY_ELBS)
    play(audio)


def make_response_humanlike(response_text):
    # Add pauses and intonations for natural speech
    response_text = " ".join(response_text.split())  # Remove extra spaces
    response_text = response_text + ","  # Add a comma for a natural pause
    return response_text


# ............................................................................

f = open("Hello.mp3", "rb")

transcript = openai.Audio.transcribe("whisper-1", f)
print(transcript['text'])

# ............................................................................

# Prepare message for POST request
# message = 'text'

# Send POST request
response = requests.post(RASA_SERVER_URL, json={"sender": "duck", "message": transcript['text']})

# Play the response message received from the server
if response.status_code == 200:
    response_data = response.json()
    response_message = response_data[0]['text']  # Assuming the server response contains a 'text' field
    speak(response_message)

    # Enhance the response for natural speech
    enhanced_response = make_response_humanlike(response_message)

    speak(enhanced_response)

    print("Bot : ", response_message)
    print("Bot2 : ", enhanced_response)

else:
    print("Failed to get a valid response from the server.")
