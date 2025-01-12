from rcwl1601 import RCWL1601
from machine import Pin,I2C
from time import sleep

sensor = RCWL1601(trigger_pin=14, echo_pin=22,echo_timeout_us=1000000) # Change Pins

try:
  while True:
    distance = sensor.distance_cm()
    print(distance)
except KeyboardInterrupt:
        pass
