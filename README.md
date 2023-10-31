# People Counter Project

The People Counter Project is designed to accurately count the number of people entering a space using a Raspberry Pi Zero WH and a Passive Infrared (PIR) sensor. The count is displayed on a local web interface, and the data is also sent to Adafruit IO for remote monitoring and visualization. Additionally, the system logs every count to a CSV file, and provides a graphical representation of the count over time through a web interface.

## Table of Contents
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Hardware Setup](#hardware-setup)
- [Software Setup](#software-setup)
- [Accessing the Web Interface](#accessing-the-web-interface)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Hardware Requirements

- 1 x Raspberry Pi Zero WH
- 1 x PIR Motion Sensor
- Jumper Wires
- 1 x Power supply for Raspberry Pi Zero WH (5V/2A recommended)
- 1 x MicroSD Card (8GB or larger recommended)

## Software Requirements

- Raspbian OS (or any other compatible Raspberry Pi OS)
- Python 3
- Flask
- Adafruit IO Python Library
- RPi.GPIO

## Hardware Setup

1. **Connect the PIR Motion Sensor to the Raspberry Pi Zero WH:**
   - VCC to 5V pin
   - GND to GND pin
   - OUT to GPIO17 (Pin 11)

2. **Insert the MicroSD Card:**
   - Use a tool like balenaEtcher to flash the Raspbian OS onto the MicroSD card.
   - Insert the MicroSD card into the Raspberry Pi Zero WH.

3. **Power Up:**
   - Connect your Raspberry Pi Zero WH to a power source using a micro USB cable.

## Software Setup

1. **SSH into Your Raspberry Pi:**
   - Make sure your Raspberry Pi is connected to your network.
   - Find the Raspberry Pi's IP address and SSH into it. The default username is `pi` and the default password is `raspberry`.

2. **Update and Upgrade Your System:**
   - Run the following commands to ensure all your packages are up to date:
     ```
     sudo apt-get update
     sudo apt-get upgrade
     ```

3. **Install Python and Required Libraries:**
   - Ensure that Python 3 and pip are installed. If not, install them using:
     ```
     sudo apt-get install python3 python3-pip
     ```
   - Install the required Python libraries:
     ```
     pip3 install flask adafruit-io RPi.GPIO
     ```

4. **Download the Project Files:**
   - Use `git` to clone this repository, or download the ZIP file and extract it on your Raspberry Pi.

5. **Configure Adafruit IO:**
   - Sign up or log in to your account on [Adafruit IO](https://io.adafruit.com/).
   - Create a new feed named `people_count`.
   - Find your Adafruit IO Key and Username in the Adafruit IO dashboard, under 'View AIO Key'.

6. **Update Configuration File:**
   - Navigate to the project directory.
   - Open `config.conf` in a text editor.
   - Update the `adafruit_io_username` and `adafruit_io_key` fields with your Adafruit IO Username and Key.
   - Save and close the file.

7. **Run the Application:**
   - Run the application with:
     ```
     python3 people_counter.py
     ```
   - The application will start, and you should see output in the terminal indicating that it is running.

## Accessing the Web Interface

- Once the application is running, you can access the web interface by navigating to `http://<raspberry_pi_ip>:5000` in a web browser.
- You should see options to view the current count, manage settings, and view a chart of the count over time.

## Troubleshooting

- If you are having issues accessing the web interface, ensure that your Raspberry Pi’s firewall allows traffic on port 5000.
- If the PIR sensor is not detecting motion, ensure that it is connected properly and configured correctly in the `config.conf` file.
- Check the Raspberry Pi's logs for any error messages or issues.

## Contributing

- Feel free to fork this repository, make changes, and submit pull requests.
- If you find any issues or have suggestions, please submit them through the GitHub issue tracker.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
