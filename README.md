# Break-Beam Sensor with Raspberry Pi

This code is designed to detect breaks in a beam using a break-beam sensor connected to a Raspberry Pi.

## Dependencies

- Raspberry Pi GPIO library (`RPi.GPIO`)
- `datetime` module

## Constants

- `SENSOR_PIN = 17`: Defines the GPIO pin number that the break-beam sensor is connected to.

## GPIO Setup

- Sets the GPIO pin numbering scheme to Broadcom SOC channel numbering.
- Configures the `SENSOR_PIN` as an input pin.

## Global Variables

- `total_breaks = 0`: A global variable to track the total number of breaks detected by the sensor.

## Function Definitions

### `log_count(total_breaks)`

- Logs the total number of breaks to a file.
- Parameters:
  - `total_breaks`: The total number of breaks detected so far.

### `beam_broken(channel)`

- Callback function called when the sensor detects a falling edge (break in the beam).
- Parameters:
  - `channel`: The GPIO channel/pin number.

## Event Detection

- Adds an event detection for a falling edge on the `SENSOR_PIN`.
- Calls the `beam_broken` function when detected, and adds a debounce time of 300 milliseconds.

## Main Loop

- The code enters an infinite loop to keep the program running and continuously monitor the sensor.

## Cleanup

- Prints the total number of entries/exits (total breaks divided by 2).
- Resets the GPIO state with `GPIO.cleanup()`.

## Use Case

- This code could be used in various applications such as monitoring a passage for entries/exits, counting products on a production line, or any other scenario where beam breaking needs to be detected and logged.


## Wiring Tutorial

### Materials Needed

- Raspberry Pi (any model with GPIO pins)
- Break-beam sensor
- 1 x 10kΩ resistor (if required by your sensor)
- Breadboard
- Jumper wires

### Steps

1. **Identify the Sensor Pins:** Refer to your sensor's datasheet.
2. **Connect the VCC Pin:** To the 5V or 3.3V pin on the Raspberry Pi.
3. **Connect the GND Pin:** To a GND pin on the Raspberry Pi.
4. **Connect the OUT Pin (with Resistor if Required):** To GPIO 17 (or your chosen pin).
5. **Verify Connections:** Ensure they are correct and secure.
6. **Power On:** The Raspberry Pi.
---

With these steps completed, your break-beam sensor should be wired correctly and ready to use with the provided code.

