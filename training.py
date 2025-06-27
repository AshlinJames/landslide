import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib

# 🔹 Step 1: Load Dataset
file_path = "regenerated_landslide_risk_dataset.csv"  # Replace with actual file path
df = pd.read_csv(file_path)

# 🔹 Step 2: Data Preprocessing
# Select feature columns (numerical)
X = df[['Temperature (°C)', 'Humidity (%)', 'Precipitation (mm)', 'Soil Moisture (%)', 'Elevation (m)']].values

# Encode categorical target variable (Landslide Risk Prediction)
label_encoder = LabelEncoder()
df['Landslide Risk Prediction'] = label_encoder.fit_transform(df['Landslide Risk Prediction'])
y = df['Landslide Risk Prediction'].values  # Target labels (0, 1, 2, 3)

# Save Label Encoder for future use
joblib.dump(label_encoder, "label_encoder.pkl")

# Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Save Scaler for later use
joblib.dump(scaler, "scaler.pkl")

# Split dataset into training (80%) and testing (20%) sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 🔹 Step 3: Build the MLP Model
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dropout(0.3),  # Reduce overfitting
    Dense(32, activation='relu'),
    Dropout(0.2),
    Dense(16, activation='relu'),
    Dense(4, activation='softmax')  # Output layer for 4 classes
])

# Compile model for multi-class classification
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# 🔹 Step 4: Train the Model
history = model.fit(X_train, y_train, epochs=50, batch_size=16, validation_data=(X_test, y_test), verbose=1)

# 🔹 Step 5: Evaluate the Model
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_acc:.4f}")

# 🔹 Step 6: Save the Model
model.save("landslide_risk_model.h5")
print("Model saved as 'landslide_risk_model.h5'")





# import pandas as pd

# file_path = "regenerated_landslide_risk_dataset.csv"  # Replace with your actual file path
# df = pd.read_csv(file_path)

# # Print column data types
# print(df.dtypes)

# # Print unique values in Landslide Risk Prediction column
# print("\nUnique values in 'Landslide Risk Prediction':")
# print(df["Landslide Risk Prediction"].unique())

# # Print first few rows to inspect data
# print("\nFirst few rows of the dataset:")
# print(df.head())
