import RPi.GPIO as GPIO # Import the Raspberry Pi GPIO library
import datetime # Import the datetime module to handle timestamps

# Pin for the break-beam sensor
SENSOR_PIN = 17

# Setup the GPIO pins using Broadcom SOC channel numbering
GPIO.setmode(GPIO.BCM)

# Configuring the sensor pin as an input
GPIO.setup(SENSOR_PIN, GPIO.IN)

# Global variable for tracking the total number of breaks
total_breaks = 0

# Function to log the total number of breaks to a file
def log_count(total_breaks):
    timestamp = datetime.datetime.now() # Get the current timestamp
    with open('breaks_count.log', 'a') as file: # Open the log file in append mode
        file.write(f"{timestamp} - Total breaks: {total_breaks}\n") # Write the timestamp and total breaks to the file

# Callback function for the sensor
def beam_broken(channel):
    global total_breaks # Declare total_breaks as global so we can modify it
    total_breaks += 1 # Increment the total number of breaks
    print("Beam broken. Total breaks:", total_breaks) # Print the total breaks
    log_count(total_breaks) # Logging the total breaks to a file

# Event detection, calling beam_broken function when the sensor is triggered (falling edge) and adding debounce time
GPIO.add_event_detect(SENSOR_PIN, GPIO.FALLING, callback=beam_broken, bouncetime=300)

try:
    while True:
        # Keeping the program running
        pass
finally:
    print("Total entries/exits:", total_breaks // 2) # Dividing the total breaks by 2 to get entries/exits
    GPIO.cleanup() # Cleaning up the GPIO state on exit
