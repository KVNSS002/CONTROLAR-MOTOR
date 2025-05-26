import requests
import serial
import time

# 🔩 Configuración global
GITHUB_URL = "https://raw.githubusercontent.com/KVNSS002/CONTROLAR-MOTOR/main/estado.json"
SERIAL_PORT = "COM7"
BAUDRATE = 9600

# 🚀 Conectar con Arduino
try:
    arduino = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=0.5)  # Ajuste de timeout para mejor comunicación
    time.sleep(1)  # Esperar conexión
except serial.SerialException:
    print(f"❌ Error: No se pudo abrir el puerto {SERIAL_PORT}. Verifica la conexión.")
    exit()

# 🔄 Bucle para actualizar estado y enviar comandos cada 2 segundos
while True:
    try:
        # Obtener estado.json SIN caché para asegurar actualización
        response = requests.get(GITHUB_URL, timeout=2, headers={"Cache-Control": "no-cache", "Pragma": "no-cache"})
        response.raise_for_status()

        # Extraer comando y enviarlo SIEMPRE
        comando = str(response.json().get("comando", ""))
        arduino.write(comando.encode())
        arduino.flush()
        print(f"✅ Comando repetido a Arduino: {comando}")

    except requests.exceptions.RequestException:
        print("⚠ Error al obtener datos de GitHub.")

    time.sleep(2)  # **Ahora se ejecuta cada 2 segundos**