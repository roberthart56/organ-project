'''
general_combinations.py
Scans six combination buttons
Sends 'NoteOn' for each button. 'NoteOff' is not needed.  
'''


import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
#from adafruit_midi.note_off import NoteOff
import time
import board
import digitalio




midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

N = 6

button_objects = []		#list of configured objects for pedal switches.

button_pin_no = [board.GP10, board.GP11, board.GP12, board.GP13,
              board.GP14, board.GP15]


for pin in (button_pin_no):			
    but_obj = digitalio.DigitalInOut(pin)  
    but_obj.direction = digitalio.Direction.INPUT
    but_obj.pull = digitalio.Pull.UP
    button_objects.append(but_obj)			#this fills the list of objects, all input pullup.


while True:
    
    for i in range(N):		#scan each button pin
     
        if not button_objects[i].value:  #switch has closed
            midi.send(NoteOn(i, 127))
            #print(i,'on')
            time.sleep(0.5)
            
        
            
   
    