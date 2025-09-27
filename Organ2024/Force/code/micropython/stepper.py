from machine import Pin, PWM
from time import sleep
from math import sin, asin, sqrt, pi

pwma = PWM(Pin(27), freq=500000, duty_u16=32768)  # vref for A
pwmb = PWM(Pin(29), freq=500000, duty_u16=32768)   #vref for B

pwma.duty_u16(5000)	#with .3 mOhm Sense Resistor, I = V/3
pwmb.duty_u16(5000)

A1_in = Pin(6, Pin.OUT)
A2_in = Pin(7, Pin.OUT)
B1_in = Pin(28, Pin.OUT)
B2_in = Pin(4, Pin.OUT)


def step(n):
    if n == 0:
        A1_in.on()
        A2_in.off()
        B1_in.on()
        B2_in.off()
    
    elif n == 1:
        A1_in.on()
        A2_in.off()
        B1_in.off()
        B2_in.on()
        
    elif n == 2:
        A1_in.off()
        A2_in.on()
        B1_in.off()
        B2_in.on()
        
    else:
        A1_in.off()
        A2_in.on()
        B1_in.on()
        B2_in.off()

def move(st, end):
    ct = st

    while not ct == end:
        step(ct % 4)
        sleep(0.005)
        if end > st:
            ct += 1
        else:
            ct -= 1  

#move(0,100)
        
