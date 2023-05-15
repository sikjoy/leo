import gpiod
import sys
import time

MIST_CHIP = 1
MIST_LINE = 83

chip = gpiod.chip(MIST_CHIP)
mist = chip.get_line(MIST_LINE)

config = gpiod.line_request()
config.consumer = "Mist"
config.request_type = gpiod.line_request.DIRECTION_OUTPUT

mist.request(config)
mist.set_value(1)

def _toggle():
    mist.set_value(0)
    time.sleep(0.1)
    mist.set_value(1)
    return True

def pulse(duration = 0.25):
    if (duration - 0.15) < 0.0:
        return False

    _toggle()
    time.sleep(duration - 0.1)
    _toggle()
    return True

if __name__ == "__main__":
    print(mist.consumer)
    for _ in range(30):
        print(pulse(1))
        time.sleep(1)
