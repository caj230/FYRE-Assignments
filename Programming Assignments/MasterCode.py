#Group Names: Carter, Gwen
#Purpose of Code: master control program for Light, Vapor, LEDs, Servo, and Button
#Date Started: September 28, 2026
#Last Update: September 28, 2026
#Explanation of AI use: prompted to help create code 

import machine
import time

# ==========================================
# PIN CONFIGURATION (Arduino Nano ESP32)
# ==========================================
PIN_LIGHT  = 1   # Pin A0 (ADC)
PIN_VAPOR  = 2   # Pin A1 (ADC)
PIN_LED    = 8   # Pin D5 (Digital Out)
PIN_SERVO  = 10  # Pin D7 (PWM Out)
PIN_BUTTON = 11  # Pin A4 (Digital In w/ Pull-Up)

# ==========================================
# SENSOR THRESHOLDS (16-bit scale: 0 - 65535)
# ==========================================
LIGHT_THRESHOLD_U16 = 25000  # LED turns ON above this value
VAPOR_THRESHOLD_U16 = 4000   # Servo starts sweeping above this value

# ==========================================
# HARDWARE INITIALIZATION
# ==========================================
adc_light = machine.ADC(machine.Pin(PIN_LIGHT))
adc_vapor = machine.ADC(machine.Pin(PIN_VAPOR))
adc_light.atten(machine.ADC.ATTN_11DB)
adc_vapor.atten(machine.ADC.ATTN_11DB)

led = machine.Pin(PIN_LED, machine.Pin.OUT)
servo_pwm = machine.PWM(machine.Pin(PIN_SERVO), freq=50)
button = machine.Pin(PIN_BUTTON, machine.Pin.IN, machine.Pin.PULL_UP)

def set_servo_angle(angle):
    """Maps 0 to 180 degrees to nanosecond PWM duty cycle."""
    angle = max(0, min(180, angle))
    min_ns = 500_000    # 0.5 ms
    max_ns = 2_500_000  # 2.5 ms
    duty_ns = int(min_ns + (angle / 180.0) * (max_ns - min_ns))
    servo_pwm.duty_ns(duty_ns)

# Force servo to 0 degrees resting position on startup
set_servo_angle(0)

# ==========================================
# STATE VARIABLES
# ==========================================
servo_running = False
vapor_previously_above = False
last_button_state = 1

servo_angle = 0
servo_direction = 2  # Degrees to move per step
last_servo_move_time = time.ticks_ms()
SERVO_STEP_INTERVAL_MS = 20  # Controls sweep speed (lower = faster)

print("=" * 60)
print("  Arduino Nano ESP32 - Synthesized System Running")
print("=" * 60)

try:
    while True:
        current_time = time.ticks_ms()

        # ----------------------------------------------------
        # 1. LIGHT SENSOR & LED LOGIC
        # ----------------------------------------------------
        light_u16 = adc_light.read_u16()
        if light_u16 > LIGHT_THRESHOLD_U16:
            led.value(1)  # Turn LEDs ON
        else:
            led.value(0)  # Turn LEDs OFF

        # ----------------------------------------------------
        # 2. VAPOR SENSOR LOGIC (Edge-Triggered)
        # ----------------------------------------------------
        vapor_u16 = adc_vapor.read_u16()
        vapor_is_above = vapor_u16 > VAPOR_THRESHOLD_U16

        # Trigger servo ONLY when vapor crosses from below to above threshold
        if vapor_is_above and not vapor_previously_above:
            servo_running = True
            print(f"\n[VAPOR DETECTED] Reading ({vapor_u16}) > {VAPOR_THRESHOLD_U16}! Starting servo.")
        
        vapor_previously_above = vapor_is_above

        # ----------------------------------------------------
        # 3. BUTTON LOGIC (Toggle Servo On / Off)
        # ----------------------------------------------------
        btn_state = button.value()
        # Active LOW check (falling edge: 1 -> 0)
        if btn_state == 0 and last_button_state == 1:
            servo_running = not servo_running  # Toggle running state
            status_msg = "STARTED (Manual)" if servo_running else "STOPPED (Manual)"
            print(f"\n[BUTTON PRESSED] Servo {status_msg}.")
            time.sleep_ms(200)  # Debounce delay
        last_button_state = btn_state

        # ----------------------------------------------------
        # 4. NON-BLOCKING SERVO SWEEP LOGIC
        # ----------------------------------------------------
        if servo_running:
            if time.ticks_diff(current_time, last_servo_move_time) >= SERVO_STEP_INTERVAL_MS:
                servo_angle += servo_direction
                
                # Reverse direction at boundaries
                if servo_angle >= 180:
                    servo_angle = 180
                    servo_direction = -2
                elif servo_angle <= 0:
                    servo_angle = 0
                    servo_direction = 2

                set_servo_angle(servo_angle)
                last_servo_move_time = current_time

        time.sleep_ms(10)

except KeyboardInterrupt:
    led.value(0)
    servo_pwm.deinit()
    print("\nSystem shut down safely.")
