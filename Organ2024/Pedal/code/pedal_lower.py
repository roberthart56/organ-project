'''
pedal_lower.py
Circuit python code to check lowest 10 notes, send message
via UART to RP Pico when a pedal note changes.
Byte sent is integer 0-9, with the fifth bit a flag signifying 'on'

'''


import board
import busio
import time
import digitalio


# Initialize UART with default TX pin and no RX pin
uart = busio.UART(tx=board.GP0, rx=None, baudrate=460800)

N = 10
ped_objects = []		#list of configured objects for pedal switches.
ped_pin_no = [board.A0, board.A1, board.A2, 
         board.A3, board.GP6, board.GP7, board.GP1,
           board.GP2, board.GP4, board.GP3]


for pin in (ped_pin_no):			#set up rows
    pin_obj = digitalio.DigitalInOut(pin)  
    pin_obj.direction = digitalio.Direction.INPUT
    pin_obj.pull = digitalio.Pull.UP
    ped_objects.append(pin_obj)			#this fills the list of objects, all input pullup.

ped_state_old  = [True] * N		#list of ped note states	
ped_state_new = [True] * N	#initialize list for scanned pins.

while True:
#for _ in range(1):
    
    for i in range(N):		#scan each pedal note pin
        ped_state_new[i] = ped_objects[i].value
    
        if ped_state_old[i] and not ped_state_new[i]:  #switch has closed
            print(i, 'on')
            msg = bytes([i | 1 << 4])   #send the index plus an 'on' flag.
            uart.write(msg)
            
        elif not ped_state_old[i] and ped_state_new[i]:	#switch has opened
            print(i, 'off')
            msg = bytes([i])   #send the index with no flag.
            uart.write(msg)

    # Create a copy of ped_state_new for the next iteration
    ped_state_old = ped_state_new[:]
#     print(ped_state_new[6])
#     time.sleep(1)


