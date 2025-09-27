import time
import board
import analogio
import usb_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.midi_message import MIDIMessage
from adafruit_midi import MIDI

# MIDI setup
midi0 = MIDI(midi_out=usb_midi.ports[1], out_channel=0)  # MIDI channel 1 (0-based)
midi1 = MIDI(midi_out=usb_midi.ports[1], out_channel=0)  # MIDI channel 1 (0-based)

# Analog input setup
potentiometer0 = analogio.AnalogIn(board.A0)  # Adjust to the correct pin
potentiometer1 = analogio.AnalogIn(board.A1)
#potentiometer2 = analogio.AnalogIn(board.A2)

# Calibration values
MIDI_MIN = 0    # MIDI CC range min
MIDI_MAX = 127  # MIDI CC range max
ADC_MIN = 0     # Adjust based on testing
ADC_MAX = 65535 # Max ADC value for RP2040

# Expression pedal settings
CC_NUMBER_0 = 11  # MIDI Expression pedal CC (Hauptwerk uses CC 11 for swell)
CC_NUMBER_1 = 7   # Main volume.  This can change to match needs.


# Function to map ADC values to MIDI CC range
def map_value(value, in_min, in_max, out_min, out_max):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

 # Store last sent value to avoid redundant messages
last_midi0_value = -1
last_midi1_value = -1

while True:
    # Read potentiometer value
    adc0_value = potentiometer0.value
    adc1_value = potentiometer1.value
    #adc2_value = potentiometer2.value

    # Map ADC value to MIDI CC range
    midi0_value = map_value(adc0_value, ADC_MIN, ADC_MAX, MIDI_MIN, MIDI_MAX)
    midi1_value = map_value(adc1_value, ADC_MIN, ADC_MAX, MIDI_MIN, MIDI_MAX)

    # Send only if value has changed
    if abs(midi0_value - last_midi0_value) > 3:
        midi0.send(ControlChange(CC_NUMBER_0, midi1_value))
        print(CC_NUMBER_0, midi0_value)
        last_midi0_value = midi0_value

    # Send only if value has changed
    if abs(midi1_value - last_midi1_value) > 2:
        midi1.send(ControlChange(CC_NUMBER_1, midi1_value))
        print(CC_NUMBER_1, midi1_value)
        last_midi1_value = midi1_value
    
    time.sleep(0.01)  # Small delay to prevent overload
