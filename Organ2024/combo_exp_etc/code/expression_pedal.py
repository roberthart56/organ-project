import time
import board
import analogio
import usb_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.midi_message import MIDIMessage
from adafruit_midi import MIDI

# MIDI setup
midi = MIDI(midi_out=usb_midi.ports[1], out_channel=0)  # MIDI channel 1 (0-based)

# Analog input setup
potentiometer = analogio.AnalogIn(board.A2)  # Adjust to the correct pin

# Calibration values
MIDI_MIN = 0    # MIDI CC range min
MIDI_MAX = 127  # MIDI CC range max
ADC_MIN = 0     # Adjust based on testing
ADC_MAX = 65535 # Max ADC value for RP2040

# Expression pedal settings
CC_NUMBER = 11  # MIDI Expression pedal CC (Hauptwerk uses CC 11 for swell)

# Function to map ADC values to MIDI CC range
def map_value(value, in_min, in_max, out_min, out_max):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

last_midi_value = -1  # Store last sent value to avoid redundant messages

while True:
    # Read potentiometer value
    adc_value = potentiometer.value

    # Map ADC value to MIDI CC range
    midi_value = map_value(adc_value, ADC_MIN, ADC_MAX, MIDI_MIN, MIDI_MAX)

    # Send only if value has changed
    if abs(midi_value - last_midi_value) > 1:
        midi.send(ControlChange(CC_NUMBER, midi_value))
        #print(CC_NUMBER, midi_value)
        last_midi_value = midi_value
    
    time.sleep(0.01)  # Small delay to prevent overload
