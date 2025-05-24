const int pinIN3 = 22;  // Pin de dirección del motor
const int pinIN4 = 23;  // Pin de dirección del motor
const int pinENB = 2;   // ¡Debe ser PWM para el control de velocidad!

int ultimoComando = 0;  // Guarda el último comando recibido

void setup() {
  pinMode(pinIN3, OUTPUT);
  pinMode(pinIN4, OUTPUT);
  pinMode(pinENB, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String comandoStr = Serial.readStringUntil('\n');  // Leer línea completa
    int comando = comandoStr.toInt();  // Convertir a número

    if (comando >= 1 && comando <= 3) {  // Validación del comando
      ultimoComando = comando;
      Serial.print("Comando recibido y ejecutando: ");
      Serial.println(ultimoComando);
    } else {
      Serial.println("Comando inválido.");
    }
  }

  ejecutarMotor(ultimoComando);
}

void ejecutarMotor(int comando) {
  switch (comando) {
    case 1:  // Velocidad baja
      digitalWrite(pinIN3, HIGH);
      digitalWrite(pinIN4, LOW);
      analogWrite(pinENB, 100);
      break;
    case 2:  // Velocidad máxima
      digitalWrite(pinIN3, HIGH);
      digitalWrite(pinIN4, LOW);
      analogWrite(pinENB, 255);
      break;
    case 3:  // Cambio de dirección con velocidad media
      digitalWrite(pinIN3, LOW);
      digitalWrite(pinIN4, HIGH);
      analogWrite(pinENB, 150);
      break;
    default:  // Detener el motor si el comando es inválido
      digitalWrite(pinIN3, LOW);
      digitalWrite(pinIN4, LOW);
      analogWrite(pinENB, 0);
      break;
  }
}