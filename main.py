#!/usr/bin/env python3
from modules.reminder import Reminder
from modules.monitor import Monitor
from modules.buzzer import Buzzer
from modules.display import LCD
from modules.lights import Lights

from comm.redis import get_redis
from datetime import datetime, time
from multiprocessing import Process


class HabitatMonitor:
    def __init__(self):
        self.lcd = LCD()
        self.reminder = Reminder()
        self.reminder.start_reminder()

    def display(self):
        deg_symbol = chr(223)

        while True:
            reading = get_redis("reading")
            line_1 = f"Temp: {reading.temp} {deg_symbol}C" + "\n"
            line_2 = f"Humidity: {reading.hum}% RH"
            self.lcd.display((line_1, line_2))

            if self.reminder.food_reminder is not None:
                self.reminder.show_reminder("FEED THE SNAKE!!", "food")
            elif self.reminder.water_reminder is not None:
                self.reminder.show_reminder("WATER THE SNAKE!!", "water")

    def destroy(self):
        self.lcd.destroy()

def run():
    print('Program is starting ... ')

    monitor = Monitor()
    monitor_process = Process(target=monitor.monitor_temp_hum)
    monitor_process.start()

    lights = Lights()
    lights.start_lights()

    habitat = HabitatMonitor()
    try:
        habitat.display()
    except KeyboardInterrupt:
        monitor_process.terminate()
        monitor.destroy()

        lights.destroy()
        
        habitat.destroy()


if __name__ == '__main__':
    run()
    

