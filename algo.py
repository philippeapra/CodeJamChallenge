import heapq
import json
import requests
import paho.mqtt.client as mqtt
from Truck import *
from Load import *
from travel_time import *
from connection import *
from Notification import *




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

# def getProfitNumberScore(load, truck, api_key):
#     profit = calculate_profit(load, truck, api_key)
#     if (profit < 50):
#         return 1
#     elif (profit < 100):
#         return 2
#     elif (profit < 150):
#         return 3
#     elif (profit < 200):
#         return 4
#     elif (profit < 250):
#         return 5
#     elif (profit < 300):
#         return 6
#     elif (profit)
        

#def calculate_score(load,  truck, api_key):
 #   score = get_tripLength_preferenceNumber_score() * truck.trip_length_preference_weightage + getProfitNumberScore() * truck.profit_weightage \
  #  + get_deadhead_time(load, truck, api_key) * truck.deadhead_time_weightage + truck.idleTime 


# def checkThresholdValue(load, truck, api_key, ThresholdValue):
#     if calculate_score(load, truck, api_key) > ThresholdValue :
#         return True
#     return False

def sendNotification(truck, load):
     
    if load.equipmentType != truck.equipType:
        return False
    profit = calculate_profit(load,truck,api_key)
    if profit <=0:
        return False
    # if checkThresholdValue :
    #     return True
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