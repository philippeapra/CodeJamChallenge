import heapq
import json
import requests
import paho.mqtt.client as mqtt
from Truck import *
from Load import *
from travel_time import *
from connection import *

def notify_trucker(truck, load):
    print(f"Notify trucker {truck.truckId} about load {load.loadId}")



def get_deadhead_time(truck, load, api_key):
    deadhead_time, _ = get_route(truck.position[0], truck.position[1], load.origin[0], load.origin[1], api_key)
    return deadhead_time

def calculate_profit(load, truck, api_key):
    _, deadhead_distance = get_route(truck.position[0], truck.position[1], load.origin[0], load.origin[1], api_key)
    total_distance = deadhead_distance + load.mileage
    fuel_cost = 1.38 * total_distance
    profit = load.price - fuel_cost
    return profit


def match_loads_to_trucks(api_key):
    matched_loads = {}
    for truck_id, truck in trucks.items():
        load_heap = []
        for load_id, load in loads.items():
            # Ensure truck type matches load type
            if load.equipmentType != truck.equipType:
                continue  

            # Calculate profit and deadhead
            profit = calculate_profit(load, truck, api_key)
            deadhead_time = get_deadhead_time(truck, load, api_key)

            # Check trip length preference
            trip_length_match = (load.mileage < 200 and truck.tripLengthPreference == "Short") or \
                                (load.mileage >= 200 and truck.tripLengthPreference == "Long")


            # Calculate score (adjust the weights and logic as needed)
            score = profit - deadhead_time - idle_time
            if trip_length_match:
                score += 100  # Arbitrary bonus for matching trip length preference

            heapq.heappush(load_heap, (-score, load))

        if load_heap:
            best_load = heapq.heappop(load_heap)[1]
            matched_loads[truck_id] = best_load.loadId
            notify_trucker(truck, best_load)

    return matched_loads
