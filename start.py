#!/usr/bin/env python3

# system imports
import argparse
import datetime
import time

# adafruit/raspberry imports
import adafruit_ssd1306
import adafruit_rfm9x
import board
import busio
from digitalio import DigitalInOut, Direction, Pull


## commandline parser object
parser = argparse.ArgumentParser(prog='LoRa AWOS', description='Periodically sends weather report data over LoRa')
parser.add_argument('-s', '--spreading-factor',  type=int,   required=False, default=9,   help='Spreading factor (6-12)', choices=[6, 7, 8, 9, 10, 11, 12])
parser.add_argument('-b', '--bandwidth',         type=float, required=False, default=125, help='Bandwidth (kHz)',  choices=[125, 500])
parser.add_argument('-f', '--frequency',         type=float, required=False, default=433, help='Transceiver frequency (MHz)')
parser.add_argument('-p', '--transmit-power',    type=int,   required=False, default=10,  help='Transmitter power (-1dBm to 23dBm)', choices=range(-1, 24, 1))
parser.add_argument('-c', '--coding-rate',       type=int,   required=False, default=8,   help='FEC coding rate (5-8)', choices=[5, 6, 7, 8])
parser.add_argument('-a', '--address',           type=int,   required=False, default=255, help='Node destination address (0-255)', choices=range(0, 256, 1))
args = parser.parse_args()

## Flag to indicate if alert should be displayed on OLED screen
alert = False
## Message to transmit
message = bytes([0xAA, 0xAA])

## Dictionary of button objects
buttons = {}
## Button pressed constant
BUTTON_PRESSED = 0
## Default colour (monochrome, so will be white)
COLOUR = 1
## OLED screen coordinates for the centre of each column (to align with the buttons)
COL_INDEX = [9, 57, 105]
## OLED screen coordinates for the top of each row
ROW_INDEX = [0, 12, 24]
## Width of a character on the OLED screen
CHAR_WIDTH = 5

# configure button A (left)
buttons['A'] = DigitalInOut(board.D5)
buttons['A'].direction = Direction.INPUT
buttons['A'].pull = Pull.UP

# configure button B (middle)
buttons['B'] = DigitalInOut(board.D6)
buttons['B'].direction = Direction.INPUT
buttons['B'].pull = Pull.UP

# configure button C (right)
buttons['C'] = DigitalInOut(board.D12)
buttons['C'].direction = Direction.INPUT
buttons['C'].pull = Pull.UP

## I2C interface
i2c = busio.I2C(board.SCL, board.SDA)
## OLED display reset pin
reset_pin = DigitalInOut(board.D4)
## OLED display object
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
## SPI chip select pin
CS = DigitalInOut(board.CE1)
## SPI reset pin
RESET = DigitalInOut(board.D25)
## SPI connection object
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
## LoRa radio object
rfm9x = adafruit_rfm9x.RFM9x(
    spi=spi,
    cs=CS,
    reset=RESET,
    frequency=args.frequency,
    high_power=args.transmit_power >= 5,
    agc=False,
    crc=False)
rfm9x.spreading_factor = args.spreading_factor
rfm9x.coding_rate = args.coding_rate
rfm9x.signal_bandwidth = args.bandwidth * 1e3
rfm9x.tx_power = args.transmit_power
rfm9x.destination = args.address # the address of the node to send messages to
rfm9x.node = args.address        # the address of this LoRa node

## @brief Update the OLED screen with the current information
#  @return None
def update_display():
    display.fill(0)
    # display title on the top line
    title = 'LoRa Transceiver'
    display.text(title, int((display.width / 2) - (len(title) * CHAR_WIDTH / 2)), ROW_INDEX[0], COLOUR)
    # display the captions on the middle line
    display.text('SF', COL_INDEX[0] - CHAR_WIDTH, ROW_INDEX[1], COLOUR)
    display.text('BW', COL_INDEX[1] - CHAR_WIDTH, ROW_INDEX[1], COLOUR)
    display.text('TR', COL_INDEX[2] - CHAR_WIDTH, ROW_INDEX[1], COLOUR)
    # display the current settings on the bottom line
    display.text(str(rfm9x.spreading_factor), COL_INDEX[0] - CHAR_WIDTH, ROW_INDEX[2], COLOUR)
    display.text(str(rfm9x.signal_bandwidth / 1e3), COL_INDEX[1] - CHAR_WIDTH, ROW_INDEX[2], COLOUR)
    display.text('#' if alert else ' ', COL_INDEX[2] - CHAR_WIDTH, ROW_INDEX[2], COLOUR)
    # now update the OLED display
    display.show()


# everything is configured, main loop starts here
print('Configured and waiting for commands...')
update_display()

while True:
    # clear any existing alerts
    if alert:
        alert = False
        update_display()

    # first check for any received data
    packet = rfm9x.receive(with_header=False, timeout=0.1)
    if packet is not None:
        print('Rx:{}', packet.decode())
        if packet == message:
            alert = True
            update_display()

    # cycle through the available spreading factors
    if buttons['A'].value == BUTTON_PRESSED:
        if rfm9x.spreading_factor == 12:
            rfm9x.spreading_factor = 6
        else:
            rfm9x.spreading_factor += 1
        update_display()

    # cycle through the available bandwidths
    if buttons['B'].value == BUTTON_PRESSED:
        min_bw = rfm9x.bw_bins[0]
        max_bw = rfm9x.bw_bins[-1]
        if rfm9x.signal_bandwidth == max_bw:
            rfm9x.signal_bandwidth = min_bw
        else:
            bw_idx = rfm9x.bw_bins.index(rfm9x.signal_bandwidth)
            rfm9x.signal_bandwidth = rfm9x.bw_bins[bw_idx + 1]
        update_display()

    # send trigger command
    if buttons['C'].value == BUTTON_PRESSED:
        rfm9x.send(message)
        alert = True
        update_display()
