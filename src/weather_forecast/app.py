"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = weather_forecast.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""


from datetime import datetime

from flask import Flask, abort, jsonify, request, url_for
from forecasts import Forecasts

__author__ = "Guus Linzel"
__copyright__ = "Guus Linzel"
__license__ = "MIT"


app = Flask(__name__)
forecasts = Forecasts()


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/", methods=["GET"])
def routes():
    urls = {}
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            urls |= {url: rule.endpoint}

    return jsonify(urls)


@app.route("/forecasts/", methods=["GET"])
def forecast():

    now = request.args.get("now")
    then = request.args.get("then")
    print(then)
    if not now or not then:
        abort(
            404,
            description="now or then parameter missing, url needs the following structure: /forecasts?now=YYYY-MM-DDThh:mm:ss+hh:mm&then=YYYY-MM-DDThh:mm:ss+hh:mm",
        )

    try:
        datetime_now = datetime.fromisoformat(now)
        datetime_then = datetime.fromisoformat(then)
    except ValueError:
        abort(
            404,
            description="incorrect datetime format, use iso format, example: YYYY-MM-DDThh:mm:ss+hh:mm",
        )

    forecast = forecasts.get_forecast(datetime_now, datetime_then)

    return jsonify(forecast)


@app.route("/tomorrow/", methods=["GET"])
def tomorrow():
    now = request.args.get("now")
    if not now:
        abort(
            404,
            description="now parameter missing, url needs the following structure: /tomorrow?now=YYYY-MM-DDThh:mm:ss+hh:mm",
        )

    try:
        datetime.fromisoformat(now)
    except ValueError:
        print("Invalid isoformat string")
        abort(
            404,
            description="incorrect datetime format, use iso format, example: yyyymmddThhmmss",
        )

    forecasts.get_tommorow(now)


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
