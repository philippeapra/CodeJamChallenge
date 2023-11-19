import paho.mqtt.client as mqtt
import json
from Truck import *
from Load import *
from CustomEncoder import *
import matplotlib.pyplot as plt

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
# Callback when connecting to the broker
def on_connect(client, userdata, flags, rc):
    # with open("new_file.txt", "w") as file:
    #     z=0
    print("Connected with result code "+str(rc))
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

    """ with open("new_file.txt", "w") as file:
         line = str(message_type)
        
         #print(json.dumps(trucks, indent=4))
         for truck in trucks:
             file.write(str(trucks)+"\n"+str(loads)+"\n")
  #  finally:
   #     return load_coord"""

# Create MQTT client and set username and password
client = mqtt.Client("ExceptionHandlers01")
client.username_pw_set(mqtt_user, password=mqtt_password)

# Assign callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(mqtt_broker, mqtt_port, 60)

client.loop_forever()

# Start the loop
#client.loop_forever()

def get_truckers():
    return trucks
