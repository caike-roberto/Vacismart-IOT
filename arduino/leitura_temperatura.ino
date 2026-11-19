// VaciSmart - monitoramento de temperatura da caixa termica (prototipo)
// Sensor DS18B20 no pino 2, leitura enviada pela serial para o gateway.

#include <OneWire.h>
#include <DallasTemperature.h>

const int PINO_SENSOR = 2;

// Meta do projeto: 30000 ms (30 s).
// Nos testes do simulador usamos 5000 ms pra nao ficar esperando.
const unsigned long INTERVALO_MS = 5000;

OneWire oneWire(PINO_SENSOR);
DallasTemperature sensor(&oneWire);

void setup() {
  Serial.begin(9600);
  sensor.begin();
}

void loop() {
  sensor.requestTemperatures();
  float t = sensor.getTempCByIndex(0);

  // -127 e o valor que a biblioteca devolve quando o sensor nao responde
  if (t == DEVICE_DISCONNECTED_C) {
    Serial.println("ERRO_SENSOR");
  } else {
    Serial.println(t, 1);
  }

  delay(INTERVALO_MS);
}
