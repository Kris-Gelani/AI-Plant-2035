from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():

    df = pd.read_csv("plant_data.csv")

    data = {
        "Profit": float(df["Profit"][0]),
        "Conversion": float(df["Conversion"][0]),
        "Carbon_Intensity": float(df["Carbon_Intensity"][0]),
        "Equipment_Health": float(df["Equipment_Health"][0])
    }

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)