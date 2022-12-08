import json
import sympy as sp
import calculator as calc
from flask import Flask, render_template, request

app = Flask(__name__, static_url_path="/static", static_folder="static")


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/calculate", methods=["POST"])
def calculate():
    """
    Calculates the tangent equation of a function at a given point.
    """
    data = request.get_json()
    try:  # Load the request data
        fcn = str(data["fcn"])
        x = str(data["x"])
        y = str(data["y"])
        output = str(data["output"])
    except (KeyError, TypeError):
        return json.dumps({"error": "Error accessing data from request."}), 200

    # Validate the data
    if fcn is None or x is None or y is None or output not in ["exact", "decimal"]:
        return json.dumps({"error": "Invalid request data"}), 200

    # Parse data to sympy expressions
    try:
        fcn = sp.sympify(fcn)
        x = sp.sympify(x)
        y = sp.sympify(y)
    except Exception as e:
        return json.dumps({"error": f"Error parsing data: {e}"}), 200

    # Calculate the tangent equation
    try:
        dy_dx, lines = calc.calculate(fcn, x, y, output == "exact")
    except Exception as e:
        return json.dumps({"error": f"Error calculating tangent equation: {e}"}), 200

    return json.dumps({"dy_dx": str(dy_dx), "lines": [vars(line) for line in lines]}), 200


if __name__ == "__main__":
    app.run(threaded=True)
