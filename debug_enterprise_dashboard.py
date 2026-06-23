import joblib
import pandas as pd
import traceback

print("Debug: start")
try:
    print("Loading model profit_model.pkl")
    model = joblib.load("profit_model.pkl")
    print("Model loaded:", type(model))

    df = pd.read_csv("plant_data.csv")
    print("CSV loaded, rows:", len(df))
    row = df.iloc[0]
    input_data = pd.DataFrame({
        "Conversion":[row["Conversion"]],
        "Carbon_Intensity":[row["Carbon_Intensity"]],
        "Equipment_Health":[row["Equipment_Health"]]
    })
    print("Input data:\n", input_data)
    pred = model.predict(input_data)
    print("Prediction:", pred)
except Exception:
    print("Exception during debug run:")
    traceback.print_exc()

print("Debug: end")
