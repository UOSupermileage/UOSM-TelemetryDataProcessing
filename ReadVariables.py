
from mysecrets import DEVICE_ID
from mysecrets import SECRET_KEY
from arduino_iot_cloud import ArduinoCloudClient
import time
import datetime
import logging
import Telemetry as tem
#class TelemetryDataPoint:
#    timestamp: datetime
#    speed: float
#    current: float
#    voltage: float
#    rpm: int


def logging_func():

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    logging.basicConfig(
        datefmt="%H:%M:%S",
        format="%(asctime)s.%(msecs)03d %(message)s",
        level=logging.INFO,
    )

# This function is executed each time the "speed", "current", "voltage" or "rpm" variable changes

def rpm_switch_change(client,value):
    print(f"Value changed! {value}")
    client["ModifiedRPM"] = value * 2
    if (client["ModifiedSpeed"] != None and client["ModifiedCurrent"] != None and client["ModifiedVoltage"] != None and client["ModifiedRPM"] != None): 
        points.append(tem.TelemetryDataPoint(datetime.now(), client["ModifiedSpeed"], client["ModifiedCurrent"], client["ModifiedVoltage"], client["ModifiedRPM"]))
        i+=1 

def voltage_switch_change(client, value): 
    client["ModifiedVoltage"] = value
    if (client["ModifiedSpeed"] != None and client["ModifiedCurrent"] != None and client["ModifiedVoltage"] != None and client["ModifiedRPM"] != None): 
        points.append(tem.TelemetryDataPoint(datetime.now(), client["ModifiedSpeed"], client["ModifiedCurrent"], client["ModifiedVoltage"], client["ModifiedRPM"]))
        i+=1 


def amps_switch_change(client, value): 
    client["ModifiedCurrent"] = value
    if (client["ModifiedSpeed"] != None and client["ModifiedCurrent"] != None and client["ModifiedVoltage"] != None and client["ModifiedRPM"] != None): 
        points.append(tem.TelemetryDataPoint(datetime.now(), client["ModifiedSpeed"], client["ModifiedCurrent"], client["ModifiedVoltage"], client["ModifiedRPM"]))
        i+=1 

def speed_switch_change(client, value): 
    client["ModifiedSpeed"] = value
    if (client["ModifiedSpeed"] != None and client["ModifiedCurrent"] != None and client["ModifiedVoltage"] != None and client["ModifiedRPM"] != None): 
        points.append(tem.TelemetryDataPoint(datetime.now(), client["ModifiedSpeed"], client["ModifiedCurrent"], client["ModifiedVoltage"], client["ModifiedRPM"]))
        i+=1 


logging_func()

if __name__ == "__main__": 
    
    #TelemetryDataPoint node counter 
    i = 0
    points: list[tem.TelemetryDataPoint] = []
    #TODO: determine how many nodes we want to consider a single instance...
    
    #Create ArduinoCloudClient instance
    client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)

    #Register variables and corresponding edited variables
    client.register("randomm", value = None, on_write = rpm_switch_change)
    client.register("ModifiedRPM", value = None)

    client.register("Voltage", value = None, on_write = voltage_switch_change)
    client.register("ModifiedVoltage", value = None)
    
    client.register("ModifiedAmps", value = None)
    client.register("Current", value = None, on_write = amps_switch_change)
    
    client.register("ModifiedSpeed", value = None)
    client.register("Speed", value = None, on_write = speed_switch_change)

    client.start()

