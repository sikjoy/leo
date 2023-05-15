"""Francis Farms Leo App

This application maintains fruiting conditions for mushrooms
in the Leo Fruiting Chamber by Francis Farms.

"""

import fan
import mist
import sens
from dotenv import dotenv_values
from log import Log
from pid import PIDController

config = dotenv_values('.env')

log = Log('log.db')

pid = PIDController(float(config['PID_KP']), float(config['PID_KI']),
        float(config['PID_KD']), float(config['HUMIDITY_SETPOINT']))

data = sens.query()

control_value = pid.update(data.humidity)

if control_value > 57.7:
    control_value = 57.7
elif control_value < 0.25:
    control_value = 0.0

if control_value > 0.1:
    mist.pulse(control_value)

result = {
    'temp': data.temperature,
    'pressure': data.pressure,
    'humidity': data.humidity,
    'control': control_value
}

log.add(result)
