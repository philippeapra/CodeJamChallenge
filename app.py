from flask import Flask, redirect, render_template, request, url_for
from threading import Thread
import paho.mqtt.client as mqtt
#from connection import *
import json
from Truck import *
from Load import *
from CustomEncoder import *
app = Flask(__name__)
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
day = 1
client = None

# Callback when connecting to the broker
def on_connect(client, userdata, flags, rc):
    # with open("new_file.txt", "w") as file:
    #     z=0
    #print("Connected with result code "+str(rc))
    client.subscribe("CodeJam")

# Callback when receiving a message
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    payload = msg.payload.decode("utf-8")
    try:
        event = json.loads(payload)
        event_type = event['type']
        if event_type == 'Truck':
            truck = Truck(
                event['truckId'],
                event['positionLatitude'],
                event['positionLongitude'],
                event['equipType'],
                event['nextTripLengthPreference']
            )
            global numOfTrucks
            numOfTrucks+=1
            trucks[event['truckId']] = truck

        elif event_type == 'Load':
            load = Load(
                event['loadId'],
                event['originLatitude'],
                event['originLongitude'],
                event['destinationLatitude'],
                event['destinationLongitude'],
                event['equipmentType'],
                event['price'],
                event['mileage']
            )
            loads[event['loadId']] = load
            global numOfLoads
            numOfLoads+=1
            
        elif event_type == 'End':
           print("numOfLoads: "+str(numOfLoads))
           print("numOfTrucks: " + str(numOfTrucks))
           print("numOfUniqueLoads: "+str(len(loads)))
           print("numOfUniqueTrucks: "+str(len(trucks)))
           global day
           day_coord = [] 
           global load_coord
           #load_coord=[]
           for key, value in loads.items():
               day_coord.append(value.origin)
           numOfLoads=0
           numOfTrucks=0
           day +=1
           
           load_coord.append(day_coord)
           print("Day ended")

        elif event_type == 'Start':
           print("Day started")
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
    latitude2 =40.19
    latitude3 =41.02
    longitude2 = -88.58
    longitude3= -84.82
    return render_template('dashboard.html', latitude=latitude, longitude=longitude,latitude2=latitude2,latitude3 = latitude3,longitude2=longitude2,longitude3=longitude3)

    #return render_template('dashboard.html')

@app.route('/rank_categories', methods=['POST'])
def rank_categories():
    # Get the user's ranking choices from the form
    maximize_profitability = request.form.get('maximize_profitability')
    meet_length_preference = request.form.get('meet_length_preference')
    minimize_deadhead_time = request.form.get('minimize_deadhead_time')
    minimize_idle_time = request.form.get('minimize_idle_time')
    
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
