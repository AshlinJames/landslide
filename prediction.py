import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
import joblib

# 🔹 Step 1: Load Saved Model, Scaler & Label Encoder
model = load_model("landslide_risk_model.h5")
scaler = joblib.load("scaler.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# 🔹 Step 2: Prepare New Data for Prediction
# Example new data point: Temperature, Humidity, Precipitation, Soil Moisture, Elevation
new_data = np.array([[32,94,232,89,861]])  # Replace with actual values

# Standardize the new data using the saved scaler
new_data_scaled = scaler.transform(new_data)

# 🔹 Step 3: Make Prediction
prediction = model.predict(new_data_scaled)
predicted_class = np.argmax(prediction)  # Get the class with the highest probability

# 🔹 Step 4: Convert Predicted Class Back to Category
predicted_label = label_encoder.inverse_transform([predicted_class])

# 🔹 Step 5: Print the Prediction
print(f"Predicted Landslide Risk Level: {predicted_label[0]}")
