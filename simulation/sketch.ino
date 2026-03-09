#include "DHT.h"

#define DHTPIN 15
#define DHTTYPE DHT22

#define MQ135_PIN 34

#define LED_GOOD 18
#define LED_MODERATE 19
#define LED_UNHEALTHY 21
#define LED_HAZARD 22

DHT dht(DHTPIN, DHTTYPE);

float CO, NOx, NO2, benzene, pt08;

String classifyAQI(float co) {

  if (co <= 2) return "Good";
  else if (co <= 5) return "Moderate";
  else if (co <= 10) return "Unhealthy";
  else return "Hazardous";
}

void setup() {

  Serial.begin(115200);

  dht.begin();

  pinMode(LED_GOOD, OUTPUT);
  pinMode(LED_MODERATE, OUTPUT);
  pinMode(LED_UNHEALTHY, OUTPUT);
  pinMode(LED_HAZARD, OUTPUT);

}

void loop() {

  float temp = dht.readTemperature();
  float hum = dht.readHumidity();

  int gas_raw = analogRead(MQ135_PIN);

  CO = map(gas_raw, 0, 4095, 0, 15);
  NOx = map(gas_raw, 0, 4095, 0, 200);
  NO2 = map(gas_raw, 0, 4095, 0, 100);
  benzene = map(gas_raw, 0, 4095, 0, 20);
  pt08 = map(gas_raw, 0, 4095, 0, 1000);

  String category = classifyAQI(CO);

  digitalWrite(LED_GOOD, LOW);
  digitalWrite(LED_MODERATE, LOW);
  digitalWrite(LED_UNHEALTHY, LOW);
  digitalWrite(LED_HAZARD, LOW);

  if (category == "Good") digitalWrite(LED_GOOD, HIGH);
  if (category == "Moderate") digitalWrite(LED_MODERATE, HIGH);
  if (category == "Unhealthy") digitalWrite(LED_UNHEALTHY, HIGH);
  if (category == "Hazardous") digitalWrite(LED_HAZARD, HIGH);

  Serial.println("Air Quality Data:");

  Serial.print("Temperature (T): ");
  Serial.println(temp);

  Serial.print("Humidity (RH): ");
  Serial.println(hum);

  Serial.print("CO(GT): ");
  Serial.println(CO);

  Serial.print("NOx(GT): ");
  Serial.println(NOx);

  Serial.print("NO2(GT): ");
  Serial.println(NO2);

  Serial.print("C6H6(GT) Benzene: ");
  Serial.println(benzene);

  Serial.print("PT08.S1(CO): ");
  Serial.println(pt08);

  Serial.print("AQI Category: ");
  Serial.println(category);

  delay(3000);
}