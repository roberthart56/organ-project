
#scan_matrix_play_61 notes
#columns are attached to outputs, raised high,
#rows scanned with pulldown input.


import board
import time
import digitalio
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

LED = digitalio.DigitalInOut(board.GP28)  #pin_obj is an internal variable
LED.direction = digitalio.Direction.OUTPUT

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)



button1 = digitalio.DigitalInOut(board.GP0)  
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.UP

button2 = digitalio.DigitalInOut(board.GP11)  
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.UP

button3 = digitalio.DigitalInOut(board.GP12)  
button3.direction = digitalio.Direction.INPUT
button3.pull = digitalio.Pull.UP

    

    
note = [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47,
        48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
        60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71,
        72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83,
        84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95,
        96]


while True:

    
    if not button1.value:
        
        for i in range(40,50):
            
            #print(note[i], 'on')
            midi.send(NoteOn(note[i], 127))

            time.sleep(0.2)

            #print(note[i], 'off')
            midi.send(NoteOff(note[i], 127))
            
            time.sleep(0.2)
           
    if not button2.value:
        i=0
        #print(note[i], 'on')
        midi.send(NoteOn(note[i], 127))

        time.sleep(0.2)

        #print(note[i], 'off')
        midi.send(NoteOff(note[i], 127))
        
        time.sleep(0.2)
        
    if not button3.value:
        i=60
        #print(note[i], 'on')
        midi.send(NoteOn(note[i], 127))

        time.sleep(0.2)

        #print(note[i], 'off')
        midi.send(NoteOff(note[i], 127))
        
        time.sleep(0.2)
    
    
          
#main


