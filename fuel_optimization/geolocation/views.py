from django.http import JsonResponse
import json
from django.conf import settings
from django.shortcuts import render
import openrouteservice
import requests

# Fetch the route data from OpenRouteService API
def fetch_route_from_ors(start, finish):
    client = openrouteservice.Client(key=settings.OPENROUTESERVICE_API_KEY)
    coords = [start, finish]
    route = client.directions(
        coordinates=coords,
        profile='driving-car',
        format='geojson'
    )
    return route

# Function to generate fuel stops (this is just mock data; replace with actual data)
def get_fuel_stops():
    return [
        {"name": "Fuel Stop 1", "price": 3.50, "coordinates": [-74.030, 40.730]},
        {"name": "Fuel Stop 2", "price": 3.80, "coordinates": [-118.250, 34.070]},
    ]

# Map view function
def map_view(request):
    start_coords = [-74.0060, 40.7128]  # Example start (New York)
    end_coords = [-118.25703, 34.05513]  # Example end (Los Angeles)
    ors_api_key = settings.OPENROUTESERVICE_API_KEY

    # Get route data from OpenRouteService
    route_data = fetch_route_from_ors(start_coords, end_coords)

    # Get fuel stops data
    fuel_stops = get_fuel_stops()

    # Pass the data to the template
    context = {
        'start_coords': json.dumps(start_coords),  # Serialize Python list to JSON
        'end_coords': json.dumps(end_coords),
        'route_geometry': json.dumps(route_data['features'][0]['geometry']['coordinates']),
        'fuel_stops': json.dumps(fuel_stops),
    }

    return render(request, 'map.html', context)
# from django.http import JsonResponse
# from django.conf import settings
# from django.shortcuts import render
# import json
# import openrouteservice
# import requests

# # Function to get latitude and longitude from place name using OpenRouteService API
# def get_coordinates_from_place(place_name):
#     client = openrouteservice.Client(key=settings.OPENROUTESERVICE_API_KEY)  # ORS API key
#     geocode_result = client.pelias_search(place_name)  # ORS geocoding search
#     if geocode_result['features']:
#         lat = geocode_result['features'][0]['geometry']['coordinates'][1]  # Latitude
#         lon = geocode_result['features'][0]['geometry']['coordinates'][0]  # Longitude
#         return [lon, lat]  # [lon, lat] format for ORS
#     else:
#         return None

# # Fetch the route data from OpenRouteService API using the provided endpoint format
# def fetch_route_from_ors(start, finish):
#     api_key = settings.OPENROUTESERVICE_API_KEY  # ORS API key
#     url = f'https://api.openrouteservice.org/v2/directions/driving-car'
#     params = {
#         'api_key': api_key,
#         'start': f'{start[0]},{start[1]}',  # Longitude, Latitude format
#         'end': f'{finish[0]},{finish[1]}',  # Longitude, Latitude format
#     }
#     response = requests.get(url, params=params)

#     if response.status_code == 200:
#         route_data = response.json()
#         return route_data
#     else:
#         return None

# # Map view where users can input place names
# def map_view(request):
#     start_place = request.GET.get('start_place', 'New York')  # Default value
#     end_place = request.GET.get('end_place', 'Los Angeles')  # Default value

#     # Get coordinates for the places entered by the user
#     start_coords = get_coordinates_from_place(start_place)
#     end_coords = get_coordinates_from_place(end_place)

#     if start_coords and end_coords:
#         route_data = fetch_route_from_ors(start_coords, end_coords)
#         print(route_data)  # Check if it's JSON or HTML

#         if route_data:
#             context = {
#                 'start_coords': json.dumps(start_coords),  # Ensure it's valid JSON
#                 'end_coords': json.dumps(end_coords),      # Ensure it's valid JSON
#                 'start_place': start_place,
#                 'end_place': end_place,
#                 'route_geometry': json.dumps(route_data['features'][0]['geometry']['coordinates']),
#             }
#         else:
#             context = {
#                 'error': 'Could not fetch route data from OpenRouteService.',
#                 'start_place': start_place,
#                 'end_place': end_place,
#             }
#     else:
#         context = {
#             'error': 'Could not find coordinates for one or both of the places.',
#             'start_place': start_place,
#             'end_place': end_place,
#         }

#     return render(request, 'map.html', context)
