# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
import requests


class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # Get user message from Rasa tracker
        user_message = tracker.latest_message.get('text')
        print(user_message)

        # def get_chatgpt_response(self, message):
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {
            'Authorization': 'Bearer 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',
            'Content-Type': 'application/json'
        }
        data = {
            'model': "gpt-3.5-turbo",
            'messages': [
                {'role': 'system', 'content': 'You are an AI assistant for the user. You help to solve user query'},
                {'role': 'user', 'content': 'You: ' + user_message}
                ],
            'max_tokens': 100
        }
        response = requests.post(url, headers=headers, json=data)
        # response = requests.post(api_url, headers=headers, json=data)

        # Print the API response
        print(response.text)

        if response.status_code == 200:
            chatgpt_response = response.json()
            message = chatgpt_response['choices'][0]['message']['content']
            dispatcher.utter_message(message)
        else:
            # Handle error
            return "Sorry, I couldn't generate a response at the moment. Please try again later."

            # Revert user message which led to fallback.
        return [UserUtteranceReverted()]


class ActionRestaurantNearMe(Action):
    def name(self) -> Text:
        return "action_restaurant_near_me"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        GELOCATION_API_KEY = 'AIzaSyBM_L32LJNZu0nU_emJQ4D391HPBSoc5hM'
        PLACES_API_KEY = 'AIzaSyBM_L32LJNZu0nU_emJQ4D391HPBSoc5hM'
        DISTANCE_API_KEY = 'AIzaSyBM_L32LJNZu0nU_emJQ4D391HPBSoc5hM'


        # Step 1: Get User's Location using Geolocation API
        geolocation_url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={GELOCATION_API_KEY}'
        geolocation_response = requests.post(geolocation_url)
        geolocation_data = geolocation_response.json()

        geo_location = geolocation_data['location']

        print(f"Latitude: {geo_location['lat']}, Longitude: {geo_location['lng']}")

        # Step 2: Use User's Location for Places API Nearby Search
        radius = 1000  # 2km in meters
        places_url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={PLACES_API_KEY}&location={geo_location["lat"]},{geo_location["lng"]}&radius={radius}&type=restaurant'
        places_data = requests.get(places_url).json()

        results = []

        # Step 3: Fetch rating and distance to each place using Distance Matrix API
        printed_restaurants = 0
        for place in places_data['results']:
            place_location = place['geometry']['location']
            distance_api_url = f'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={geo_location["lat"]},{geo_location["lng"]}&destinations={place_location["lat"]},{place_location["lng"]}&key={DISTANCE_API_KEY}'
            distance_data = requests.get(distance_api_url).json()
            distance = distance_data['rows'][0]['elements'][0]['distance']['text']
            duration = distance_data['rows'][0]['elements'][0]['duration']['text']
            rating = place.get('rating', 'No ratings')  # Get rating if exists, else default to 'No ratings'

            if rating != 'No ratings':
                print(f"Restaurant: {place['name']}, Rating: {rating}, Distance: {distance}, Duration: {duration}")
                printed_restaurants += 1

            if printed_restaurants == 5:  # Print only the top 5 restaurants
                break

            results.append(f"Restaurant: {place['name']}, Rating: {rating}, Distance: {distance}, Duration: {duration}")

        # Send the information back to the user
        # You can adjust the code to send something different or additional information
        dispatcher.utter_message(
            text=r"Here are Top 5 restaurants nearby:" + "\n" + "\n".join(results[:5]))

