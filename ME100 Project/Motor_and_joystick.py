from machine import DAC, ADC, Pin, PWM, Timer
from time import sleep

# Set pins A0 and A2 for DAC and ADC respectively
xcontrol = Pin(33, mode=Pin.IN)
ycontrol = Pin(32, mode=Pin.IN)
swcontrol = Pin(12, mode=Pin.IN, pull=Pin.PULL_UP)
"""Connecting GPIO pins A0 and A1 to the signal-in of the H-Bridge"""
motor_A1 = Pin(26, mode=Pin.OUT)
motor_A2 = Pin(25, mode=Pin.OUT)


# Assign DAC and ADC converter objects to each pin
adc_x = ADC(xcontrol)
adc_y = ADC(ycontrol)
# adc.val(0)
# ADC configs
adc_x.atten(ADC.ATTN_11DB)  # change range of converter to be V_ref = 3.2
adc_y.atten(ADC.ATTN_11DB)  # change range of converter to be V_ref = 3.2
adc_val = 0  # set val of ADC to dummy value to start off

#Convert duty cylce to speed
def duty_u16_forward(value):
    return int((1-value/65535) * (2**16-1))
def duty_u16_reverse(value):
    return int((value/65535) * (2**16-1))

#Set xIN1 and xIN2 both equal 1
motor_A1.value(1)
motor_A2.value(1)
value2 = 0
value1 = 1
# Print DAC and ADC values with a 100 ms delay
while True:
    adc_val_x = adc_x.read_u16()
    adc_val_y = adc_y.read_u16()
    speed = (adc_val_x/65535)* 100 #speed in percentage
    print("adc_val_x:",adc_val_x,"duty_cycle", speed)
    sw_val = swcontrol()
    
    #motor goes forward
    if value1 == 1:
        if speed<60 and speed >50:
            motor_A2.value(value1)
            L1 = PWM(motor_A2, freq=500, duty_u16=duty_u16_forward(0))
        elif speed>60:
            motor_A2.value(value1)
            L1 = PWM(motor_A2, freq=500, duty_u16=duty_u16_forward(adc_val_x))
        else:
            value1 = 0
            value2 = 1
    #motor goes reverse
    elif value2 == 1:
        if speed<60 and speed >50:
            motor_A1.value(value2)
            L1 = PWM(motor_A1, freq=500, duty_u16=duty_u16_forward(0))
        elif speed<50:
            L1 = PWM(motor_A1, freq=500, duty_u16=duty_u16_reverse(adc_val_x))
            motor_A2.value(value2)
        #motor_vpin.value(0)
        else:
            value1 = 1
            value2 = 0
            
    sleep(0.1)



