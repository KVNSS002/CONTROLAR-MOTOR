import requests
import serial
import time

# URL de GitHub
GITHUB_URL = "https://raw.githubusercontent.com/KVNSS002/CONTROLAR-MOTOR/main/estado.json"
SERIAL_PORT = "COM7"
BAUDRATE = 9600

# Conectar con Arduino
try:
    arduino = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
except serial.SerialException:
    print(f"Error: No se pudo abrir el puerto {SERIAL_PORT}.")
    exit()

ultimo_comando = None

while True:
    try:
        response = requests.get(GITHUB_URL, timeout=10)  # Long Polling con timeout de 10 segundos
        if response.status_code == 200:
            data = response.json()
            comando_actual = str(data.get("comando", ""))

            if comando_actual and comando_actual != ultimo_comando:
                arduino.write(comando_actual.encode())
                print(f"✅ Comando actualizado y enviado a Arduino: {comando_actual}")
                ultimo_comando = comando_actual

        else:
            print(f"⚠ Error al obtener estado.json, código {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"⚠ Error en la conexión: {e}")

    time.sleep(0.5)  # Revisar cambios cada 500ms