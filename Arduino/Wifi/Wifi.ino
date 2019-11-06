#include <ESP8266WiFi.h>
WiFiServer wifiServer(42777);
const char* ssid = "";
const char* password =  "";

int L1 = 16;
int L2 = 5;
int L3 = 4;
int L4 = 0;
int L5 = 14;
int L6 = 12;
int Automatizacion = 2;

void Accion(char comando) {

  if (comando == 'a') {
    digitalWrite(L1, HIGH);   // Desactivo L1
  }
  else if (comando == '1') {
    digitalWrite(L1, LOW);    // Activo L1
  }
  if (comando == 'b') {
    digitalWrite(L2, HIGH);   // Desactivo L2
  }
  else if (comando == '2') {
    digitalWrite(L2, LOW);    // Activo L2
  }
    if (comando == 'c') {
    digitalWrite(L3, HIGH);   // Desactivo L3
  }
  else if (comando == '3') {
    digitalWrite(L3, LOW);    // Activo L3
  }
    if (comando == 'd') {
    digitalWrite(L4, HIGH);   // Desactivo L4
  }
  else if (comando == '4') {
    digitalWrite(L4, LOW);    // Activo L4
  }
    if (comando == 'e') {
    digitalWrite(L5, HIGH);   // Desactivo L5
  }
  else if (comando == '5') {
    digitalWrite(L5, LOW);    // Activo L5
  }
    if (comando == 'f') {
    digitalWrite(L6, HIGH);   // Desactivo L6
  }
  else if (comando == '6') {
    digitalWrite(L6, LOW);    // Activo L6
  }
    if (comando == 'g') {
    digitalWrite(Automatizacion, HIGH);   // Desactivo Automatizacion
  }
  else if (comando == '7') {
    digitalWrite(Automatizacion, LOW);    // Activo Automatizacion
  }

  return;
}

void setup() {

  Serial.begin(115200);
  delay(1000);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println(".");
  }
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
  wifiServer.begin();
  pinMode(L1, OUTPUT);
  pinMode(L2, OUTPUT);
  pinMode(L3, OUTPUT);
  pinMode(L4, OUTPUT);
  pinMode(L5, OUTPUT);
  pinMode(L6, OUTPUT);
  pinMode(Automatizacion, OUTPUT);
  digitalWrite(L1, HIGH);
  digitalWrite(L2, HIGH);
  digitalWrite(L3, HIGH);
  digitalWrite(L4, HIGH);
  digitalWrite(L5, HIGH);
  digitalWrite(L6, HIGH);
  digitalWrite(Automatizacion, HIGH);
}

void loop() {
  WiFiClient client = wifiServer.available();
  if (client) {
    Serial.print("Conectado Desde: ");
    Serial.println(client.remoteIP());
    while (client.connected()) {
      while (client.available() > 0) {
        char c = client.read();
        Accion(c);
        Serial.write(c);
        Serial.println("");
      }
      delay(10);
    }
    client.stop();
    Serial.println("Desconectado");
  }
}
