/*
 * Complete Medical Assistant Robot Sensor Test
 * ESP32 + DHT22 + MAX30102 + MLX90614 + HC-SR04 + HX711
 * Sends sensor data to Flask app via USB Serial
 */

#include <Wire.h>
#include <DHT.h>
#include <Adafruit_MLX90614.h>
#include "MAX30105.h"
#include "spo2_algorithm.h"
#include "HX711.h"
 
 // DHT22 setup
 #define DHT_PIN 4
 #define DHT_TYPE DHT22
 DHT dht(DHT_PIN, DHT_TYPE);
 
 // MLX90614 setup
 Adafruit_MLX90614 mlx = Adafruit_MLX90614();
 
 // MAX30102 setup
 MAX30105 particleSensor;
 
 // HC-SR04 setup
 #define TRIG_PIN 5
 #define ECHO_PIN 18
 
// HX711 setup
#define LOADCELL_DOUT_PIN 2
#define LOADCELL_SCK_PIN 3
HX711 scale;

// Variables for sensor readings
float temperature, humidity, bodyTemp, distance, weight;
int heartRate = 0;
int spo2 = 0;
bool validHR = false, validSPO2 = false;
 
 // MAX30102 variables
 uint32_t irBuffer[25];
 uint32_t redBuffer[25];
 int32_t bufferLength = 25;
 int32_t spo2Value;
 int8_t validSPO2Flag;
 int32_t heartRateValue;
 int8_t validHeartRateFlag;
 
void setup() {
  Serial.begin(115200);
  Serial.println("=== Medical Assistant Robot Sensor Test ===");
  Serial.println("Initializing all sensors...");
  
  // Initialize DHT22
  dht.begin();
  Serial.println("✓ DHT22 initialized");
   
   // Initialize MLX90614
   if (!mlx.begin()) {
     Serial.println("✗ MLX90614 failed - check wiring");
   } else {
     Serial.println("✓ MLX90614 initialized");
   }
   
   // Initialize MAX30102
   if (!particleSensor.begin()) {
     Serial.println("✗ MAX30102 failed - check wiring");
   } else {
     particleSensor.setup();
     particleSensor.setPulseAmplitudeRed(0x0A);
     particleSensor.setPulseAmplitudeGreen(0);
     Serial.println("✓ MAX30102 initialized");
   }
   
   // Initialize HC-SR04
   pinMode(TRIG_PIN, OUTPUT);
   pinMode(ECHO_PIN, INPUT);
   Serial.println("✓ HC-SR04 initialized");
   
   // Initialize HX711
   scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
   scale.set_scale(-7050); // Default calibration
   scale.tare();
   Serial.println("✓ HX711 initialized and tared");
   
   Serial.println("\nAll sensors ready!");
   Serial.println("Starting medical readings...");
   delay(2000);
 }
 
 void loop() {
   Serial.println("\n" + String("=").substring(0,50));
   Serial.println("    MEDICAL SENSOR READINGS");
   Serial.println(String("=").substring(0,50));
   
   // Read all sensors
   readEnvironmentalSensors();
   readBodyTemperature();
   readVitalSigns();
   readDistance();
   readWeight();
   
  // Medical assessment
  performMedicalAssessment();
  
  // Send data to Flask app via Serial
  sendSensorDataToSerial();
  
  Serial.println(String("=").substring(0,50));
  delay(5000);
}
 
 void readEnvironmentalSensors() {
   temperature = dht.readTemperature();
   humidity = dht.readHumidity();
   
   Serial.println("🌡️ ENVIRONMENTAL CONDITIONS:");
   if (!isnan(temperature) && !isnan(humidity)) {
     Serial.print("  Room Temp: ");
     Serial.print(temperature);
     Serial.println("°C");
     
     Serial.print("  Humidity: ");
     Serial.print(humidity);
     Serial.println("%");
     
     // Environment assessment
     if (temperature >= 20 && temperature <= 24 && humidity >= 40 && humidity <= 60) {
       Serial.println("  Status: OPTIMAL for medical use");
     } else {
       Serial.println("  Status: Suboptimal conditions");
     }
   } else {
     Serial.println("  Status: DHT22 reading failed");
   }
 }
 
 void readBodyTemperature() {
   bodyTemp = mlx.readObjectTempC();
   
   Serial.println("\n🌡️ BODY TEMPERATURE:");
   Serial.print("  Temperature: ");
   Serial.print(bodyTemp);
   Serial.println("°C");
   
   if (bodyTemp > 35.0 && bodyTemp < 42.0) {
     Serial.println("  Detection: Human body temperature");
     if (bodyTemp >= 37.5) {
       Serial.println("  🚨 ALERT: FEVER DETECTED!");
     } else if (bodyTemp >= 37.0) {
       Serial.println("  ⚠️ WARNING: Slightly elevated");
     } else {
       Serial.println("  ✓ Normal temperature");
     }
   } else {
     Serial.println("  Status: No body temperature detected");
   }
 }
 
 void readVitalSigns() {
   Serial.println("\n❤️ VITAL SIGNS:");
   
   // Quick reading for heart rate and SpO2
   bool fingerDetected = false;
   
   // Check if finger is present
   for (int i = 0; i < bufferLength; i++) {
     while (particleSensor.available() == false) {
       particleSensor.check();
     }
     redBuffer[i] = particleSensor.getRed();
     irBuffer[i] = particleSensor.getIR();
     particleSensor.nextSample();
     
     if (irBuffer[i] > 50000) {
       fingerDetected = true;
     }
   }
   
   if (fingerDetected) {
     maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength, redBuffer, &spo2Value, &validSPO2Flag, &heartRateValue, &validHeartRateFlag);
     
     if (validHeartRateFlag) {
       Serial.print("  Heart Rate: ");
       Serial.print(heartRateValue);
       Serial.println(" BPM");
       
       if (heartRateValue < 60) {
         Serial.println("  Status: LOW heart rate");
       } else if (heartRateValue > 100) {
         Serial.println("  Status: HIGH heart rate");
       } else {
         Serial.println("  Status: Normal heart rate");
       }
     } else {
       Serial.println("  Heart Rate: Invalid reading");
     }
     
     if (validSPO2Flag) {
       Serial.print("  SpO2: ");
       Serial.print(spo2Value);
       Serial.println("%");
       
       if (spo2Value < 95) {
         Serial.println("  🚨 ALERT: LOW oxygen saturation!");
       } else {
         Serial.println("  ✓ Normal oxygen saturation");
       }
     } else {
       Serial.println("  SpO2: Invalid reading");
     }
   } else {
     Serial.println("  Status: No finger detected on sensor");
     Serial.println("  Instruction: Place finger on MAX30102");
   }
 }
 
 void readDistance() {
   // Send ultrasonic pulse
   digitalWrite(TRIG_PIN, LOW);
   delayMicroseconds(2);
   digitalWrite(TRIG_PIN, HIGH);
   delayMicroseconds(10);
   digitalWrite(TRIG_PIN, LOW);
   
   // Read echo
   long duration = pulseIn(ECHO_PIN, HIGH);
   distance = duration * 0.034 / 2; // Convert to cm
   
   Serial.println("\n📏 DISTANCE MEASUREMENT:");
   Serial.print("  Distance: ");
   Serial.print(distance);
   Serial.println(" cm");
   
   if (distance < 10) {
     Serial.println("  Status: Very close - possible contact");
   } else if (distance < 50) {
     Serial.println("  Status: Patient in range");
   } else if (distance < 100) {
     Serial.println("  Status: Patient nearby");
   } else {
     Serial.println("  Status: No patient detected");
   }
 }
 
 void readWeight() {
   if (scale.is_ready()) {
     weight = scale.get_units(5); // Average of 5 readings
     
     Serial.println("\n⚖️ WEIGHT MEASUREMENT:");
     Serial.print("  Weight: ");
     Serial.print(abs(weight));
     Serial.println(" grams");
     
     float weightKg = abs(weight) / 1000.0;
     Serial.print("  Weight: ");
     Serial.print(weightKg);
     Serial.println(" kg");
     
     if (weightKg > 30 && weightKg < 200) {
       Serial.println("  Detection: Possible patient weight");
       if (weightKg < 50) {
         Serial.println("  Category: Underweight range");
       } else if (weightKg < 80) {
         Serial.println("  Category: Normal weight range");
       } else {
         Serial.println("  Category: Overweight range");
       }
     } else if (abs(weight) > 100) {
       Serial.println("  Detection: Object on scale");
     } else {
       Serial.println("  Status: No weight detected");
     }
   } else {
     Serial.println("\n⚖️ WEIGHT: Scale not ready");
   }
 }
 
void performMedicalAssessment() {
  Serial.println("\n🏥 MEDICAL ASSESSMENT:");
  
  bool environmentOK = (temperature >= 20 && temperature <= 24 && humidity >= 40 && humidity <= 60);
  bool temperatureOK = (bodyTemp >= 36.0 && bodyTemp <= 37.4);
  bool patientPresent = (distance < 100);
  
  Serial.println("  Environmental Conditions: " + String(environmentOK ? "GOOD" : "NEEDS ATTENTION"));
  Serial.println("  Patient Temperature: " + String(temperatureOK ? "NORMAL" : "CHECK REQUIRED"));
  Serial.println("  Patient Presence: " + String(patientPresent ? "DETECTED" : "NOT DETECTED"));
  
  if (environmentOK && temperatureOK && patientPresent) {
    Serial.println("  🟢 OVERALL STATUS: All systems normal");
  } else {
    Serial.println("  🟡 OVERALL STATUS: Attention required");
  }
}

void sendSensorDataToSerial() {
  // Send structured data to Flask app via Serial
  // Format: SENSOR_DATA:heart_rate,spo2,body_temp,env_temp,humidity,distance,weight,timestamp
  
  Serial.println("\n📡 SENDING DATA TO FLASK APP:");
  
  // Create structured data string
  String sensorData = "SENSOR_DATA:";
  sensorData += String(validHeartRateFlag ? heartRateValue : 0) + ",";
  sensorData += String(validSPO2Flag ? spo2Value : 0) + ",";
  sensorData += String(bodyTemp, 2) + ",";
  sensorData += String(temperature, 2) + ",";
  sensorData += String(humidity, 2) + ",";
  sensorData += String(distance, 2) + ",";
  sensorData += String(abs(weight), 2) + ",";
  sensorData += String(millis());
  
  // Send the data
  Serial.println(sensorData);
  
  Serial.println("  ✓ Data sent via Serial");
  Serial.println("  Format: SENSOR_DATA:heart_rate,spo2,body_temp,env_temp,humidity,distance,weight,timestamp");
}
 
 /*
  * COMPLETE WIRING GUIDE:
  * 
  * DHT22:
  * VCC -> 3.3V, GND -> GND, DATA -> GPIO 4
  * 
  * MLX90614:
  * VIN -> 3.3V, GND -> GND, SCL -> GPIO 22, SDA -> GPIO 21
  * 
  * MAX30102:
  * VIN -> 3.3V, GND -> GND, SCL -> GPIO 22, SDA -> GPIO 21
  * 
  * HC-SR04:
  * VCC -> 5V, GND -> GND, TRIG -> GPIO 5, ECHO -> GPIO 18
  * 
  * HX711:
  * VCC -> 3.3V, GND -> GND, DOUT -> GPIO 2, SCK -> GPIO 3
  * 
  * REQUIRED LIBRARIES:
  * - DHT sensor library
  * - Adafruit MLX90614
  * - MAX30105 library
  * - SparkFun MAX3010x library
  * - HX711 Arduino Library
  * 
  * OPERATION:
  * 1. Monitor environmental conditions continuously
  * 2. Detect patient presence with ultrasonic sensor
  * 3. Measure body temperature when patient approaches
  * 4. Monitor vital signs when finger placed on sensor
  * 5. Track weight measurements on scale
  * 6. Provide comprehensive medical assessment
  */