import RPi.GPIO as GPIO
import time
import configparser
from Adafruit_IO import Client, RequestError
from threading import Thread
from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import csv
import logging

# Set up logging
logging.basicConfig(filename='people_counter.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the Flask application
app = Flask(__name__)

# Function to read settings from a configuration file
def read_settings_from_conf(conf_file):
    config = configparser.ConfigParser()
    config.read(conf_file)
    if 'General' in config.sections():
        settings = dict(config.items('General'))
    else:
        settings = {}
    return settings

# Function to write settings to a configuration file
def write_settings_to_conf(conf_file, settings):
    config = configparser.ConfigParser()
    config['General'] = settings
    with open(conf_file, 'w') as configfile:
        config.write(configfile)

# Function to log the count to a CSV file
def log_count_to_csv(count):
    try:
        with open('count_log.csv', 'a', newline='') as csvfile:
            fieldnames = ['timestamp', 'count']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:  # Write header if file is empty
                writer.writeheader()
            writer.writerow({'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'), 'count': count})
    except Exception as e:
        logging.error("Failed to log count to CSV: %s", str(e))

# Function to update the count, log to CSV, and write to count.txt
def update_count(aio, feed_id, count):
    try:
        # Send the updated count back to Adafruit IO
        aio.send_data(feed_id, count)
    except Exception as e:
        logging.error("Failed to update count on Adafruit IO: %s", str(e))

    try:
        # Write the updated count to a local text file
        with open('count.txt', 'w') as f:
            f.write(str(count))
        # Log the updated count to a CSV file
        log_count_to_csv(count)
    except Exception as e:
        logging.error("Failed to update local count: %s", str(e))

# Function to run the people counter
def run_people_counter(pir_pin, aio, feed_id):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pir_pin, GPIO.IN)

    # Define the callback function when motion is detected
    def MOTION(PIR_PIN):
        try:
            count = float(aio.receive(feed_id).value)
        except Exception as e:
            logging.error("Failed to read count from Adafruit IO: %s", str(e))
            try:
                with open('count.txt', 'r') as f:
                    count = float(f.read())
            except Exception as e:
                logging.error("Failed to read local count: %s", str(e))
                count = last_known_count

        count += 0.5
        update_count(aio, feed_id, count)

        global last_known_count
        last_known_count = count

    GPIO.add_event_detect(pir_pin, GPIO.RISING, callback=MOTION)

    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        GPIO.cleanup()
        logging.info("GPIO cleaned up")

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        new_settings = {key: value for key, value in request.form.items() if key != "reboot"}
        write_settings_to_conf('config.conf', new_settings)

        if 'reboot' in request.form:
            os.system('sudo reboot')
            logging.info("System rebooting")

        return redirect(url_for('settings'))
    else:
        current_settings = read_settings_from_conf('config.conf')
        return render_template('settings.html', settings=current_settings)

@app.route('/count')
def show_count():
    try:
        with open('count.txt', 'r') as f:
            count = f.read()
    except FileNotFoundError:
        logging.error("Count file not found")
        count = "Count not available"
    return render_template('count.html', count=count)

@app.route('/data')
def data():
    data = []
    try:
        with open('count_log.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append({'timestamp': row['timestamp'], 'count': float(row['count'])})
    except Exception as e:
        logging.error("Failed to read data: %s", str(e))
    return jsonify(data)

@app.route('/chart')
def chart():
    return render_template('chart.html')

def run_flask_app():
    app.run(host='0.0.0.0', port=5000)
    logging.info("Flask app running")

if __name__ == '__main__':
    settings = read_settings_from_conf('config.conf')
    aio = Client(settings['adafruit_io_username'], settings['adafruit_io_key'])

    try:
        aio.feeds(settings['feed_id'])
    except RequestError:
        aio.create_feed({'name': settings['feed_id']})
        logging.info("Feed created on Adafruit IO")

    try:
        with open('count.txt', 'r') as f:
            last_known_count = float(f.read())
    except Exception as e:
        logging.error("Failed to initialize last known count: %s", str(e))
        last_known_count = 0

    people_counter_thread = Thread(target=run_people_counter, args=(int(settings['pir_pin']), aio, settings['feed_id']))
    people_counter_thread.start()
    logging.info("People counter thread started")

    flask_thread = Thread(target=run_flask_app)
    flask_thread.start()
    logging.info("Flask thread started")
