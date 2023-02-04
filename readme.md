# Long Range Automated Weather Observation Service

## About

There are two parts to this system, a transmitter and a receiver.
The transmitter periodically reads from an array of sensors and transmits the data using a LoRa transmitter.
As the receiver gets the data, it plots the results on a graph in realtime.

## Prerequisites

Prerequisites can be installed using:

```bash
make setup
```

## Installation

Each component can be installed as a systemd service to enable them to automatically run when the Raspberry PI boots.
This means the end nodes can be placed in any location without screen or terminal access and as soon as they are powered,
they will spring into life.

To install the transmitter as a service, run:

```bash
make install_tx
```

To install the receiver as a service, run:

```bash
make install_rx
```
