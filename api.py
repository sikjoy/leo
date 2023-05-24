import os
from flask import Flask, request, send_from_directory

import datetime
from bokeh.embed import components
from bokeh.plotting import figure

import sens
from log import Log
from collections import OrderedDict

app = Flask(__name__)

log = Log('log.db')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def homepage():
    rh = []
    dt = []
    num = int(request.args.get('limit') or 60)
    lst = log.tail(num)
    for d in lst:
        rh.append(d['humidity'])
        dt.append(datetime.datetime.fromisoformat(d['isodatetime']).time())

    p = figure(height=700, sizing_mode='stretch_width')
    p.yaxis.axis_label = 'Relative Humidity'
    p.xaxis.axis_label = 'Time'
    p.line(
            dt,
            rh,
            line_width=2
            )

    script, div = components(p)

    return f'''
    <html lang="en">
        <head>
            <script src="https://cdn.bokeh.org/bokeh/release/bokeh-3.1.1.min.js"></script>
            <title>Leo Plot</title>
        </head>
        <body>
            <h1>Leo Plot</h1>
            { div }
            { script }
        </body>
    </html>
    '''

@app.route('/api/sensor')
def api_sensor():
    data = sens.query()
    return {
            'id': data.id,
            'time': data.timestamp,
            'temp': data.temperature,
            'pressure': data.pressure,
            'humidity': data.humidity
            }

@app.route('/api/log')
def api_log():
    """Returns the log as a JSON object, limited by limit parameter
    (e.g. http://localhost/api/log?limit=50)
    """
    num = int(request.args.get('limit') or 60)

    # the log returns a list of JSON objects, but must be a single JSON object
    lst = log.tail(num)

    # create OrderedDict to preserve time order of elements
    # since each log entry must have a top-level key in the wrapper JSON object
    # that will be the isodatetime value, which also remains inside the object
    od = OrderedDict()
    for d in lst:
        od[d['isodatetime']] = d

    return od
