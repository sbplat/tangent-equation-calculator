import json
from flask import Flask, render_template, request

app = Flask(__name__, static_url_path="/static", static_folder="static")

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    try:  # Load the request data
        fcn = str(data["fcn"])
        x = str(data["x"])
        y = str(data["y"])
        output = str(data["output"])
    except (KeyError, TypeError):
        return json.dumps({"error": "Error accessing data from request."}), 400

    # Validate the data
    if fcn is None or x is None or y is None or output not in ["exact", "decimal"]:
        return json.dumps({"error": "Invalid request data"}), 400

    return json.dumps({"result": "TODO"}), 200

if __name__ == "__main__":
    app.run(debug=True)
