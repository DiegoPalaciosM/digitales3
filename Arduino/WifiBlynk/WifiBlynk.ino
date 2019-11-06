#define BLYNK_PRINT Serial
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>

WiFiServer wifiServer(42777);
BlynkTimer timer;

char auth[] = "NMElketms1KxzbEPFSnWCUVyZ6oNFW1q";
char ssid[] = "";
char pass[] = "";

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
    Blynk.virtualWrite(V1, "update", 1, "L1", "Cerrado");
  }
  else if (comando == '1') {
    digitalWrite(L1, LOW);    // Activo L1
    Blynk.virtualWrite(V1, "update", 1, "L1", "Abierto");
  }
  if (comando == 'b') {
    digitalWrite(L2, HIGH);   // Desactivo L2
    Blynk.virtualWrite(V1, "update", 2, "L2", "Cerrado");
  }
  else if (comando == '2') {
    digitalWrite(L2, LOW);    // Activo L2
    Blynk.virtualWrite(V1, "update", 2, "L2", "Abierto");
  }
    if (comando == 'c') {
    digitalWrite(L3, HIGH);   // Desactivo L3
    Blynk.virtualWrite(V1, "update", 3, "L3", "Cerrado");
  }
  else if (comando == '3') {
    digitalWrite(L3, LOW);    // Activo L3
    Blynk.virtualWrite(V1, "update", 3, "L3", "Abierto");
  }
    if (comando == 'd') {
    digitalWrite(L4, HIGH);   // Desactivo L4
    Blynk.virtualWrite(V1, "update", 4, "L4", "Cerrado");
  }
  else if (comando == '4') {
    digitalWrite(L4, LOW);    // Activo L4
    Blynk.virtualWrite(V1, "update", 4, "L4", "Abierto");
  }
    if (comando == 'e') {
    digitalWrite(L5, HIGH);   // Desactivo L5
    Blynk.virtualWrite(V1, "update", 5, "L5", "Cerrado");
  }
  else if (comando == '5') {
    digitalWrite(L5, LOW);    // Activo L5
    Blynk.virtualWrite(V1, "update", 5, "L5", "Abierto");
  }
    if (comando == 'f') {
    digitalWrite(L6, HIGH);   // Desactivo L6
    Blynk.virtualWrite(V1, "update", 6, "L6", "Cerrado");
  }
  else if (comando == '6') {
    digitalWrite(L6, LOW);    // Activo L6
    Blynk.virtualWrite(V1, "update", 6, "L6", "Abierto");
  }
    if (comando == 'g') {
    digitalWrite(Automatizacion, HIGH);   // Desactivo Automatizacion
    Blynk.virtualWrite(V1, "update", 7, "Automatizacion", "Cerrado");
  }
  else if (comando == '7') {
    digitalWrite(Automatizacion, LOW);    // Activo Automatizacion
    Blynk.virtualWrite(V1, "update", 7, "Automatizacion", "Abierto");
  }

  return;
}

void setup() {

  Serial.begin(115200);
  delay(1000);
  WiFi.begin(ssid, pass);
  Blynk.begin(auth, ssid, pass);
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

  Blynk.virtualWrite(V1, "clr");
  Blynk.virtualWrite(V1, "add", 1, "L1", "Cerrado");
  Blynk.virtualWrite(V1, "add", 2, "L2", "Cerrado");
  Blynk.virtualWrite(V1, "add", 3, "L3", "Cerrado");
  Blynk.virtualWrite(V1, "add", 4, "L4", "Cerrado");
  Blynk.virtualWrite(V1, "add", 5, "L5", "Cerrado");
  Blynk.virtualWrite(V1, "add", 6, "L6", "Cerrado");
  Blynk.virtualWrite(V1, "add", 7, "Automatizacion", "Cerrado");
}

void loop() {
  Blynk.run();
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
