from ruuvitag_sensor.ruuvitag import RuuviTag
from ruuvitag_sensor.ruuvi import RuuviTagSensor

import RestfulClient as restclient
import json
import time
import serial


#RUUVITAG config data
#sensor MAC address
sensor = 'E1:93:D4:77:5F:57'
timeout_in_sec = 4
ruuvitagmemory = {'data_format': 0, 'humidity': 0, 'temperature': 0, 'pressure': 0, 'acceleration': 0, 'acceleration_x': 0, 'acceleration_y': 0, 'acceleration_z': 0, 'tx_power': 0, 'battery': 0, 'movement_counter': 0, 'measurement_sequence_number': 0, 'mac': 'e193d4775f57'}

#Light/Temp sensor config data
#Command to read light amount
readlight = [60, 1, 62]
#Command to read temperature
readtemp = [60, 2, 62]
arrlight = bytearray(readlight)
arrtemp = bytearray(readtemp)
lightmemory = 0


def ruuvitagsensor():
    #Read data from RuuviTAG sensor
    macs = [sensor]
    global ruuvitagmemory
    
    try:
        datas = RuuviTagSensor.get_data_for_sensors(macs, timeout_in_sec)
        print(datas)
        if datas == {} :
            print("RuuviTag read failed")
            restclient.ruuvitagsend(ruuvitagmemory, False);
        else:
            state= datas[sensor]
            # send temperature and humidity
            print("RuuviTag read passed")     
            restclient.ruuvitagsend(state, True);
            ruuvitagmemory = state
    
    except:
        print("something happened with RuuviTAG")
        restclient.ruuvitagsend(ruuvitagmemory, False);


def light_temp_sensor():
    #Read fata from light/temp sensor
    global lightmemory
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, bytesize=8, parity='N', stopbits=1, timeout = 3)
        ser.open
      
        writelight = ser.write(arrlight)   
        lightanswer = ser.readline()
        
        if lightanswer == b'':
            print("Light Read Failed")
            read_ok = False
            lightstring = lightmemory
        else:
            read_ok = True
            lightstring = lightanswer.decode()
            lightmemory = lightstring
            print("light " + lightstring)
        
        restclient.templightsend(lightstring, read_ok);
        
        ser.close()
    except:
        print("something happened, USB dongle not connected?")
        restclient.templightsend(0, False);


while True:
    ruuvitagsensor() 
    light_temp_sensor()
    time.sleep(5)

