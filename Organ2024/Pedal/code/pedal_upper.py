import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
import time
import board
import busio
import digitalio


uart = busio.UART(tx=None, rx=board.GP13, baudrate=460800, timeout=0.1)

print("UART initialized for receive only.")

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

N = 22
ped_objects = []		#list of configured objects for pedal switches.
ped_pin_no = [board.GP0, board.GP1, board.GP2, board.GP3,
              board.GP4, board.GP5, board.GP6, board.GP7,
              board.GP8, board.GP9, board.GP10, board.GP11,
              board.GP12, board.GP14, board.GP15, board.GP16,
              board.GP17, board.GP18, board.GP19, board.GP20,
              board.GP21, board.GP22]


for pin in (ped_pin_no):			
    pin_obj = digitalio.DigitalInOut(pin)  
    pin_obj.direction = digitalio.Direction.INPUT
    pin_obj.pull = digitalio.Pull.UP
    ped_objects.append(pin_obj)			#this fills the list of objects, all input pullup.

ped_state_old  = [True] * N		#list of ped note states	
ped_state_new = [True] * N	#initialize list for scanned pins.

while True:
    
    for i in range(N):		#scan each pedal note pin
        ped_state_new[i] = ped_objects[i].value
    
        if ped_state_old[i] and not ped_state_new[i]:  #switch has closed
            midi.send(NoteOn(i+11, 127))
            print(i+11, 'on')
            
        elif not ped_state_old[i] and ped_state_new[i]:	#switch has opened
            midi.send(NoteOff(i+11, 127))
            print(i+11, 'off')
            
    ped_state_old = ped_state_new[:]
    
    if uart.in_waiting > 0:
        data = uart.read(1)  # Read a byte.
        integer_value = int.from_bytes(data, 'big')
        note = (integer_value & 0b1111)   #strip off the integer
        if integer_value & 0b00010000:	#check the flag.
            midi.send(NoteOn(note+1, 127))
            print(note+1, 'on')
        else:
            midi.send(NoteOff(note + 1))
            print (note+1, 'off')
    #else:
        #print("No data received.")
        
    #midi.send(NoteOn(36, 127))
    #print(36)
    #time.sleep(.5)