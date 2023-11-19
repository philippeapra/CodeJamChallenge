import paho.mqtt.client as mqtt
import json
from Truck import *
from Load import *
from CustomEncoder import *
import sys
from  Notification import *

#from algo import sendNotification


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
day_started=False
notificationList = []
priceList = []

print(4)
# Callback when connecting to the broker
def on_connect(client, userdata, flags, rc):
    # with open("new_file.txt", "w") as file:
    #     z=0
    print("Connected with result code "+str(rc))
    client.subscribe("CodeJam")




# Callback when receiving a message
def on_message(client, userdata, msg):
    
    global day_started
    payload = msg.payload.decode("utf-8")
    event = json.loads(payload)
    event_type = event['type']
    global loads
    global trucks
    #sendNotification(Truck(),Load())
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
                # temp = trucks[event['truckId']]
                # if temp:
                #     truck.idleTime=trucks[event['truckId']].idleTime
                trucks[event['truckId']] = truck
                
                # for loadId, load in loads.items():
                #     if sendNotification(truck,load):
                #         notificationList.append(Notification(truck.truckId,load.loadId,truck.timestamp))


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
                priceList.append(int(event['price']))
                
                loads[event['loadId']] = load
                global numOfLoads
                numOfLoads+=1
                # for truckId, truck in trucks.items():
                #     if sendNotification(truck,load):
                #         notificationList.append(Notification(truck.truckId,load.loadId,load.timestamp))
                
        if event_type == 'End':
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
           loads={}
           trucks={}
           print("Day ended")
           if day_started:
               from algo import calculate_profit
               for truckId, truck in trucks.items():
                   for loadId, load in load.items():
                       calculate_profit(load,truck)
               print(sum(priceList)/len(priceList))
               sys.exit()

        elif event_type == 'Start':
           print("Day started")
           day_started=True
           numOfLoads=0
           numOfTrucks=0
           
        
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
    # with open("new_file.txt", "w") as file:
    #     #line = str(message_type)
        
    #     #print(json.dumps(trucks, indent=4))
    #     for truck in trucks:
    #         file.write(str(trucks)+"\n"+str(loads)+"\n")

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



