#!/usr/bin/env python3
from comm.redis import set_redis
from utility.dataclass import Reading
from api.blueprints import utils as api_tools

import plugins.Freenove_DHT as DHT
import RPi.GPIO as GPIO

import time

DHTPin = 11


class Monitor:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
                
    def monitor_temp_hum(self):
        self.dht = DHT.DHT(DHTPin)

        start_time = time.time()
        while True:
            for i in range(0, 15):
                chk = self.dht.readDHT11()
                if chk is self.dht.DHTLIB_OK:
                    break
                time.sleep(0.1)

            reading = Reading(temp=self.dht.temperature, hum=self.dht.humidity)
            set_redis("reading", reading)

            # Save readings every 5 seconds
            end_time = time.time()
            delta = end_time - start_time
            if delta >= 5:
                try:
                    resp = api_tools.add_reading(temp=reading.temp, hum=reading.hum)
                except Exception:
                    pass
                start_time = time.time()
            
    def destroy(self):
        GPIO.cleanup()
