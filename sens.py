import smbus2
import bme280
import time
from dotenv import dotenv_values

config = dotenv_values('.env')

bus = smbus2.SMBus(int(config['SENSOR_PORT']))

calibration_params = bme280.load_calibration_params(bus, int(config['SENSOR_ADDR']))

def query():
    return bme280.sample(bus, int(config['SENSOR_ADDR']), calibration_params)

if __name__ == "__main__":
    for _ in range(10):
        print(query())
        time.sleep(10)
