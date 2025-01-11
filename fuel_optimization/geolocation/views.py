from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from geopy.distance import geodesic
from .models import FuelStation

def fetch_route():
    # Define hardcoded start and finish locations
    start = {"lat": 40.7128, "lon": -74.0060}  # Example: New York
    finish = {"lat": 34.0522, "lon": -118.2437}  # Example: Los Angeles
    # Simulate the route (replace with actual route logic if needed)
    route = [
        {"lat": 40.7128, "lon": -74.0060},
        {"lat": 39.9526, "lon": -75.1652},  # Example waypoint (Philadelphia)
        {"lat": 34.0522, "lon": -118.2437},
    ]
    return route

def get_cheapest_fuel_nearby(coords):
    stations = FuelStation.objects.all()
    closest_station = None
    min_distance = float('inf')
    min_price = float('inf')

    for station in stations:
        # Replace with real coordinates from database if available
        station_coords = (34.0522, -118.2437)  # Example coordinates
        distance = geodesic(coords, station_coords).miles

        if distance < min_distance or (distance == min_distance and station.retail_price < min_price):
            min_distance = distance
            min_price = station.retail_price
            closest_station = station

    if closest_station:
        return {
            "location": f"{closest_station.truckstop_name}, {closest_station.city}, {closest_station.state}",
            "price_per_gallon": closest_station.retail_price
        }
    return None

def fuel_route_api(request):
    route = fetch_route()
    stops = []
    total_cost = 0

    miles_left = 500  # Maximum range
    for i in range(len(route) - 1):
        start_coords = (route[i]["lat"], route[i]["lon"])
        fuel_stop = get_cheapest_fuel_nearby(start_coords)
        if fuel_stop:
            stops.append(fuel_stop)
            total_cost += fuel_stop["price_per_gallon"] * (miles_left / 10)

    return JsonResponse({
        "route": route,
        "stops": stops,
        "total_cost": round(total_cost, 2),
    })
