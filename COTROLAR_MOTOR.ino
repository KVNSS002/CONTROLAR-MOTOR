// Definición de pines para control del motor
const int pinIN3 = 22;
const int pinIN4 = 23;
const int pinENB = 2;

// Variable para almacenar el último comando recibido
char ultimoComando = '0';

void setup() {
  // Configuración de pines como salida
  pinMode(pinIN3, OUTPUT);
  pinMode(pinIN4, OUTPUT);
  pinMode(pinENB, OUTPUT);

  // Iniciar comunicación serial
  Serial.begin(9600);
}

void moverMotor(int in3, int in4, int velocidad) {
  digitalWrite(pinIN3, in3);
  digitalWrite(pinIN4, in4);
  analogWrite(pinENB, velocidad);
}

void detenerMotor() {
  digitalWrite(pinIN3, LOW);
  digitalWrite(pinIN4, LOW);
  analogWrite(pinENB, 0);
}

void loop() {
  // Verificar si hay un nuevo comando en el puerto serial
  if (Serial.available() > 0) {
    char comando = Serial.read();

    // Validar si el comando recibido es '1', '2' o '3'
    if (comando == '1' || comando == '2' || comando == '3') {
      ultimoComando = comando;  // Guardar el comando válido
      Serial.print("Motor activado con comando: ");
      Serial.println(ultimoComando);
    } else {
      Serial.println("Comando desconocido. Use '1', '2' o '3'.");
    }
  }

  // Ejecutar acción según el último comando válido
  switch (ultimoComando) {
    case '1':
      moverMotor(HIGH, LOW, 100);  // Velocidad baja en una dirección
      break;
    case '2':
      moverMotor(HIGH, LOW, 200);  // Velocidad alta en la misma dirección
      break;
    case '3':
      moverMotor(LOW, HIGH, 150);  // Cambio de dirección con velocidad media
      break;
    default:
      detenerMotor();  // Si no hay un comando válido, se detiene el motor
      break;
  }
}