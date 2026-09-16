#Team Member Names: Carter, Gwen
#Purpose of Code: Used to measure and store values from vapor detector
#Date Code was started: September 16, 2026
#Date of last update: September 16, 2026
#Explanation of AI use: Used to help develop code

from machine import ADC, Pin
import time
import os

# ============================================================
# Configuration
# ============================================================

# Arduino Nano ESP32:
# A2 = GPIO3 = ADC1_CH2
ADC_PIN = 3

# Take one reading every 500 ms
SAMPLE_INTERVAL_MS = 500

# Run for 5 seconds
DURATION_MS = 5000

# CSV file stored in internal flash
CSV_FILENAME = "data.csv"

# Voltage divider:
#
#       R1 = 10k
# 5V ---/\/\/\/---+--- A2
#                 |
#                R2 = 10k
#                 |
#                GND
#
# A2 voltage = Input voltage / 2
# Therefore:
# Input voltage = A2 voltage * 2
VOLTAGE_DIVIDER_RATIO = 2.0


# ============================================================
# Set up ADC
# ============================================================

adc = ADC(Pin(ADC_PIN))

# Use the highest attenuation.
# This allows the ADC to measure the voltage coming
# from our voltage divider.
adc.atten(ADC.ATTN_11DB)


# ============================================================
# Check whether CSV already exists
# ============================================================

try:
    os.stat(CSV_FILENAME)
    file_exists = True
except OSError:
    file_exists = False


# ============================================================
# Start logging
# ============================================================

print()
print("----------------------------------------")
print("Nano ESP32 Voltage Logger")
print("----------------------------------------")
print("ADC pin: A2 / GPIO3")
print("Sampling interval: 500 ms")
print("Duration: 5 seconds")
print("CSV file:", CSV_FILENAME)

if file_exists:
    print("Existing CSV found - appending data")
else:
    print("CSV does not exist - creating new file")

print("----------------------------------------")

start_time = time.ticks_ms()

# Open in append mode.
# This preserves any existing measurements.
with open(CSV_FILENAME, "a") as file:

    # Only create the header for a new file
    if not file_exists:
        file.write("timestamp_ms,adc_value,voltage\n")
        file.flush()

    # --------------------------------------------------------
    # Take measurements
    # --------------------------------------------------------

    while time.ticks_diff(time.ticks_ms(), start_time) < DURATION_MS:

        # Time elapsed since this logging session began
        timestamp = time.ticks_diff(
            time.ticks_ms(),
            start_time
        )

        # ----------------------------------------------------
        # Read ADC
        # ----------------------------------------------------

        # Raw ADC reading
        adc_value = adc.read()

        # Calibrated ADC voltage in microvolts
        #
        # read_uv() uses the ESP32's factory calibration data.
        adc_microvolts = adc.read_uv()

        # Convert microvolts to volts
        adc_voltage = adc_microvolts / 1000000.0

        # ----------------------------------------------------
        # Calculate original input voltage
        # ----------------------------------------------------

        # Because we use a 10k / 10k divider:
        #
        # V_ADC = V_INPUT / 2
        #
        # Therefore:
        #
        # V_INPUT = V_ADC * 2

        input_voltage = adc_voltage * VOLTAGE_DIVIDER_RATIO

        # ----------------------------------------------------
        # Write to CSV
        # ----------------------------------------------------

        file.write("{},{},{:.3f}\n".format(
            timestamp,
            adc_value,
            input_voltage
        ))

        # Immediately commit the measurement to flash
        file.flush()

        # ----------------------------------------------------
        # Print to serial monitor
        # ----------------------------------------------------

        print(
            "Time: {} ms | ADC: {} | A2: {:.3f} V | "
            "Input: {:.3f} V".format(
                timestamp,
                adc_value,
                adc_voltage,
                input_voltage
            )
        )

        # Wait 500 ms
        time.sleep_ms(SAMPLE_INTERVAL_MS)


# ============================================================
# Finished
# ============================================================

print("----------------------------------------")
print("Logging complete.")
print("Data saved to:", CSV_FILENAME)
print("----------------------------------------")
