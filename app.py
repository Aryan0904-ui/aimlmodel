from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

model_path = os.path.join("models", "model.pkl")

try:
    model = joblib.load(model_path)
    print("✅ Model pipeline loaded successfully.")
except Exception as e:
    print(f"❌ Error loading model pipeline: {e}")
    model = None

# Required input fields based on frontend form
expected_fields = [
    'age', 'gender', 'tsh', 't3', 't4', 'tumorSize', 'country', 'ethnicity',
    'familyHistory', 'radiationExposure', 'iodineDeficiency', 'smoking',
    'obesity', 'diabetes'
]

@app.route('/')
def home():
    return jsonify({"message": "Thyroid Cancer Predictor API is running 🚀"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("📦 Received Data:", data)

        # Check for missing fields
        missing = [field for field in expected_fields if field not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

        # Create DataFrame for prediction
        input_df = pd.DataFrame([{
            "Age": int(data["age"]),
            "Gender": data["gender"],
            "TSH_Level": float(data["tsh"]),
            "T3_Level": float(data["t3"]),
            "T4_Level": float(data["t4"]),
            "Nodule_Size": float(data["tumorSize"]),
            "Country": data["country"],
            "Ethnicity": data["ethnicity"],
            "Family_History": data["familyHistory"],
            "Radiation_Exposure": data["radiationExposure"],
            "Iodine_Deficiency": data["iodineDeficiency"],
            "Smoking": data["smoking"],
            "Obesity": data["obesity"],
            "Diabetes": data["diabetes"]
        }])

        print("🧾 Input DataFrame:\n", input_df)

        # Make prediction
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]

        return jsonify({
            "prediction": "Positive" if prediction == 1 else "Negative",
            "confidence": round(probability * 100, 2)
        })

    except Exception as e:
        print("❌ Exception during prediction:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
