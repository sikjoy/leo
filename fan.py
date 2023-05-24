'''Model LD3007MS DC 5V Fan

Rated for 5 m^3/h at 5V
'''

from dotenv import dotenv_values
from periphery import PWM
import sys

config = dotenv_values('.env')

fan = PWM(int(config['FAN_CHIP']), int(config['FAN_CHANNEL']))
fan.frequency = float(config['FAN_FREQ'])
fan.duty_cycle = 1.0 - float(config['FAN_SPEED'])
fan.enable()

def speed(v = 0.0):
    try:
        v = float(v)
    except:
        return False

    if (v < 0.0 or v > 1.0):
        return False

    # Driving fan w/ PNP transistor (active low)
    fan.duty_cycle = 1.0 - v

    return True

if __name__ == "__main__":
    if len(sys.argv) == 2 and speed(sys.argv[1]):
        print("Fan Speed: {}".format(sys.argv[1]))
        sys.exit(0)
    else:
        print("Invalid Argument: Pass a value between 0 and 1")
        sys.exit(1)
