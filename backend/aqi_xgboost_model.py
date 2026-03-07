import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ============================================================
# STEP 1 — LOAD & CLEAN DATA
# ============================================================
print("Loading dataset...")
df = pd.read_csv("AirQualityUCI.csv", sep=';', decimal=',')

# Drop last two empty columns
df = df.iloc[:, :-2]

# Replace -200 (faulty sensor readings) with NaN
df.replace(-200, np.nan, inplace=True)

# Parse datetime
df['Datetime'] = pd.to_datetime(
    df['Date'] + ' ' + df['Time'],
    format='%d/%m/%Y %H.%M.%S',
    errors='coerce'
)

# Sort chronologically — critical for time series
df = df.sort_values('Datetime').reset_index(drop=True)

# Keep relevant columns
feature_cols = ['CO(GT)', 'NOx(GT)', 'NO2(GT)', 'T', 'RH', 'PT08.S1(CO)', 'C6H6(GT)']
df = df[['Datetime'] + feature_cols]

# Fill missing values
df[feature_cols] = df[feature_cols].ffill().fillna(df[feature_cols].mean())
print(f"Data loaded: {df.shape[0]} hourly records")

# ============================================================
# STEP 2 — FEATURE ENGINEERING
# ============================================================
LAG_HOURS = 3

print(f"\nCreating lag features (past {LAG_HOURS} hours)...")

lag_df = df[feature_cols].copy()

# Lag features — past 3 hours of all sensors
for lag in range(1, LAG_HOURS + 1):
    for col in feature_cols:
        lag_df[f'{col}_lag{lag}'] = lag_df[col].shift(lag)

# Rolling mean features — smoothed trend over last 3 hours
for col in feature_cols:
    lag_df[f'{col}_rollmean3'] = lag_df[col].shift(1).rolling(3).mean()

# Hour of day — XGBoost can exploit daily patterns (morning rush, cooking hours, etc.)
lag_df['hour'] = df['Datetime'].dt.hour

# Target: CO value 1 hour ahead
lag_df['CO_next_hour'] = lag_df['CO(GT)'].shift(-1)

# Drop original (non-lagged) columns
lag_df = lag_df.drop(columns=feature_cols)

# Drop rows with NaN
lag_df = lag_df.dropna().reset_index(drop=True)

print(f"Feature matrix shape: {lag_df.shape}")

# ============================================================
# STEP 3 — CHRONOLOGICAL TRAIN/TEST SPLIT
# ============================================================
split_idx = int(len(lag_df) * 0.8)

X = lag_df.drop(columns=['CO_next_hour'])
y = lag_df['CO_next_hour']

X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

print(f"\nTrain size: {len(X_train)} | Test size: {len(X_test)}")

# ============================================================
# STEP 4 — TRAIN XGBOOST REGRESSOR
# ============================================================
print("\nTraining XGBoost Regressor...")

xgb_model = XGBRegressor(
    n_estimators=500,       # number of trees
    learning_rate=0.05,     # smaller = more careful learning
    max_depth=6,            # tree depth — controls complexity
    subsample=0.8,          # use 80% of rows per tree (reduces overfitting)
    colsample_bytree=0.8,   # use 80% of features per tree
    random_state=42,
    n_jobs=-1,
    verbosity=0
)

xgb_model.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=False
)

y_pred = xgb_model.predict(X_test)

# ============================================================
# STEP 5 — EVALUATE REGRESSION PERFORMANCE
# ============================================================
mae  = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2   = r2_score(y_test, y_pred)

print("\n--- XGBoost Regression Results ---")
print(f"MAE  (Mean Absolute Error):      {mae:.4f}  mg/m³")
print(f"RMSE (Root Mean Squared Error):  {rmse:.4f} mg/m³")
print(f"R²   (Variance Explained):       {r2:.4f}")

# ============================================================
# STEP 6 — CONVERT PREDICTED CO → AQI CATEGORY
# ============================================================
def classify_aqi(co):
    if co <= 2:
        return "Good"
    elif co <= 5:
        return "Moderate"
    elif co <= 10:
        return "Unhealthy"
    else:
        return "Hazardous"

predicted_labels = [classify_aqi(v) for v in y_pred]
actual_labels    = [classify_aqi(v) for v in y_test]

category_accuracy = np.mean(
    [p == a for p, a in zip(predicted_labels, actual_labels)]
)

print(f"\n--- AQI Category Results ---")
print(f"Category Accuracy: {category_accuracy * 100:.2f}%")

from collections import Counter
print("\nPredicted AQI distribution:")
for cat, count in Counter(predicted_labels).most_common():
    print(f"  {cat}: {count} hours")

# ============================================================
# STEP 7 — VISUALIZATIONS
# ============================================================

# --- Plot 1: Actual vs Predicted CO ---
plt.figure(figsize=(12, 4))
plt.plot(y_test.values[:200], label='Actual CO', color='steelblue', linewidth=1.5)
plt.plot(y_pred[:200],        label='XGBoost Predicted CO', color='tomato', linestyle='--', linewidth=1.5)
plt.title("XGBoost — Actual vs Predicted CO Next Hour (First 200 Test Points)")
plt.xlabel("Time Steps (hours)")
plt.ylabel("CO Concentration (mg/m³)")
plt.legend()
plt.tight_layout()
plt.savefig("xgb_actual_vs_predicted.png", dpi=150)
plt.show()
print("\nSaved: xgb_actual_vs_predicted.png")

# --- Plot 2: Top 15 Feature Importances ---
importances = xgb_model.feature_importances_
feat_names  = X.columns.tolist()

top_n   = 15
indices = np.argsort(importances)[::-1][:top_n]

plt.figure(figsize=(11, 5))
plt.bar(range(top_n), importances[indices], color='steelblue')
plt.xticks(range(top_n), [feat_names[i] for i in indices], rotation=45, ha='right')
plt.title("Top 15 Feature Importances (XGBoost Regressor)")
plt.tight_layout()
plt.savefig("xgb_feature_importance.png", dpi=150)
plt.show()
print("Saved: xgb_feature_importance.png")

# --- Plot 3: Scatter — Actual vs Predicted ---
plt.figure(figsize=(6, 6))
plt.scatter(y_test, y_pred, alpha=0.3, color='steelblue', s=10)
plt.plot([y_test.min(), y_test.max()],
         [y_test.min(), y_test.max()],
         color='tomato', linestyle='--', linewidth=2, label='Perfect Prediction')
plt.xlabel("Actual CO (mg/m³)")
plt.ylabel("Predicted CO (mg/m³)")
plt.title("Actual vs Predicted — Scatter Plot")
plt.legend()
plt.tight_layout()
plt.savefig("xgb_scatter.png", dpi=150)
plt.show()
print("Saved: xgb_scatter.png")

# --- Plot 4: Predicted AQI Category Distribution ---
from collections import Counter
categories = ["Good", "Moderate", "Unhealthy", "Hazardous"]
colors     = ["green", "gold", "orange", "red"]

pred_counts   = Counter(predicted_labels)
actual_counts = Counter(actual_labels)

x = np.arange(len(categories))
width = 0.35

fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(x - width/2, [actual_counts.get(c, 0) for c in categories],
       width, label='Actual', color=colors, alpha=0.6)
ax.bar(x + width/2, [pred_counts.get(c, 0) for c in categories],
       width, label='Predicted', color=colors, alpha=1.0)
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.set_title("AQI Category Distribution — Actual vs Predicted")
ax.set_ylabel("Number of Hours")
ax.legend()
plt.tight_layout()
plt.savefig("xgb_category_distribution.png", dpi=150)
plt.show()
print("Saved: xgb_category_distribution.png")

# ============================================================
# STEP 8 — SAVE MODEL
# ============================================================
with open("aqi_xgboost_model.pkl", "wb") as f:
    pickle.dump(xgb_model, f)

print("\nModel saved as: aqi_xgboost_model.pkl")
print("\nDone! Your XGBoost prediction model is ready.")
