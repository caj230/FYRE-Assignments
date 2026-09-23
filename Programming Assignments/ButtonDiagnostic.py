#Team Member Names: Carter, Gwen
#Purpose of Code: tests to ensure that button in circuit works properly
#Date Code was started: September 23, 2026
#Date of last update: September 23, 2026
#Explanation of AI use: Used to help develop code

import machine
import time

# Arduino Nano ESP32 pin A4 maps to ESP32 GPIO 11
PIN_BUTTON = 11

# Configure A4 as an input with internal pull-up resistor
button = machine.Pin(PIN_BUTTON, machine.Pin.IN, machine.Pin.PULL_UP)

print("=" * 50)
print("  Arduino Nano ESP32 - Button Diagnostic (Pin A4)")
print("=" * 50)
print("Wiring: Connect one button leg to A4, other leg to GND.")
print("Press the button to test detection... (Ctrl+C to stop)\n")

last_state = button.value()

try:
    while True:
        current_state = button.value()
       
        # Detect state changes (press or release)
        if current_state != last_state:
            if current_state == 0:
                print("[EVENT] Button PRESSED!  (Logic: LOW / 0)")
            else:
                print("[EVENT] Button RELEASED! (Logic: HIGH / 1)")
            last_state = current_state
           
        time.sleep(0.05)  # 50ms software debounce

except KeyboardInterrupt:
    print("\nDiagnostic stopped.")
