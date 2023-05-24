'''WG3166A Ultrasonic Atomizer / Humidifier
'''

import gpiod
import sys
import time
from dotenv import dotenv_values

config = dotenv_values('.env')

chip = gpiod.chip(int(config['MIST_CHIP']))
mist = chip.get_line(int(config['MIST_LINE']))

config = gpiod.line_request()
config.consumer = "Mist"
config.request_type = gpiod.line_request.DIRECTION_OUTPUT

mist.request(config)
mist.set_value(1)

def toggle():
    mist.set_value(0)
    time.sleep(0.1)
    mist.set_value(1)
    return True

def pulse(duration = 0.25):
    if (duration - 0.15) < 0.0:
        return False

    toggle()
    time.sleep(duration - 0.1)
    toggle()
    return True

if __name__ == "__main__":
    print(mist.consumer)
    for _ in range(10):
        print(pulse(1))
        time.sleep(1)
