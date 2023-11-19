import paho.mqtt.client as mqtt
import json
from Truck import *
from Load import *
from CustomEncoder import *
import sys
from  Notification import *
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
# Connection parameters
mqtt_broker = "fortuitous-welder.cloudmqtt.com"
mqtt_port = 1883
mqtt_user = "CodeJamUser"
mqtt_password = "123CodeJam"
trucks = {}
loads = {}
numOfTrucks=0
numOfLoads=0
load_coord=[]
day_started=True
notificationList = []
profitList = []
nmsgs=0
deadheadList=[]


def notify_trucker(truck, load):
    print(f"Notify trucker {truck.truckId} about load {load.loadId}")

import math

def haversine_distance(lat1, lon1, lat2, lon2):
    
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Radius of the Earth in kilometers (mean value)
    earth_radius = 6371.0  # km

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = earth_radius * c

    return distance
def calculate_profit(load, truck, api_key):
    deadhead_distance=haversine_distance(truck.position[0],truck.position[1],load.origin[0],load.origin[1])/1.60934
    #_, deadhead_distance = get_route(truck.position[0], truck.position[1], load.origin[0], load.origin[1], api_key)
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



def sendNotification(truck, load):
     
    if load.equipmentType != truck.equipType:
        return False
    profit = calculate_profit(load,truck,api_key)
    if profit <=0:
        return False

    return False

def match_loads_to_truck(api_key, loads, truck):
    notifications =[]

    return notifications



# Callback when connecting to the broker
def on_connect(client, userdata, flags, rc):
    # with open("new_file.txt", "w") as file:
    #     z=0
    print("Connected with result code "+str(rc))
    client.subscribe("CodeJam")




# Callback when receiving a message
def on_message(client, userdata, msg):
    global trucks
    global loads
    global nmsgs
    nmsgs+=1
    if(nmsgs==1500):
        for truckId, truck in trucks.items():
            for loadId, load in loads.items():
                deadhead_distance=haversine_distance(truck.position[0],truck.position[1],load.origin[0],load.origin[1])/1.60934
                profit=calculate_profit(load,truck,api_key)
                if profit>0 and truck.equipType==load.equipmentType :
                    deadheadList.append(deadhead_distance)
                    profitList.append(profit)
                    
        print(profitList,deadheadList)
        print("average profit :"+ str(sum(profitList)/len(profitList)))
        print("average deadhead :"+ str(sum(deadheadList)/len(deadheadList)))
        print("min profit"+str(min(profitList)),"max profit:"+str(max(profitList)))
        print("min deadhead"+str(min(deadheadList)),"max deadhead:"+str(max(deadheadList)))
        sys.exit()
    global day_started
    payload = msg.payload.decode("utf-8")
    event = json.loads(payload)
    event_type = event['type']

    try:
        if day_started:
            if event_type == 'Truck':
                print(msg.topic+" "+str(msg.payload))
                truck = Truck(
                    event['truckId'],
                    event['positionLatitude'],
                    event['positionLongitude'],
                    event['equipType'],
                    event['nextTripLengthPreference'],
                    event['timestamp']
                )
                global numOfTrucks
                numOfTrucks+=1

                trucks[event['truckId']] = truck
                
     

            elif event_type == 'Load':
                print(msg.topic+" "+str(msg.payload))
                load = Load(
                    event['loadId'],
                    event['originLatitude'],
                    event['originLongitude'],
                    event['destinationLatitude'],
                    event['destinationLongitude'],
                    event['equipmentType'],
                    event['price'],
                    event['mileage'],
                    event['timestamp']
                )
                
                
                loads[event['loadId']] = load
                global numOfLoads
                numOfLoads+=1
             
        if event_type == 'End':
      
           loads={}
           trucks={}
           print("numOfLoads: "+str(numOfLoads))
           print("numOfTrucks: " + str(numOfTrucks))
           print("numOfUniqueLoads: "+str(len(loads)))
           print("numOfUniqueTrucks: "+str(len(trucks)))
           
           global load_coord
           load_coord=[]
           for key, value in loads.items():
               load_coord.append(value.origin)
           numOfLoads=0
           numOfTrucks=0
           
           print("Day ended")
               
               

        elif event_type == 'Start':
           print("Day started")
           day_started=True
           numOfLoads=0
           numOfTrucks=0
           
        
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")

# Create MQTT client and set username and password
client = mqtt.Client("ExceptionHandlers02")
client.username_pw_set(mqtt_user, password=mqtt_password)

# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(mqtt_broker, mqtt_port, 60)

# Start the loop
client.loop_forever()