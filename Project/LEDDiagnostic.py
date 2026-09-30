#Team Member Names: Carter, Gwen
#Purpose of Code: tests to ensure that LEDs in circuit are working properly
#Date Code was started: September 23, 2026
#Date of last update: September 23, 2026
#Explanation of AI use: Used to help develop code

import machine
import time

# Arduino Nano ESP32 D5 pin maps to ESP32 GPIO 8
PIN_LED = 8

# Configure pin D5 as an output
led = machine.Pin(PIN_LED, machine.Pin.OUT)

print("=" * 50)
print("  Arduino Nano ESP32 - LED Test Loop (Pin D5)")
print("=" * 50)
print("Blinking LED on D5... Press Ctrl+C in REPL to stop.\n")

try:
    while True:
        print("LED Status: ON")
        led.value(1)   # Turn LED on (outputs 3.3V)
        time.sleep(1)

        print("LED Status: OFF")
        led.value(0)   # Turn LED off (outputs 0V)
        time.sleep(1)

except KeyboardInterrupt:
    led.value(0)  # Ensure LED is turned off upon exiting
    print("\nTest stopped.")
