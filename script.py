import requests
import serial
import time

# 🔩 Configuración global
GITHUB_URL = "https://raw.githubusercontent.com/KVNSS002/CONTROLAR-MOTOR/main/estado.json"
SERIAL_PORT = "COM7"
BAUDRATE = 9600

# 🚀 Conectar con Arduino con timeout reducido
try:
    arduino = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=0.2)  # Mejor rendimiento en la comunicación serial
    time.sleep(1)  # Esperar conexión
except serial.SerialException:
    print(f"❌ Error: No se pudo abrir el puerto {SERIAL_PORT}. Verifica la conexión.")
    exit()

# 🔄 Bucle para actualizar estado y enviar comandos cada 2 segundos
while True:
    try:
        # 🔥 Forzar actualización del estado.json sin caché
        response = requests.get(GITHUB_URL, timeout=2, headers={"Cache-Control": "no-cache", "Pragma": "no-cache"})
        response.raise_for_status()

        # Extraer comando y enviarlo SIEMPRE
        comando = str(response.json().get("comando", ""))
        arduino.write(comando.encode())
        arduino.flush()
        print(f"✅ Comando enviado a Arduino: {comando}")

    except requests.exceptions.RequestException:
        print("⚠ Error al obtener datos de GitHub.")

    time.sleep(2)  # **Ahora la revisión es cada 2 segundos**