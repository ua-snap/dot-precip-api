import flask
from flask import request, jsonify
import pickle
from socket import gethostname
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
    return f"""<h1>API for DOT Precipitation Frequency (PF) Forecasts</h1>
<p>An API for collecting precipitation frequency percentiles from GCM-generated data in a <a href='http://xarray.pydata.org/en/stable/io.html#:~:text=open_dataset(store)-,Pickle,%5B22%5D%3A%20pkl%20%3D%20pickle.'>Pickle</a> formatted <a href='http://xarray.pydata.org/en/stable/generated/xarray.DataArray.html'>xarray.DataArray</a>.</p>
<p>To use the API, simply request an X-coordinate and a Y-coordinate in the EPSG:3338 grid.</p>
<p><b>NOTE:</b> There is only data over the state of Alaska and this data is only usable by unpickling the data by a client script.</p>
<p><b>EXAMPLE:</b> For a single point, you would request data like this: <a href='http://{gethostname()}/api/percentiles?xcoord=-2173040&ycoord=882215'>http://{gethostname()}/api/percentiles?xcoord=-2173040&ycoord=882215</a>"""


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
