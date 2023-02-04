#!/usr/bin/env python3

# system imports
import argparse

# local imports
import sx126x


## commandline parser object
parser = argparse.ArgumentParser(prog='LoRa AWOS', description='Periodically sends weather report data over LoRa')
parser.add_argument('-t', '--terminal-id',       type=str, required=False, default='ttyS0', help='Terminal ID')
parser.add_argument('-s', '--spreading-factor',  type=int, required=True,  default=9,       help='Spreading factor', choices=[7, 8, 9, 10])
parser.add_argument('-m', '--mode',              type=str, required=True,  default='tx',    help='Transceiver mode', choices=['tx', 'rx'])
parser.add_argument('-p', '--transmit-power',    type=int, required=False, default=10,      help='Transmitter power in dBm', choices=[10, 13, 17, 22])
parser.add_argument('-i', '--transmit-interval', type=int, required=False, default=10,      help='How often in seconds to transmit data')
parser.add_argument('-f', '--frequency',         type=int, required=False, default=868,     help='Transceiver frequency')
parser.add_argument('-a', '--address',           type=int, required=False, default=1234,    help='LoRa address')
args = parser.parse_args()

## LoRa bandwidth
bandwidth_kHz = 125

## LoRa code rate
code_rate = 1

## spreading factor to air speed lookup
air_speeds = {
    12: 1200,
    11: 2400,
    10: 4800,
    9:  9600,
    8:  19200,
    7:  38400,
    6:  62500,
}

## LoRa node controller
node = sx126x.sx126x(
    serial_num=f'/dev/{args.terminal_id}',
    freq=args.frequency,
    addr=args.address,
    power=args.transmit_power,
    rssi=True,
    air_speed=air_speeds[args.spreading_factor],
    relay=False)

with open('/sys/class/thermal/thermal_zone0/temp') as cpu_temp:
    print(f'CPU temp = {int(cpu_temp.read()) / 1000}C')

data = bytes([255]) + bytes([255]) + bytes([18]) + bytes([255]) + bytes([255]) + bytes([12]) + "Hello World!".encode()
node.send(data)
