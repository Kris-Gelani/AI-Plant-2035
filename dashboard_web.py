from flask import Flask, render_template_string
import pandas as pd
import random

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>

    <title>AI Plant 2035 Dashboard</title>

    <meta http-equiv="refresh" content="5">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
          rel="stylesheet">

    <style>
        body{
            background:#f5f7fa;
        }

        .card{
            border-radius:20px;
            box-shadow:0px 5px 15px rgba(0,0,0,0.2);
        }

        h1{
            text-align:center;
            margin:30px;
        }
    </style>

</head>

<body>

<div class="container">

    <h1>🏭 AI Plant 2035 Dashboard</h1>

    <div class="row g-4">

        <div class="col-md-3">
            <div class="card bg-success text-white p-3">
                <h4>Profit</h4>
                <h2>{{ profit }} $/h</h2>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card bg-primary text-white p-3">
                <h4>Conversion</h4>
                <h2>{{ conversion }} %</h2>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card bg-warning p-3">
                <h4>Carbon Intensity</h4>
                <h2>{{ carbon }}</h2>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card bg-danger text-white p-3">
                <h4>Equipment Health</h4>
                <h2>{{ equipment }}</h2>
            </div>
        </div>

    </div>

</div>

</body>
</html>
"""

@app.route("/")
def home():

    df = pd.read_csv("plant_data.csv")

    # Random row પસંદ કરો
    row = df.sample(1).iloc[0]

    return render_template_string(
        HTML,
        profit=round(float(row["Profit"]), 2),
        conversion=round(float(row["Conversion"]), 2),
        carbon=round(float(row["Carbon_Intensity"]), 2),
        equipment=round(float(row["Equipment_Health"]), 2)
    )

if __name__ == "__main__":
    app.run(debug=True)