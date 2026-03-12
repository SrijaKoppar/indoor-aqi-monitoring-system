"""
Model Training and Serialization Script

This script trains and saves your XGBoost and Random Forest models
for use in the FastAPI backend.

Usage:
    python train_models.py --data path/to/AirQualityUCI.csv
"""

import os
import pickle
import argparse
import logging
import pandas as pd
import numpy as np
from pathlib import Path

# Try to import sklearn and xgboost
try:
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import LabelEncoder
    from sklearn.metrics import accuracy_score, mean_absolute_error, mean_squared_error, r2_score
    from xgboost import XGBRegressor
    HAS_MODELS = True
except ImportError:
    HAS_MODELS = False
    print("⚠️  Warning: sklearn/xgboost not installed")
    print("Install with: pip install scikit-learn xgboost")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train_xgboost_model(df, output_dir):
    """Train XGBoost regressor for CO prediction"""
    if not HAS_MODELS:
        logger.error("sklearn/xgboost not installed")
        return None

    logger.info("🚀 Training XGBoost Regressor...")

    # Replace -200 with NaN
    df.replace(-200, np.nan, inplace=True)

    # Parse datetime
    df["Datetime"] = pd.to_datetime(
        df["Date"] + " " + df["Time"],
        format="%d/%m/%Y %H.%M.%S",
        errors="coerce",
    )

    # Sort chronologically
    df = df.sort_values("Datetime").reset_index(drop=True)

    feature_cols = [
        "CO(GT)",
        "NOx(GT)",
        "NO2(GT)",
        "T",
        "RH",
        "PT08.S1(CO)",
        "C6H6(GT)",
    ]
    df = df[["Datetime"] + feature_cols]

    # Fill missing values
    df[feature_cols] = df[feature_cols].ffill().fillna(df[feature_cols].mean())

    # Feature engineering
    LAG_HOURS = 3
    lag_df = df[feature_cols].copy()

    # Lag features
    for lag in range(1, LAG_HOURS + 1):
        for col in feature_cols:
            lag_df[f"{col}_lag{lag}"] = lag_df[col].shift(lag)

    # Rolling mean features
    for col in feature_cols:
        lag_df[f"{col}_rollmean3"] = lag_df[col].shift(1).rolling(3).mean()

    # Hour of day
    lag_df["hour"] = df["Datetime"].dt.hour

    # Target
    lag_df["CO_next_hour"] = lag_df["CO(GT)"].shift(-1)

    # Drop original columns and NaN
    lag_df = lag_df.drop(columns=feature_cols)
    lag_df = lag_df.dropna().reset_index(drop=True)

    logger.info(f"✓ Created {lag_df.shape[0]} samples with {lag_df.shape[1]} features")

    # Train/test split (chronological)
    split_idx = int(len(lag_df) * 0.8)
    X = lag_df.drop(columns=["CO_next_hour"])
    y = lag_df["CO_next_hour"]

    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    logger.info(f"✓ Train: {len(X_train)} | Test: {len(X_test)}")

    # Train model
    model = XGBRegressor(
        n_estimators=500,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1,
        verbosity=0,
    )

    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    logger.info(f"✓ XGBoost Results:")
    logger.info(f"  - MAE: {mae:.4f}")
    logger.info(f"  - RMSE: {rmse:.4f}")
    logger.info(f"  - R²: {r2:.4f}")

    # Save
    output_path = os.path.join(output_dir, "xgb_model.pkl")
    with open(output_path, "wb") as f:
        pickle.dump(model, f)
    logger.info(f"✓ Model saved to {output_path}")

    return model


def train_random_forest_model(df, output_dir):
    """Train Random Forest classifier for AQI categories"""
    if not HAS_MODELS:
        logger.error("sklearn not installed")
        return None

    logger.info("🚀 Training Random Forest Classifier...")

    # Replace -200 with NaN
    df.replace(-200, np.nan, inplace=True)

    feature_columns = [
        "NOx(GT)",
        "NO2(GT)",
        "T",
        "RH",
        "PT08.S1(CO)",
        "C6H6(GT)",
    ]

    df = df[["CO(GT)"] + feature_columns]
    df.fillna(df.mean(), inplace=True)

    # Create labels
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
    df["Air_Label_Encoded"] = le.fit_transform(df["Air_Label"])

    X = df[feature_columns]
    y = df["Air_Label_Encoded"]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train model
    model = RandomForestClassifier(n_estimators=300, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    logger.info(f"✓ Random Forest Results:")
    logger.info(f"  - Accuracy: {accuracy:.4f}")

    # Save model and encoder
    model_path = os.path.join(output_dir, "rf_model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    logger.info(f"✓ Model saved to {model_path}")

    le_path = os.path.join(output_dir, "label_encoder.pkl")
    with open(le_path, "wb") as f:
        pickle.dump(le, f)
    logger.info(f"✓ Label encoder saved to {le_path}")

    return model, le


def main():
    parser = argparse.ArgumentParser(description="Train and save ML models")
    parser.add_argument(
        "--data",
        type=str,
        default="AirQualityUCI.csv",
        help="Path to AirQualityUCI.csv dataset",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="./models_pickle",
        help="Output directory for model files",
    )

    args = parser.parse_args()

    # Create output directory
    output_dir = args.output
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    logger.info(f"📁 Output directory: {output_dir}")

    # Load data
    if not os.path.exists(args.data):
        logger.error(f"❌ Dataset not found: {args.data}")
        logger.info("Download from: https://archive.ics.uci.edu/dataset/360")
        return

    logger.info(f"📖 Loading data from {args.data}...")
    df = pd.read_csv(args.data, sep=";", decimal=",")
    df = df.iloc[:, :-2]  # Remove empty columns
    logger.info(f"✓ Loaded {df.shape[0]} rows, {df.shape[1]} columns")

    # Train models
    if HAS_MODELS:
        train_xgboost_model(df.copy(), output_dir)
        train_random_forest_model(df.copy(), output_dir)
        logger.info("✅ All models trained and saved!")
    else:
        logger.error(
            "❌ Cannot train models. Install dependencies: pip install scikit-learn xgboost"
        )


if __name__ == "__main__":
    main()
