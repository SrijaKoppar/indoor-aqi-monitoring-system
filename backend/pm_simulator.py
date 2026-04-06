"""
PM Sensor Simulator
===================
Generates realistic PM2.5 and PM10 values when a physical
PMS5003 sensor is not available.

The simulation is physics-inspired:
  - PM2.5 correlates positively with CO concentration
  - PM2.5 correlates negatively with relative humidity (hygroscopic effects)
  - Time-of-day patterns (higher during cooking/traffic hours)
  - Gaussian noise to simulate natural sensor variation

PM10 is derived from PM2.5 using a realistic indoor ratio (1.4x–1.8x).

This module is used ONLY for display/dashboard purposes.
The XGBoost model does not use PM data as input — the UCI
dataset does not contain PM columns.
"""

import numpy as np
from datetime import datetime
import math


class PMSimulator:
    """
    Simulates PM2.5 and PM10 sensor readings based on
    correlated environmental parameters.
    """

    # Typical indoor PM2.5 baseline range (µg/m³)
    # WHO guideline: 15 µg/m³ (24-hr mean)
    PM25_BASELINE_MIN = 8.0
    PM25_BASELINE_MAX = 20.0

    # PM10 / PM2.5 ratio for indoor environments
    PM10_RATIO_MIN = 1.4
    PM10_RATIO_MAX = 1.8

    # Hours considered "high activity" (cooking, traffic peaks)
    HIGH_ACTIVITY_HOURS = [7, 8, 12, 13, 18, 19, 20]

    def __init__(self, seed: int = None):
        """
        seed: optional random seed for reproducibility in testing
        """
        self.rng = np.random.default_rng(seed)
        self._last_pm25 = 12.0   # track last value for smoothing
        self._last_pm10 = 18.0

    def simulate(
        self,
        co_concentration: float,
        temperature: float,
        relative_humidity: float,
        hour: int = None
    ) -> dict:
        """
        Generate simulated PM2.5 and PM10 values.

        Parameters:
            co_concentration (float): CO in mg/m³ (from MQ-135 or model input)
            temperature      (float): Temperature in °C (from DHT22)
            relative_humidity(float): RH in % (from DHT22)
            hour             (int):   Hour of day 0–23. Uses current time if None.

        Returns:
            dict with keys:
                pm25        (float): PM2.5 in µg/m³
                pm10        (float): PM10  in µg/m³
                pm25_category (str): WHO-based category
                pm10_category (str): WHO-based category
                simulated   (bool):  Always True — flag for frontend
        """
        if hour is None:
            hour = datetime.now().hour

        # ── Base PM2.5 ──────────────────────────────────────────
        base = self.rng.uniform(self.PM25_BASELINE_MIN, self.PM25_BASELINE_MAX)

        # ── CO influence ────────────────────────────────────────
        # CO and PM2.5 share common sources (combustion, traffic)
        # CO > 2 mg/m³ indicates active pollution — boost PM
        co_factor = 1.0 + max(0, (co_concentration - 2.0) * 2.5)

        # ── Humidity dampening ──────────────────────────────────
        # High humidity causes particle agglomeration → lower count
        # Low humidity → more dry particles suspended
        rh_factor = 1.0 + (50.0 - relative_humidity) * 0.008
        rh_factor = np.clip(rh_factor, 0.7, 1.4)

        # ── Temperature influence ────────────────────────────────
        # Higher temperature → more volatile compounds → slightly higher PM
        temp_factor = 1.0 + max(0, (temperature - 20.0) * 0.015)

        # ── Time-of-day pattern ──────────────────────────────────
        # Peak hours: morning commute, lunch, evening cooking
        hour_factor = 1.4 if hour in self.HIGH_ACTIVITY_HOURS else 1.0
        # Smooth the peak with a sinusoidal envelope
        sin_pattern = 1.0 + 0.15 * math.sin(math.pi * hour / 12.0)
        time_factor = hour_factor * sin_pattern

        # ── Gaussian noise ───────────────────────────────────────
        noise = self.rng.normal(0, 1.2)

        # ── Final PM2.5 ──────────────────────────────────────────
        pm25_raw = base * co_factor * rh_factor * temp_factor * time_factor + noise

        # Smooth with previous reading (exponential moving average)
        pm25 = 0.7 * pm25_raw + 0.3 * self._last_pm25
        pm25 = float(np.clip(pm25, 2.0, 150.0))
        self._last_pm25 = pm25

        # ── PM10 from PM2.5 ratio ────────────────────────────────
        ratio = self.rng.uniform(self.PM10_RATIO_MIN, self.PM10_RATIO_MAX)
        pm10  = float(np.clip(pm25 * ratio, pm25, 250.0))
        self._last_pm10 = pm10

        return {
            "pm25"          : round(pm25, 1),
            "pm10"          : round(pm10, 1),
            "pm25_category" : self._classify_pm25(pm25),
            "pm10_category" : self._classify_pm10(pm10),
            "simulated"     : True
        }

    @staticmethod
    def _classify_pm25(pm25: float) -> str:
        """WHO 2021 PM2.5 24-hour guideline categories"""
        if pm25 <= 15:
            return "Good"
        elif pm25 <= 35:
            return "Moderate"
        elif pm25 <= 75:
            return "Unhealthy"
        else:
            return "Hazardous"

    @staticmethod
    def _classify_pm10(pm10: float) -> str:
        """WHO 2021 PM10 24-hour guideline categories"""
        if pm10 <= 45:
            return "Good"
        elif pm10 <= 75:
            return "Moderate"
        elif pm10 <= 150:
            return "Unhealthy"
        else:
            return "Hazardous"


# ── Singleton instance for FastAPI app ──────────────────────
# Import this in main.py:
#   from pm_simulator import pm_simulator
#   result = pm_simulator.simulate(co_gt, temperature, rh)
pm_simulator = PMSimulator()


# ── Quick test ───────────────────────────────────────────────
if __name__ == "__main__":
    sim = PMSimulator(seed=42)

    print("PM Simulator — Test Run")
    print("-" * 45)
    print(f"{'Scenario':<25} {'PM2.5':>7} {'PM10':>7} {'Category'}")
    print("-" * 45)

    test_cases = [
        ("Good air (CO=1.0)",   1.0,  22.0, 55.0, 14),
        ("Moderate (CO=3.5)",   3.5,  25.0, 50.0, 18),
        ("Cooking hour",        4.0,  28.0, 45.0, 19),
        ("Unhealthy (CO=7.0)",  7.0,  30.0, 35.0, 20),
        ("Hazardous (CO=12.0)", 12.0, 32.0, 25.0, 8),
    ]

    for name, co, temp, rh, hour in test_cases:
        result = sim.simulate(co, temp, rh, hour)
        print(f"{name:<25} {result['pm25']:>7.1f} {result['pm10']:>7.1f}  {result['pm25_category']}")
