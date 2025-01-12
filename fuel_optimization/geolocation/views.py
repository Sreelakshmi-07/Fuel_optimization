from django.http import JsonResponse
import json
from geopy.geocoders import Nominatim
from django.conf import settings
from django.shortcuts import render
import openrouteservice
import requests
import csv
import os 
import logging

# Configure logging
logger = logging.getLogger(__name__)

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

def get_coordinates_from_name(name):
    # Initialize geolocator (using Nominatim from OpenStreetMap)
    geolocator = Nominatim(user_agent="fuel_stop_locator")

    # Geocode the name of the fuel stop
    location = geolocator.geocode(name)
    print(location,"76767")

    
    if location:
        return [location.longitude, location.latitude]  # Return [longitude, latitude]
    else:
        return None  # Return None if no coordinates found

def get_fuel_stops():
    fuel_stops = []
    try:
        with open('fuel-prices-for-be-assessment.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Get coordinates based on truckstop name
                name = row['Truckstop Name']
                coordinates = get_coordinates_from_name(name)

                if coordinates:
                    fuel_stops.append({
                        'truckstop_name': row['Truckstop Name'],
                        'address': row['Address'],
                        'city': row['City'],
                        'state': row['State'],
                        'retail_price': float(row['Retail Price']),
                        'coordinates': coordinates  # Add coordinates to the list
                    })
                    print(fuel_stops)
                else:
                    print(f"Could not geocode {name}")  # Handle the case where coordinates couldn't be found
    except FileNotFoundError:
        # Handle error if the file does not exist
        return None

    return fuel_stops

# Map view function
from django.shortcuts import render
from geopy.geocoders import Nominatim
import json
import logging

# Configure logging
logger = logging.getLogger(__name__)

def map_view(request):
    # Get start and end places from the user input
    start_place = request.GET.get('start_place', 'New York')  # Default to New York if not provided
    end_place = request.GET.get('end_place', 'Los Angeles')  # Default to Los Angeles if not provided
    
    geolocator = Nominatim(user_agent="route_map")
    
    # Geocode start and end places
    start_location = geolocator.geocode(start_place)
    end_location = geolocator.geocode(end_place)
    
    if start_location and end_location:
        start_coords = [start_location.longitude, start_location.latitude]
        end_coords = [end_location.longitude, end_location.latitude]
    else:
        # Log error if geocoding fails
        logger.error(f"Geocoding failed for start place: {start_place}, end place: {end_place}")
        
        # Set default coordinates for the USA center if geocoding fails
        start_coords = end_coords = [-98.583333, 39.8283]  # USA center coordinates
        
        # Optionally, you could add a message to pass to the template to notify the user
        error_message = "Unable to geocode one or both locations. Showing default USA coordinates."

    # Get route data from OpenRouteService
    ors_api_key = settings.OPENROUTESERVICE_API_KEY
    route_data = fetch_route_from_ors(start_coords, end_coords)

    # Get fuel stops data (assuming you have a function for that)
    fuel_stops = get_fuel_stops()

    context = {
        'start_coords': json.dumps(start_coords),
        'end_coords': json.dumps(end_coords),
        'route_geometry': json.dumps(route_data['features'][0]['geometry']['coordinates']),
        'fuel_stops': json.dumps(fuel_stops),
        'start_place': start_place,
        'end_place': end_place,
        'error_message': error_message if 'error_message' in locals() else None,  # Pass the error message if it exists
    }

    return render(request, 'map.html', context)
