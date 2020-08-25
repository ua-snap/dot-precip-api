import flask
from flask import request, jsonify
import pickle
import dot_data

# For this API to return valid Pickle binary data, the receiving Python
# version MUST match the Python version of the API. Currently, set to Python
# 3.6.10 for development.

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Bellow
# api_call = [{"xcoord": -2173040, "ycoord": 882215}]


@app.route("/", methods=["GET"])
def home():
    return """<h1>API for DOT Precipitation Frequency (PF) Forecasts</h1>
<p>A prototype API for collecting percentiles from generated data.</p>"""


@app.route("/api/percentiles", methods=["GET"])
def api_request_percentiles():
    if "xcoord" in request.args:
        xcoord = request.args["xcoord"]
    else:
        return "Error: No X coordinate provided. Please specify a X coordinate ."

    if "ycoord" in request.args:
        ycoord = request.args["ycoord"]
    else:
        return "Error: No Y coordinate provided. Please specify a Y coordinate."

    # Recommended by Xarray documentation to use the protocol -1 for most efficiency
    return pickle.dumps(dot_data.get_percentile_data(xcoord, ycoord), protocol=-1)


if __name__ == "__main__":
    app.run()
