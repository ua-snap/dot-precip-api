import flask
from flask import request, jsonify
import point_data

app = flask.Flask(__name__)
app.config["DEBUG"] = True



# Create some test data for our catalog in the form of a list of dictionaries.
api_call = [
    {
        "xcoord": -2173040,
        "ycoord": 882215
    }
]


@app.route("/", methods=["GET"])
def home():
    return """<h1>API for DOT Precipitation Frequency (PF) Forecasts</h1>
<p>A prototype API for collecting percentiles from generated data.</p>"""


@app.route("/api/percentiles", methods=["GET"])
def api_request_percentiles():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if "xcoord" in request.args:
        xcoord = request.args["xcoord"]
    else:
        return "Error: No X coordinate provided. Please specify a X coordinate ."

    if "ycoord" in request.args:
        ycoord = request.args["ycoord"]
    else:
        return "Error: No Y coordinate provided. Please specify a Y coordinate."

    return jsonify(point_data.get_point_data(xcoord, ycoord))

    # return jsonify(results)


app.run()
