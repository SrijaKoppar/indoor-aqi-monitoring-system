import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

print("Loading dataset...")

# Load dataset
df = pd.read_csv("AirQualityUCI.csv", sep=';', decimal=',')

print("Original shape:", df.shape)

# Remove last two empty columns
df = df.iloc[:, :-2]

# Replace -200 with NaN
df.replace(-200, np.nan, inplace=True)

# Features used for prediction
feature_columns = [
    "NOx(GT)",
    "NO2(GT)",
    "T",
    "RH",
    "PT08.S1(CO)",
    "C6H6(GT)"
]

# Keep CO for label creation
df = df[["CO(GT)"] + feature_columns]

# Fill missing values
df.fillna(df.mean(), inplace=True)

print("Shape after fixing missing values:", df.shape)

# Create Air Quality Label
def classify_air(co):
    if co <= 2:
        return "Good"
    elif co <= 5:
        return "Moderate"
    elif co <= 10:
        return "Unhealthy"
    else:
        return "Hazardous"

df["Air_Label"] = df["CO(GT)"].apply(classify_air)

# Encode labels
le = LabelEncoder()
df["Air_Label"] = le.fit_transform(df["Air_Label"])

# Define X and y
X = df[feature_columns]
y = df["Air_Label"]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ==============================
# Random Forest Model
# ==============================
rf_model = RandomForestClassifier(
    n_estimators=300,
    random_state=42
)

rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)

print("\nRandom Forest Results")
print("Accuracy:", accuracy_score(y_test, rf_pred))

# ==============================
# Confusion Matrix
# ==============================
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, rf_pred))

print("\nClassification Report:")
print(classification_report(y_test, rf_pred))

# ==============================
# Feature Importance Graph
# ==============================
importance = rf_model.feature_importances_

plt.figure()
plt.bar(feature_columns, importance)
plt.xticks(rotation=45)
plt.title("Feature Importance (Random Forest)")
plt.tight_layout()
plt.show()

# ==============================
# Save Model
# ==============================
with open("aqi_model.pkl", "wb") as f:
    pickle.dump(rf_model, f)

print("\nModel saved successfully!")