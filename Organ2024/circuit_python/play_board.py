
#play_board.py
#demonstration of using RP2040 to send MIDI signals for virtual organ.
#October, 2025.
#Potentiometer, button, other inputs?  


import board
import time
import digitalio
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

LED = digitalio.DigitalInOut(board.GP28)  
LED.direction = digitalio.Direction.OUTPUT

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)



button = digitalio.DigitalInOut(board.GP0)  
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

    

    
note = [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47,
        48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
        60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71,
        72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83,
        84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95,
        96]


while True:

    while button.value:
        pass
                    

    for i in range(40,50):
        
        print(note[i], 'on')
        midi.send(NoteOn(note[i], 127))

        time.sleep(0.2)

        print(note[i], 'off')
        midi.send(NoteOff(note[i], 127))
        
        time.sleep(0.2)
           
      
#main


