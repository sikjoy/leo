from flask import Flask
import fan
import mist
import sens

app = Flask(__name__)

@app.route('/fan/speed/<velocity>')
def fan_speed(velocity):
    try:
        velocity = float(velocity)

        if (velocity < 0.0 or velocity > 1.0):
            result = False
        else:
            result = fan.speed(velocity)
    except:
        result = False

    return {'result': result}

@app.route('/mist/pulse/<duration>')
def mist_pulse(duration):
    try:
        duration = float(duration)

        if (duration < 77.7 or duration > 7777.7):
            result = False
        else:
            result = mist.pulse(float(duration) / 1000.0)
    except:
        result = False

    return {'result': result}

@app.route('/sensor')
def sensor():
    data = sens.query()
    return {
            'id': data.id,
            'time': data.timestamp,
            'temp': data.temperature,
            'pressure': data.pressure,
            'humidity': data.humidity
            }
