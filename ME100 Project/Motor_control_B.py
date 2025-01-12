import network
import espnow
from machine import DAC, ADC, Pin, PWM, Timer
from time import sleep

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()   # Because ESP8266 auto-connects to last Access Point

e = espnow.ESPNow()
e.active(True)

"""Connecting GPIO pins A0 and A1 to the signal-in of the H-Bridge"""
motor_A1 = Pin(26, mode=Pin.OUT)
motor_A2 = Pin(25, mode=Pin.OUT)
swcontrol = Pin(12, mode=Pin.IN, pull=Pin.PULL_UP)
motor_B1 = Pin(27, mode=Pin.OUT)
motor_B2 = Pin(4, mode=Pin.OUT)

#Convert duty cylce to speed_B
def duty_u16_reverse(value):
    return int((1.5-value/65535) * (2**16-1))
def duty_u16_forward(value):
    return int((0.5+value/65535) * (2**16-1))

#Set xIN1 and xIN2 both equal 1
motor_A1.value(1)
motor_A2.value(1)
motor_B1.value(1)
motor_B2.value(1)
value2 = 0
value1 = 1

while True:
    host, msg = e.recv()
    if msg:             # msg == None if timeout in recv()
        message = str(msg)
        values = message.split(',')
        
        adc_right_val = int(values[1])
        left_val = int(values[2])
        
        #print(f"right: {adc_right_val}, left: {left_val}")
        
#       print(int(str(msg)[5:-1]))
        if msg == b'end':
            break
        
    speed_B = (left_val/65535)* 100 #speed_B in percentage
    #print("adc_right_val:",adc_right_val,"duty_cycle", speed_B)
    print("left_val:",left_val,"duty_cycle", speed_B)
    sw_val = swcontrol()
    
    #motor goes forward
    if value1 == 1:
        if speed_B<60 and speed_B >40:
            motor_B1.value(value1)
            L2 = PWM(motor_B1, freq=500, duty_u16=2**16-1)
        elif speed_B>60:
            motor_B1.value(value1)
            L2 = PWM(motor_B1, freq=500, duty_u16=duty_u16_reverse(left_val))
        else:
            value1 = 0
            value2 = 1
    #motor goes reverse
    elif value2 == 1:
        if speed_B<60 and speed_B >40:
            motor_B2.value(value2)
            L2 = PWM(motor_B2, freq=500, duty_u16=2**16-1)
        elif speed_B<40:
            L2 = PWM(motor_B2, freq=500, duty_u16=duty_u16_forward(left_val))
            motor_B1.value(value2)
        #motor_vpin.value(0)
        else:
            value1 = 1
            value2 = 0
            
    sleep(0.1)









