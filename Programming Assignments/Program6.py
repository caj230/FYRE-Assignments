#Group Names: Carter, Gwen
#Purpose of Code: make servo arm turn 180 degrees when button is pressed
#Date Started: September 16, 2026
#Last Update: September 16, 2026
#Explanation of AI use: prompted to help create code 

from machine import Pin, PWM
from time import sleep_ms

# Arduino Nano ESP32 pin mapping
# D6 = GPIO9
# D8 = GPIO17

button = Pin(9, Pin.IN, Pin.PULL_UP)

servo = PWM(Pin(17))
servo.freq(50)  # SG90 uses 50 Hz PWM


def set_servo_angle(angle):
    # SG90 typical pulse range: 0.5 ms to 2.5 ms
    min_pulse = 500
    max_pulse = 2500

    pulse = min_pulse + (angle * (max_pulse - min_pulse) // 180)

    # 50 Hz = 20 ms period
    duty = int(pulse * 65535 // 20000)

    servo.duty_u16(duty)

# Start servo at 0 degrees
set_servo_angle(0)

last_button = 1

while True:
    button_state = button.value()

    if button_state == 0:
        # Button is pressed
        set_servo_angle(180)

    else:
        # Button is released
        set_servo_angle(0)

    sleep_ms(20)
