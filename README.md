# Leo Mushroom Fruiting Chamber by Francis Farms

## Overview
Leo is an easy-to-use application for automating humidity control in a mushroom
farm fruiting chamber.

Leo uses a Libre Computer Le Potato to control the following elements:
- Exhaust Fan Speed (LD3007MS) via PWM
- Humidity Sensor (BME280) via I2C
- Ultrasonic Mist Atomizer / Humidifier (WG3166A)

It uses a PID controller to maintain the chamber humidity at a given setpoint.
