const int pinIN3 = 22;
const int pinIN4 = 23;
const int pinENB = 2;

int ultimoComando = 0;
bool nuevoComandoRecibido = false;  // Bandera para detectar cambios

void setup() {
  pinMode(pinIN3, OUTPUT);
  pinMode(pinIN4, OUTPUT);
  pinMode(pinENB, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  while (Serial.available() > 0) {
    char comandoChar = Serial.read();  // Leer solo un carácter
    if (comandoChar >= '1' && comandoChar <= '3') {
      ultimoComando = comandoChar - '0';  // Convertir carácter a número
      nuevoComandoRecibido = true;
      Serial.print("Comando recibido: ");
      Serial.println(ultimoComando);
    }
  }

  if (nuevoComandoRecibido) {
    ejecutarMotor(ultimoComando);
    nuevoComandoRecibido = false;  // Resetea bandera para esperar nuevo comando
  }
}

void ejecutarMotor(int comando) {
  switch (comando) {
    case 1: 
      digitalWrite(pinIN3, HIGH);
      digitalWrite(pinIN4, LOW);
      analogWrite(pinENB, 100);
      break;
    case 2:  
      digitalWrite(pinIN3, HIGH);
      digitalWrite(pinIN4, LOW);
      analogWrite(pinENB, 255);
      break;
    case 3:  
      digitalWrite(pinIN3, LOW);
      digitalWrite(pinIN4, HIGH);
      analogWrite(pinENB, 250);
      break;
    default:  
      digitalWrite(pinIN3, LOW);
      digitalWrite(pinIN4, LOW);
      analogWrite(pinENB, 0);
      break;
  }
}
