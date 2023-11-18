import heapq
import json
import requests
import paho.mqtt.client as mqtt
from Truck import *
from Load import *
from travel_time import *
from connection import *
from Notification import *


deadhead_time_weightage= 1
trip_length_preference_weightage = 1
profit_weightage= 1
idleTimeWeightage= 1
matched_loads = {}
ThresholdValue = 0


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

def get_tripLength_preferenceNumber_score(truck,load):
    if (truck.tripLengthPreference == "Long" and load.mileage >= 200):
        return load.mileage / 200
    elif (truck.tripLengthPreference == "Long" and load.mileage < 200):
        return ((load.mileage / 200)-0.5)
    elif (truck.tripLengthPreference == "Short" and load.mileage >= 200):
        return ((200 / load.mileage)-0.5)
    elif (truck.tripLengthPreference == "Short" and load.mileage < 200):
        return 200 / load.mileage
    

def calculate_score(load, truck, api_key):
    score = get_tripLength_preferenceNumber_score() * trip_length_preference_weightage + calculate_profit() * profit_weightage \
    + get_deadhead_time(load, truck, api_key) * deadhead_time_weightage + truck.idleTime 


def checkThresholdValue(load, truck, api_key, ThresholdValue):
    if calculate_score(load, truck, api_key) > ThresholdValue :
        truck.idleTime = 0
        return True
    truck.idleTime = truck.idleTime + 1
    return False

def sendNotification():
    if checkThresholdValue :
        return True
    return False

def match_loads_to_truck(api_key, loads, truck):
    notifications =[]




    # for truck_id, truck in trucks.items():
    #     load_heap = []
    #     for load_id, load in loads.items():
    #         # Ensure truck type matches load type
    #         if load.equipmentType != truck.equipType:
    #             continue  

    #         # Calculate profit and deadhead
    #         profit = calculate_profit(load, truck, api_key)
    #         deadhead_time = get_deadhead_time(truck, load, api_key)

    #         # Check trip length preference
    #         trip_length_match = (load.mileage < 200 and truck.tripLengthPreference == "Short") or \
    #                             (load.mileage >= 200 and truck.tripLengthPreference == "Long")

    #         # Calculate score (adjust the weights and logic as needed)
    #         score = profit - deadhead_time - idle_time



    #         heapq.heappush(load_heap, (-score, load))

    #     if load_heap:
    #         best_load = heapq.heappop(load_heap)[1]
    #         matched_loads[truck_id] = best_load.loadId
    #         notify_trucker(truck, best_load)

    return notifications
