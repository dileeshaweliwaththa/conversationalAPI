import requests

GELOCATION_API_KEY = 'AIzaSyBM_L32LJNZu0nU_emJQ4D391HPBSoc5hM'
PLACES_API_KEY = 'AIzaSyBM_L32LJNZu0nU_emJQ4D391HPBSoc5hM'
DISTANCE_API_KEY = 'AIzaSyBM_L32LJNZu0nU_emJQ4D391HPBSoc5hM'  # Add your Distance Matrix API Key here

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
