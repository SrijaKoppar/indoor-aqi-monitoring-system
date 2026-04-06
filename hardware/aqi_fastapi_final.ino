/*
 * IoT AQI Monitor — ESP8266 + FastAPI Integration
 * Sensors : MQ-2, MQ-7, MQ-135, LCD 16x2
 * Simulated: Temperature, Humidity, PM2.5, PM10
 *
 * Libraries required:
 *   - LiquidCrystal_I2C by Frank de Brabander
 *   - ArduinoJson       by Benoit Blanchon
 */

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// ============================================================
// CONFIGURATION — UPDATE THESE
// ============================================================
const char* WIFI_SSID     = "Srija's OnePlus";
const char* WIFI_PASSWORD = "srij1375";
const char* SERVER_IP     = "10.121.97.96";   // your laptop IP
const int   SERVER_PORT   = 8080;

// ============================================================
// PIN DEFINITIONS
// ============================================================
#define MQ2_PIN    D5
#define MQ7_PIN    D6
#define MQ135_PIN  A0

#define MQ135_CO_MAX   12.0
#define MQ135_ADC_MAX  1023.0

// Placeholder values for fields model needs but we can't measure
#define DEFAULT_NOX     120.0
#define DEFAULT_NO2      60.0
#define DEFAULT_PT08S1  1050.0
#define DEFAULT_C6H6      4.8

// ============================================================
// OBJECTS
// ============================================================
LiquidCrystal_I2C lcd(0x27, 16, 2);
WiFiClient wifiClient;

// ============================================================
// SIMULATION STATE
// ============================================================
float lastTemp     = 25.0;
float lastHumidity = 55.0;
float lastPM25     = 12.0;
float lastPM10     = 18.0;

// ============================================================
// STRUCTS
// ============================================================
struct EnvReading {
  float temperature;
  float humidity;
};

struct PMReading {
  float pm25;
  float pm10;
  String category;
};

struct PredictionResult {
  String aqiCategory;
  String predictedCategory;
  float  predictedCO;
  float  pm25;
  float  pm10;
  String pm25Category;
  bool   success;
};

// ============================================================
// TEMPERATURE + HUMIDITY SIMULATOR
// ============================================================
EnvReading simulateEnvironment() {
  EnvReading env;

  float timeOfDay = fmod((float)millis() / 3600000.0, 24.0);
  float baseTemp  = 22.0 + 4.0 * sin(PI * (timeOfDay - 6.0) / 12.0);
  float tempNoise = ((float)(millis() % 100) / 100.0 - 0.5) * 0.6;

  env.temperature = 0.8 * (baseTemp + tempNoise) + 0.2 * lastTemp;
  env.temperature = constrain(env.temperature, 18.0, 34.0);
  lastTemp = env.temperature;

  float baseHumidity = 70.0 - (env.temperature - 18.0) * 1.2;
  float humNoise     = ((float)(millis() % 73) / 73.0 - 0.5) * 2.0;

  env.humidity = 0.8 * (baseHumidity + humNoise) + 0.2 * lastHumidity;
  env.humidity = constrain(env.humidity, 30.0, 80.0);
  lastHumidity = env.humidity;

  return env;
}

// ============================================================
// PM SIMULATOR
// ============================================================
PMReading simulatePM(float co, float temperature, float humidity) {
  PMReading pm;

  float base      = 8.0 + fmod((float)millis() / 1000.0, 12.0);
  float coFactor  = 1.0 + max(0.0f, (co - 2.0f) * 2.5f);
  float rhFactor  = constrain(1.0 + (50.0 - humidity) * 0.008, 0.7, 1.4);
  float tmpFactor = 1.0 + max(0.0f, (temperature - 20.0f) * 0.015f);
  float noise     = ((float)(millis() % 100) / 100.0 - 0.5) * 2.4;

  pm.pm25 = constrain(0.7 * (base * coFactor * rhFactor * tmpFactor + noise) + 0.3 * lastPM25, 2.0, 150.0);
  lastPM25 = pm.pm25;

  pm.pm10 = constrain(pm.pm25 * 1.6, pm.pm25, 250.0);
  lastPM10 = pm.pm10;

  if (pm.pm25 <= 15)       pm.category = "Good";
  else if (pm.pm25 <= 35)  pm.category = "Moderate";
  else if (pm.pm25 <= 75)  pm.category = "Unhealthy";
  else                     pm.category = "Hazardous";

  return pm;
}

// ============================================================
// AQI CLASSIFICATION (local fallback)
// ============================================================
String classifyAQI(float co) {
  if (co <= 2)        return "Good";
  else if (co <= 5)   return "Moderate";
  else if (co <= 10)  return "Unhealthy";
  else                return "Hazardous";
}

// ============================================================
// PING FASTAPI SERVER
// ============================================================
void pingServer() {
  HTTPClient http;
  String url = "http://" + String(SERVER_IP) + ":" + SERVER_PORT + "/health";
  http.begin(wifiClient, url);

  Serial.println("[INFO] Pinging FastAPI server...");
  int code = http.GET();

  if (code == 200) {
    Serial.println("[OK] FastAPI server reachable!");
    lcd.clear();
    lcd.setCursor(0, 0); lcd.print("Server OK!");
    delay(1500);
  } else {
    Serial.printf("[WARN] Server ping failed (HTTP %d)\n", code);
    lcd.clear();
    lcd.setCursor(0, 0); lcd.print("Server offline");
    lcd.setCursor(0, 1); lcd.print("Using local sim");
    delay(2000);
  }
  http.end();
}

// ============================================================
// SEND TO FASTAPI — matches PredictionRequest schema exactly
// ============================================================
PredictionResult sendToFastAPI(float co_gt, float temperature, float humidity) {
  PredictionResult result = {"N/A", "N/A", 0.0, 0.0, 0.0, "N/A", false};

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("[WARN] WiFi disconnected, using local classification");
    return result;
  }

  HTTPClient http;
  String url = "http://" + String(SERVER_IP) + ":" + SERVER_PORT + "/api/predict";
  http.begin(wifiClient, url);
  http.addHeader("Content-Type", "application/json");
  http.setTimeout(8000);

  // Build JSON body matching PredictionRequest in schemas.py
  StaticJsonDocument<256> reqDoc;
  reqDoc["co_gt"]             = co_gt;
  reqDoc["nox_gt"]            = DEFAULT_NOX;
  reqDoc["no2_gt"]            = DEFAULT_NO2;
  reqDoc["temperature"]       = temperature;
  reqDoc["relative_humidity"] = humidity;
  reqDoc["pt08_s1_co"]        = DEFAULT_PT08S1;
  reqDoc["c6h6_gt"]           = DEFAULT_C6H6;

  String payload;
  serializeJson(reqDoc, payload);
  Serial.println("[POST] /api/predict → " + payload);

  int httpCode = http.POST(payload);

  if (httpCode == 200) {
    String response = http.getString();
    Serial.println("[RESP] " + response);

    // Parse response matching PredictionResponse in schemas.py
    StaticJsonDocument<1024> respDoc;
    if (!deserializeJson(respDoc, response)) {
      result.aqiCategory       = respDoc["aqi_category"].as<String>();
      result.predictedCategory = respDoc["predicted_category"].as<String>();
      result.predictedCO       = respDoc["co_concentration_next_hour"].as<float>();
      // PM from backend pm_simulator.py (if available)
      result.pm25              = respDoc["pm25"].as<float>();
      result.pm10              = respDoc["pm10"].as<float>();
      result.pm25Category      = respDoc["pm25_category"].as<String>();
      result.success           = true;
      Serial.printf("[OK] AQI: %s | Predicted: %s | CO next hr: %.2f\n",
        result.aqiCategory.c_str(),
        result.predictedCategory.c_str(),
        result.predictedCO
      );
    } else {
      Serial.println("[ERROR] Failed to parse response JSON");
    }
  } else {
    Serial.printf("[ERROR] HTTP %d from FastAPI\n", httpCode);
  }

  http.end();
  return result;
}

// ============================================================
// SETUP
// ============================================================
void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("=============================");
  Serial.println(" IoT AQI Monitor + FastAPI");
  Serial.println(" Temp + PM: Simulated");
  Serial.println("=============================");

  pinMode(MQ2_PIN, INPUT);
  pinMode(MQ7_PIN, INPUT);

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0); lcd.print("AQI Monitor");
  lcd.setCursor(0, 1); lcd.print("Connecting...");

  // Connect to Wi-Fi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.printf("Connecting to %s", WIFI_SSID);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 30) {
    delay(500); Serial.print("."); attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[OK] WiFi Connected: " + WiFi.localIP().toString());
    lcd.clear();
    lcd.setCursor(0, 0); lcd.print("WiFi OK!");
    lcd.setCursor(0, 1); lcd.print(WiFi.localIP());
    delay(2000);
    pingServer();
  } else {
    Serial.println("\n[WARN] WiFi failed. Running in offline mode.");
    lcd.clear();
    lcd.setCursor(0, 0); lcd.print("WiFi Failed");
    lcd.setCursor(0, 1); lcd.print("Offline mode");
    delay(2000);
  }

  // Warm up MQ sensors
  lcd.clear();
  lcd.setCursor(0, 0); lcd.print("Warming up...");
  lcd.setCursor(0, 1); lcd.print("10 seconds...");
  Serial.println("Warming up MQ sensors...");
  delay(10000); // use 120000 in production

  lcd.clear();
  Serial.println("Ready!\n");
}

// ============================================================
// LOOP
// ============================================================
void loop() {

  // --- Real sensors ---
  bool  smokeDetected = (digitalRead(MQ2_PIN) == LOW);
  bool  coDetected    = (digitalRead(MQ7_PIN) == LOW);
  int   mq135Raw      = analogRead(MQ135_PIN);
  float co_gt         = constrain(
    (mq135Raw / MQ135_ADC_MAX) * MQ135_CO_MAX, 0.0, MQ135_CO_MAX
  );

  // --- Simulated sensors ---
  EnvReading env = simulateEnvironment();
  PMReading  pm  = simulatePM(co_gt, env.temperature, env.humidity);

  // --- Send to FastAPI ---
  PredictionResult pred = sendToFastAPI(co_gt, env.temperature, env.humidity);

  // Use server PM if available, local simulation as fallback
  float  displayPM25    = pred.success ? pred.pm25        : pm.pm25;
  float  displayPM10    = pred.success ? pred.pm10        : pm.pm10;
  String displayPM25Cat = pred.success ? pred.pm25Category: pm.category;
  String aqiNow         = pred.success ? pred.aqiCategory : classifyAQI(co_gt);
  String aqiNext        = pred.success ? pred.predictedCategory : "---";

  // --- Serial Monitor ---
  Serial.println("-----------------------------");
  Serial.print("MQ-2  (Smoke):     "); Serial.println(smokeDetected ? "DETECTED!" : "Clean");
  Serial.print("MQ-7  (CO):        "); Serial.println(coDetected    ? "DETECTED!" : "Clean");
  Serial.print("MQ-135 Raw:        "); Serial.println(mq135Raw);
  Serial.print("CO Concentration:  "); Serial.print(co_gt, 2);           Serial.println(" mg/m3");
  Serial.print("AQI Now:           "); Serial.println(aqiNow);
  Serial.print("AQI Next Hour:     "); Serial.println(aqiNext);
  Serial.print("Temp  [simulated]: "); Serial.print(env.temperature, 1);  Serial.println(" C");
  Serial.print("Humid [simulated]: "); Serial.print(env.humidity, 1);     Serial.println(" %");
  Serial.print("PM2.5 [simulated]: "); Serial.print(displayPM25, 1);      Serial.println(" ug/m3");
  Serial.print("PM10  [simulated]: "); Serial.print(displayPM10, 1);      Serial.println(" ug/m3");
  Serial.print("Server used:       "); Serial.println(pred.success ? "Yes" : "No (offline)");
  Serial.println("-----------------------------\n");

  // --- LCD Screen 1: Current AQI + Predicted AQI ---
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Now: "); lcd.print(aqiNow);
  lcd.setCursor(0, 1);
  lcd.print("1hr: "); lcd.print(aqiNext);
  delay(3000);

  // --- LCD Screen 2: Gas alerts + CO ---
  lcd.clear();
  lcd.setCursor(0, 0);
  if (smokeDetected)   lcd.print("! Smoke Detected");
  else if (coDetected) lcd.print("! CO Detected   ");
  else                 lcd.print("Gas: Clean      ");
  lcd.setCursor(0, 1);
  lcd.print("CO:"); lcd.print(co_gt, 2); lcd.print(" mg/m3");
  delay(3000);

  // --- LCD Screen 3: Simulated Temp + Humidity ---
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("T:"); lcd.print(env.temperature, 1); lcd.print("C [sim]");
  lcd.setCursor(0, 1);
  lcd.print("RH:"); lcd.print(env.humidity, 1); lcd.print("% [sim]");
  delay(3000);

  // --- LCD Screen 4: Simulated PM ---
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("PM2.5:"); lcd.print(displayPM25, 1); lcd.print("[sim]");
  lcd.setCursor(0, 1);
  lcd.print("PM10: "); lcd.print(displayPM10, 1); lcd.print("[sim]");
  delay(3000);
}
