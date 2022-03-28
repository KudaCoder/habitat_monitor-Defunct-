from comm.redis import get_redis

import RPi.GPIO as GPIO

from datetime import datetime
import threading
import time

NIGHT_LIGHT_PIN = 29
WINTER_MONTHS = [1, 2, 3, 10, 11, 12]
SUMMER_MONTHS = [4, 5, 6, 7, 8, 9]


class Lights:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(NIGHT_LIGHT_PIN, GPIO.OUT)
            
    def night_light_on(self):
        GPIO.output(NIGHT_LIGHT_PIN, GPIO.LOW)
    
    def night_light_off(self):
        GPIO.output(NIGHT_LIGHT_PIN, GPIO.HIGH)
    
    def control(self):
        return_to_cool = False

        c_time = time.time()
        first = False
        while True:
            c_end_time = time.time()
            delta = c_end_time - c_time
            if delta >= 5 or not first:
                config = get_redis("environment")            
                c_time = time.time()
                first = True
            reading = get_redis("reading")
            temp = reading.temp

            now = datetime.now()
            month = int(now.strftime("%-m"))
            n_time = now.time()
            
            heat_on = False
            # if month in WINTER_MONTHS:
            # Night time
            if (config.lights_off_time < n_time) or (n_time < config.lights_on_time):
                if temp > config.night_h_sp:
                    return_to_cool = True
                elif (config.night_l_sp <= temp <= config.night_h_sp) and not return_to_cool:
                    heat_on = True
                elif temp < config.night_l_sp:
                    heat_on = True
                    return_to_cool = False
            # Day time
            elif config.lights_on_time <= n_time <= config.lights_off_time:
                if temp > config.day_h_sp:
                    return_to_cool = True
                elif (config.day_l_sp <= temp <= config.day_h_sp) and not return_to_cool:
                    heat_on = True
                elif temp < config.day_l_sp:
                    heat_on = True
                    return_to_cool = False

            if heat_on:
                self.night_light_on()
            else:
                self.night_light_off()
            
    def destroy(self):
        GPIO.cleanup()
    
    def start_lights(self):
        thread = threading.Thread(target=self.control, daemon=True)
        thread.start()

