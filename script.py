import requests
import serial
import time

# 🔩 Configuración global
GITHUB_URL = "https://raw.githubusercontent.com/KVNSS002/CONTROLAR-MOTOR/main/estado.json"
SERIAL_PORT = "COM7"
BAUDRATE = 9600

# 🚀 Conectar con Arduino con timeout ajustado
try:
    arduino = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=0.3)  # Aumentado para evitar bloqueos
    time.sleep(1)  # Esperar conexión
except serial.SerialException:
    print(f"❌ Error: No se pudo abrir el puerto {SERIAL_PORT}. Verifica la conexión.")
    exit()

# 🔄 Bucle para actualizar estado y enviar comandos cada 2.5 segundos
while True:
    try:
        # 🔥 Reintentar la descarga hasta 3 veces para evitar caché y demoras
        for _ in range(3):
            response = requests.get(GITHUB_URL, timeout=3, headers={"Cache-Control": "no-cache", "Pragma": "no-cache"})
            if response.status_code == 200:
                break  # Si la respuesta es correcta, salir del bucle

        response.raise_for_status()

        # Extraer comando y enviarlo SIEMPRE
        comando = str(response.json().get("comando", ""))
        arduino.write(comando.encode())
        arduino.flush()
        print(f"✅ Comando enviado a Arduino: {comando}")

    except requests.exceptions.RequestException:
        print("⚠ Error al obtener datos de GitHub.")

    time.sleep(2.5)  # **Ahora se ejecuta cada 2.5 segundos**