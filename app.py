from flask import Flask, redirect, render_template, request, url_for
from threading import Thread
import paho.mqtt.client as mqtt
import numpy as np
import sys
#from connection import *
import json
from Truck import *
from Load import *
from CustomEncoder import *
from Notification import *
app = Flask(__name__)
preference_weights = [1,1,1]#,1]
matched_loads = {}
ThresholdValue = 0
avg_profit = 260.96
avg_dh = 256.23
min_profit = 1.11
max_profit = 988.55
min_dh = 5.79
max_dh = 959.1

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
client = None
day_started=True
notificationList = []
profitList = []
nmsgs=0
deadheadList=[]
api_key = "b2f6e2bb-de44-46e4-bcc8-5faf77b3a76e"
trucks_nfs = {}
# Callback when connecting to the broker
def on_connect(client, userdata, flags, rc):
 
    client.subscribe("CodeJam")

# Callback when receiving a message
def on_message(client, userdata, msg):
    global trucks
    global loads
    global nmsgs
    nmsgs+=1
    if(nmsgs==200):
        """    for truckId, truck in trucks.items():
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
        """
        #id =  notificationList[0].truckId
        """       for nf in notificationList:
            if nf.truckId in trucks_nfs:
                trucks_nfs[nf.truckId].append(nf)
            else:
                trucks_nfs[nf.truckId] = [nf]
       """
        print(trucks_nfs)
        sys.exit()
    global day_started
    payload = msg.payload.decode("utf-8")
    event = json.loads(payload)
    event_type = event['type']

    try:
        if day_started:
            if event_type == 'Truck':
                #print(msg.topic+" "+str(msg.payload))
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
                for loadId, load in loads.items():
                    if sendNotification(truck,load):
                        nf = Notification(truck.truckId,load.loadId,truck.timestamp,get_score(truck,load,api_key))
                        notificationList.append(nf)
                        print(f"Sent to {truck.truckId}")
                        if nf.truckId in trucks_nfs:
                            trucks_nfs[nf.truckId].append(nf)
                        else:
                            trucks_nfs[nf.truckId] = [nf]
                
                
     

            elif event_type == 'Load':
                #print(msg.topic+" "+str(msg.payload))
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

                for truckId, truck in trucks.items():
                    if sendNotification(truck,load):
                        nf = Notification(truck.truckId,load.loadId,load.timestamp,get_score(truck,load,api_key))
                        notificationList.append(nf)
                        print(f"Sent to {truck.truckId}")
                        if nf.truckId in trucks_nfs:
                            trucks_nfs[nf.truckId].append(nf)
                        else:
                            trucks_nfs[nf.truckId] = [nf]
             
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
# Define your MQTT client setup and callback functions
def handle_mqtt():
    # Set up MQTT client and callbacks
    global client
    client = mqtt.Client("ExceptionHandlers01")
    client.username_pw_set(mqtt_user, password=mqtt_password)
    client.on_connect = on_connect
    client.on_message = on_message
    #client.username_pw_set(mqtt_user, password=mqtt_password)
    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_start()  # Starts network loop in a separate thread


def notify_trucker(truck, load):
    print(f"Notify trucker {truck.truckId} about load {load.loadId}")

import math



import datetime
def compare_and_return_latest(datetime_str1, datetime_str2):
    # Parse the datetime strings into datetime objects
    datetime1 = datetime.fromisoformat(datetime_str1)
    datetime2 = datetime.fromisoformat(datetime_str2)
    
    # Compare the datetime objects
    if datetime1 > datetime2:
        return datetime_str1
    else:
        return datetime_str2

def match_loads_to_truck(api_key, loads, truck):
    notifications =[]
    for load in loads:
        if sendNotification(truck,load):
            t1 = truck.timestamp()
            t2 = load.timestamp()
            t1 = compare_and_return_latest(t1,t2)
           
            notifications.append(Notification(truck.truckId,load.loadId,t1))
      
                
    return notifications
def get_dh(truck,load):
    return haversine_distance(truck.position[0],truck.position[1],load.origin[0],load.origin[1])/1.60934

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
def sendNotification(truck, load):
    
    if load.equipmentType != truck.equipType:
        return False
    profit = calculate_profit(load,truck,api_key)
    if profit <=0:
        return False
    score = get_score(truck,load,api_key)
    #"Score is {score}")
    if score>np.sum(preference_weights) * 1/3:
        return True
    return False
    #     return True
    #return False

def match_loads_to_truck(api_key, loads, truck):
    notifications =[]
    return notifications

def get_score(truck,load,api_key):#,c1,c2,c3,c4):
    profit_n = normalize_profit(calculate_profit(load,truck,api_key))
    dh_n =  normalize_dh(get_dh(truck,load))
    tl_n = get_tripLength_preferenceNumber_score(truck,load)
    #it_n = normalize_it()
   # preference_weights = [c1,c2,c3,c4]
    score = [profit_n,-dh_n,tl_n]#,it_n]
    print( np.dot(score,preference_weights))
    return np.dot(score,preference_weights)


def normalize_profit(p):
    profit_n = p-min_profit
    profit_n /= max_profit-min_profit

    #profit_n = p-np.mean(get_profits())
    #profit_n /=np.std(get_profits())
    return profit_n


def normalize_dh(p):
    
    profit_n = p-min_dh
    profit_n /=max_dh-min_dh
    return profit_n


#def normalize_tl(p):
 #   profit_n = p-np.mean(get_trip_lengths())
 #   profit_n /=np.std(get_trip_lengths())
 #   return profit_n


#def normalize_it(p):
 #   profit_n = p-np.mean(get_idle_times())
  #  profit_n /=np.std(get_idle_times())
 #   return profit_n
def get_tripLength_preferenceNumber_score(truck,load):
    if load.mileage > 600:
        return -2
    elif (truck.tripLengthPreference == "Long" and load.mileage >= 200):
        return 1 - (200/load.mileage)
    elif (truck.tripLengthPreference == "Long" and load.mileage < 200):
        return -(1-(load.mileage / 200))
    elif (truck.tripLengthPreference == "Short" and load.mileage >= 200):
        return -(1-(200 / load.mileage))
    elif (truck.tripLengthPreference == "Short" and load.mileage < 200):
        return 1-(load.mileage/200)
    elif load.mileage > 600:
        return -2
    
def calculate_profit(load, truck, api_key):
    deadhead_distance=haversine_distance(truck.position[0],truck.position[1],load.origin[0],load.origin[1])/1.60934
    #_, deadhead_distance = get_route(truck.position[0], truck.position[1], load.origin[0], load.origin[1], api_key)
    total_distance = deadhead_distance + load.mileage
    fuel_cost = 1.38 * total_distance
    profit = load.price - fuel_cost
    return profit
def get_trucker(truck_id):
    # Example logic: return None if truck_id is invalid
    print(trucks)
    try:
        truck_id_int = int(truck_id)
    except:
        truck_id_int = -1
        print("not a number")
        pass

    if truck_id_int in trucks:  # Replace with your validation logic
        print("here")
        return truck_id_int  # Replace with actual trucker data
    else:
        return None

@app.route('/')
def index():
    return render_template('page.html') 

@app.route('/submit_truck_id', methods=['POST'])
def submit_truck_id():
    truck_id = request.form.get('truckId')
    trucker_info = get_trucker(truck_id)
   
    if trucker_info is None:
        # Truck ID is invalid
        return render_template('page.html', error="Invalid Truck ID")
    else:
         global current_truck
         current_truck = trucks.get(trucker_info)
        # Truck ID is valid, redirect to dashboard
         return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    
    latitude = float(current_truck.position[0])
    longitude = float(current_truck.position[1]) 
    if current_truck.truckId not in trucks_nfs:
        return render_template('page.html',error='No Notifications yet')
    sorted_nf = sorted(trucks_nfs[current_truck.truckId], key=lambda x: x.score)
    if(len(sorted_nf)>0):
        latitude2 =   loads[sorted_nf[-1].loadId].origin[0]
        dh1 = get_dh(trucks[sorted_nf[-1].truckId],loads[sorted_nf[-1].loadId])
        
        longitude2 = loads[sorted_nf[-1].loadId].origin[1]
        em1 = (dh1+loads[sorted_nf[-1].loadId].mileage) * 161.8 * 21
        l1 = loads[sorted_nf[-1].loadId].mileage
        p1 = calculate_profit(loads[sorted_nf[-1].loadId],trucks[sorted_nf[-1].truckId],api_key)
        t1 = (l1+dh1) * (1/65)

        if len(sorted_nf)>1:

            latitude3 =loads[sorted_nf[-2].loadId].origin[0]
            longitude3=loads[sorted_nf[-2].loadId].origin[1]

            dh2 = get_dh(trucks[sorted_nf[-2].truckId],loads[sorted_nf[-2].loadId])

            em2 = (dh1+loads[sorted_nf[-2].loadId].mileage) * 161.8 * 21

            l2 = loads[sorted_nf[-2].loadId].mileage

            p2 = calculate_profit(loads[sorted_nf[-2].loadId],trucks[sorted_nf[-2].truckId],api_key)

            t2 = (l2+dh2) * (1/65)

            data_rows = [
                {'rank': 1, 'profit': p1, 'emission': em1, 'length': l1, 'time': t1},
                {'rank': 2, 'profit': p2, 'emission': em2, 'length': l2, 'time': t2}
            
            ]
        else:
            data_rows = [
                {'rank': 1, 'profit': p1, 'emission': em1, 'length': l1, 'time': t1},
            ]

        longitude3=0
        latitude3=0
        return render_template('dashboard.html', latitude=latitude, longitude=longitude,latitude2=latitude2,latitude3 = latitude3,longitude2=longitude2,longitude3=longitude3,data_rows = data_rows)
    latitude2,latitude3,longitude3,longitude2=0

    return render_template('dashboard.html',latitude = latitude, latitude2=latitude2,latitude3=latitude3)

    #return render_template('dashboard.html')

@app.route('/rank_categories', methods=['POST'])
def rank_categories():
    # Get the user's ranking choices from the form
    maximize_profitability = request.form.get('maximize_profitability')
    meet_length_preference = request.form.get('meet_length_preference')
    minimize_deadhead_time = request.form.get('minimize_deadhead_time')
    minimize_idle_time = request.form.get('minimize_idle_time')
    global preference_weights
    print(maximize_profitability)
    
    if(maximize_profitability=='low'):
        preference_weights[0]-=0.05
    if(meet_length_preference=='low'):
        preference_weights[1]-=0.05
    if(minimize_deadhead_time=='low'):
        preference_weights[2]-=0.05
    if(maximize_profitability=='high'):
        preference_weights[0]+=0.05
    if(meet_length_preference=='high'):
        preference_weights[1]+=0.05
    if(minimize_deadhead_time=='high'):
        preference_weights[2]+=0.05
    #preference_weights
    # You can process and store these rankings as needed
    # For example, you can store them in a database


    # Redirect to the dashboard or any other page
    return redirect(url_for('dashboard'))
if __name__ == '__main__':
    # Start the MQTT client on a separate thread
    print("Starting thread")
    mqtt_thread = Thread(target=handle_mqtt)
    mqtt_thread.start()

    # Start the Flask application

    app.run(debug=True)

    # Once app.run() completes, it's time to clean up and stop the MQTT client
    client.loop_stop()
    client.disconnect()
