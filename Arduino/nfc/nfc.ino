#include <MFRC522.h>
#include <SPI.h>

#define RST_PIN  9
#define SS_PIN  10
MFRC522 NFC(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(9600);
  SPI.begin();
  NFC.PCD_Init();
}

byte ActualID[4];

void loop() {
  if ( NFC.PICC_IsNewCardPresent()) {
    if ( NFC.PICC_ReadCardSerial()) {
      for (byte i = 0; i <  4; i++) {
        ActualID[i] = NFC.uid.uidByte[i];
      }
      String ID0 = String(ActualID[0]);
      String ID1 = String(ActualID[1]);
      String ID2 = String(ActualID[2]);
      String ID3 = String(ActualID[3]);
      String ID = "A" + ID0 + ID1 + ID2 + ID3 + "A";
      Serial.println(ID);
    }
  }
}
