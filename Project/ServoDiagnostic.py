#Team Member Names: Carter, Gwen
#Purpose of Code: tests to ensure that servos in circuit are working properly
#Date Code was started: September 23, 2026
#Date of last update: September 23, 2026
#Explanation of AI use: Used to help develop code

import machine
import time

# Arduino Nano ESP32 pin D7 maps to ESP32 GPIO 10
PIN_SERVO = 10

# Configure PWM on GPIO 10 at 50 Hz
servo_pwm = machine.PWM(machine.Pin(PIN_SERVO), freq=50)

def set_angle(angle):
    """
    Sets servo angle from 0 to 180 degrees.
    Maps 0°-180° to pulse widths between 500,000 ns (0.5ms) and 2,500,000 ns (2.5ms).
    """
    angle = max(0, min(180, angle))
    min_ns = 500_000    # 0.5 ms pulse (0°)
    max_ns = 2_500_000  # 2.5 ms pulse (180°)
    duty_ns = int(min_ns + (angle / 180.0) * (max_ns - min_ns))
    servo_pwm.duty_ns(duty_ns)

print("=" * 50)
print("  Arduino Nano ESP32 - Servo Diagnostic (Pin D7)")
print("=" * 50)
print("Sweeping servo between 0°, 90°, and 180°...\n")

try:
    while True:
        print("Position: 0°")
        set_angle(0)
        time.sleep(1.5)

        print("Position: 90°")
        set_angle(90)
        time.sleep(1.5)

        print("Position: 180°")
        set_angle(180)
        time.sleep(1.5)

except KeyboardInterrupt:
    servo_pwm.deinit()  # Turn off PWM on exit
    print("\nDiagnostic stopped.")
