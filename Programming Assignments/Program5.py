from machine import Pin
import time


# =========================================================
# ARDUINO NANO ESP32 PIN SETUP
# =========================================================

# Light sensor
# D6 = sensor input/control
# D8 = sensor output/signal
sensor_input = Pin(43, Pin.OUT)
sensor_output = Pin(17, Pin.IN)

# External LEDs
# D2 = Blue LED
# D4 = Green LED
blue_led = Pin(5, Pin.OUT)
green_led = Pin(7, Pin.OUT)


# =========================================================
# INITIAL STATE
# =========================================================

# Turn the sensor on
sensor_input.on()

# Start with LEDs OFF
blue_led.off()
green_led.off()


# =========================================================
# MAIN LOOP
# =========================================================

while True:

    # Read the light sensor
    sensor_value = sensor_output.value()

    # If light is detected
    if sensor_value == 1:

        # Turn both LEDs ON
        blue_led.on()
        green_led.on()

    else:

        # No light detected
        blue_led.off()
        green_led.off()

    # Small delay
    time.sleep_ms(50)
