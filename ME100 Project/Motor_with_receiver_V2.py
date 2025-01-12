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

#Convert duty cylce to speed
def duty_u16_reverse(value):
    return int((1.5-value/65535) * (2**16-1))
def duty_u16_forward(value):
    return int((0.5+value/65535) * (2**16-1))
Full_speed_B = int(0.5*2**16 - 1)
Half_speed_B = int(0.75*2**16 - 1)


#Set xIN1 and xIN2 both equal 1
motor_A1.value(1)
motor_A2.value(1)
motor_B1.value(1)
motor_B2.value(1)
value2_A = 0
value1_A = 1
value2_B = 0
value1_B = 1

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
        
    speed = (adc_right_val/65535)* 100 #speed in percentage
    speed_B = (left_val/65535)* 100
    print("adc_right_val:",adc_right_val,"duty_cycle", speed)
    print("left_val:",left_val,"duty_cycle", speed_B)
    sw_val = swcontrol()
    
    """For motor A"""
    #motor goes forward
    if value1_A == 1:
        if speed<60 and speed >40:
            motor_A2.value(value1_A)
            L1 = PWM(motor_A2, freq=500, duty_u16=65535)
        elif speed>60 and speed<90:
            motor_A2.value(value1_A)
            L1 = PWM(motor_A2, freq=500, duty_u16=Half_speed_B)
        elif speed>90:
            motor_A2.value(value1_A)
            L1 = PWM(motor_A2, freq=500, duty_u16=Full_speed_B)
        else:
            value1_A = 0
            value2_A = 1
    #motor goes reverse
    elif value2_A == 1:
        if speed<60 and speed >40:
            motor_A1.value(value2_A)
            L1 = PWM(motor_A1, freq=500, duty_u16=2**16-1)
            
        elif speed<40 and speed>2:
            L1 = PWM(motor_A1, freq=500, duty_u16=Half_speed_B)
            motor_A2.value(value2_A)
        elif speed<2:
            L1 = PWM(motor_A1, freq=500, duty_u16=Full_speed_B)
            motor_A2.value(value2_A)
        else:
            value1_A = 1
            value2_A = 0
            
    """For Motor B"""
    #motor goes forward
    if value1_B == 1:
        if speed_B<55 and speed_B >40:
            motor_B1.value(value1_B)
            L2 = PWM(motor_B1, freq=500, duty_u16=2**16-1)
        elif speed_B>55 and speed_B <90:
            motor_B1.value(value1_B)
            L2 = PWM(motor_B1, freq=500, duty_u16=Half_speed_B)
        elif speed_B>90:
            motor_B1.value(value1_B)
            L2 = PWM(motor_B1, freq=500, duty_u16=Full_speed_B)
            #print(duty_u16_reverse(left_val))
        else:
            value1_B = 0
            value2_B = 1
    #motor goes reverse
    elif value2_B == 1:
        if speed_B<55 and speed_B >40:
            motor_B2.value(value2_B)
            L2 = PWM(motor_B2, freq=500, duty_u16=2**16-1)
        elif speed_B>2 and speed_B<40:
            L2 = PWM(motor_B2, freq=500, duty_u16=Half_speed_B)
            motor_B1.value(value2_B)
        elif speed_B<2:
            L2 = PWM(motor_B2, freq=500, duty_u16=Full_speed_B)
            motor_B1.value(value2_B)
            #print(duty_u16_forward(left_val))
            #print(Full_speed_B)
        else:
            value1_B = 1
            value2_B = 0
    sleep(0.1)









