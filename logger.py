# # '''
# # UART communication on Raspberry Pi using Pyhton
import asyncio
import os
import serial
# from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
from datetime import datetime
import requests
import time

TEST_ID = 'dev-pi4'
AUTH_KEY = 'id8wn6mkJf86Svo10uiJI6iqXvebPi4US0OV9S8a'
URL = 'https://6a3blrx50f.execute-api.us-east-2.amazonaws.com/Production/ingest'

headers = {
    'Content-Type': 'application/json',
    'x-api-key': AUTH_KEY
}

async def producer(queue):
    
    print("Producer: Opening serial port")
    
    ser = serial.Serial("/dev/serial0", 57600)  # Open port with baud rate
    ser.reset_input_buffer()
    
    print("Producer: Running")

    batch = []

    BATCH_SIZE = 10

    while True:
        try:
            rx =  ser.readline()            # str(time.time() * 1000) + ",0,0,0,1394,2493,0,0,0,00.00.00" 
            s = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + "," + str(rx, encoding="utf-8")
            batch.append(s)
        except UnicodeDecodeError:
            print("Unicode error")

        if len(batch) >= BATCH_SIZE:
            await queue.put(batch)
            batch = []
            await asyncio.sleep(1)


# coroutine to consume work
async def consumer(queue):
    print("Consumer: Connecting to AWS")
    

    # mqttClient = AWSIoTMQTTClient("bruce-telemetry-pi")
    # mqttClient.enableMetricsCollection()
    # mqttClient.configureEndpoint("a134m7gripxuzz-ats.iot.us-east-2.amazonaws.com", 8883)
    # mqttClient.configureCredentials(
    #     "/home/bruce/AWSLogger/AmazonRootCA1.pem",
    #     "/home/bruce/AWSLogger/b4c01e4ca7d972a7ab4b9dc3f0d8456f788bc19901ca73474c7c085054b9bd63-private.pem.key",
    #     "/home/bruce/AWSLogger/b4c01e4ca7d972a7ab4b9dc3f0d8456f788bc19901ca73474c7c085054b9bd63-certificate.pem.crt"
    # )
    # mqttClient.configureOfflinePublishQueueing(-1) # infinite
    # mqttClient.configureDrainingFrequency(2) # 2 Hz
    # mqttClient.configureConnectDisconnectTimeout(10) # 10s
    # mqttClient.configureMQTTOperationTimeout(5) # 10s
    
    # while not mqttClient.connect():
    #     print("Failed to connect to AWS")
    #     asyncio.sleep(1)
        
    # print("Connected to AWS!")
    
    # consume work
    while True:
        item = await queue.get()
        # print(item)
        
        formatted = []
        
        for i in item:
            
            pieces = i.split(',')
            d = {
                "timestamp": {
                    "S": pieces[0]
                },
                "test_id": {
                    "S": TEST_ID
                },
                "throttle": {
                    "N": pieces[2]
                },
                "speed": {
                    "N": pieces[3]    
                },
                "rpm": {
                    "N": pieces[4]    
                },
                "current": {
                    "N": pieces[5]    
                },
                "voltage": {
                    "N": pieces[6]    
                },
                "throttleTooHigh": {
                    "N": pieces[7]    
                },
                "motorInitializing": {
                    "N": pieces[8]    
                },
                "clockState": {
                    "N": pieces[9]    
                },
                "lastDeadman": {
                    "S": pieces[10]
                }
            }
            
            # print(d)
            
            formatted.append(d)
                        
        # print(json.dumps(formatted))
        try:
            response = requests.post(URL, headers=headers, json={"messages": formatted})
            print("Uploaded to AWS with response", response.status_code)
        except:
            pass
            print("Failed to connect to AWS")    
        # Create message payload
            # mqttClient.publish("bruce/telemetry", i, 0)


# entry point coroutine
async def main():
    # create the shared queue
    queue = asyncio.Queue()
    # run the producer and consumers
    await asyncio.gather(producer(queue), consumer(queue))


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Exit application because user indicated they wish to exit.
        # This will have cancelled `main()` implicitly.
        print("User initiated exit. Exiting.")
