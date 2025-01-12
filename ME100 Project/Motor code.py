from machine import Pin, PWM, Timer
from time import sleep

""" You may need to change pinouts from your board depending on what you use """

encoder_count = 0

def counter(__):
    global encoder_count
    encoder_count = encoder_count + 1
    
def calculate_speed(timer):
    global encoder_count
    global number_of_degrees_per_encoder_tick
    delta_t = 1
    speed = encoder_count*number_of_degrees_per_encoder_tick/delta_t
    print('CPS is', encoder_count)
    print('Speed is', speed, 'deg/s')
    
    # Reset the counter for the next speed
    encoder_count = 0
    
def duty_u16(value):
    return int(value/100 * (2**16-1))

"""Connecting GPIO pins A0 and A1 to the signal-in of the H-Bridge"""
motor_vpin = Pin(26, mode=Pin.OUT)
motor_gnd = Pin(25, mode=Pin.OUT)

""" percent Full power motor (sometimes does not run below 33%"""

L1 = PWM(motor_gnd, freq=500, duty_u16=32767)
    #motor_gnd.value(A_value)
    #L1 = PWM(motor_vpin,freq=1000,duty_u16=duty_u16(speed_as_percent))
    
    
"""See how many times the encoder is getting triggered"""
encoder_0 = Pin(34, mode=Pin.IN)
encoder_0.irq( handler=counter, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)

"""Find the average speed"""
t1 = Timer(1)
t1.init(period=1000, mode=t1.PERIODIC, callback=calculate_speed)
number_of_degrees_per_encoder_tick = 4




