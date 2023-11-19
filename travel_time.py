import requests
api_key= "b2f6e2bb-de44-46e4-bcc8-5faf77b3a76e"
def get_route_time(start_lat, start_lng, end_lat, end_lng, api_key):
    url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [f"{start_lat},{start_lng}", f"{end_lat},{end_lng}"],
        "vehicle": "car",  # or truck, depending on your needs
        "key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()
    travel_time_ms = data['paths'][0]['time'] if 'paths' in data and len(data['paths']) > 0 else None
    if travel_time_ms is not None:
        travel_time_min = travel_time_ms/1000/60
        return travel_time_min
    else:
        return None

def get_route(start_lat, start_lng, end_lat, end_lng, api_key):
    url = "https://graphhopper.com/api/1/route"
    params = {
        "point": [f"{start_lat},{start_lng}", f"{end_lat},{end_lng}"],
        "vehicle": "car",  # or truck, depending on your needs
        "key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()
    total_distance_meters = data["paths"][0]["distance"]
    total_time_ms = data["paths"][0]["time"]

    # Convert distance to miles (1 mile = 1609.34 meters)
    total_distance_miles = total_distance_meters / 1609.34

    # Convert time to minutes
    total_time_minutes = total_time_ms / 1000 / 60

    return (total_time_minutes, total_distance_miles)