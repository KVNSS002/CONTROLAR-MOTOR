import requests
import serial
import time
import os
import subprocess

# Configuración global
GITHUB_URL = "https://raw.githubusercontent.com/KVNSS002/CONTROLAR-MOTOR/main/estado.json"
SERIAL_PORT = "COM7"
BAUDRATE = 9600
PROYECTO_DIR = "C:\\Users\\kevin\\Documents\\PROYECTOS GIT\\CONTROLAR-MOTOR"

# Intentar conectar con Arduino
try:
    arduino = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=0.5)  # Ajuste del timeout
    time.sleep(1)  # Reducción del tiempo inicial de conexión
except serial.SerialException:
    print(f"Error: No se pudo abrir el puerto {SERIAL_PORT}.")
    exit()

# Función para actualizar código desde GitHub
def actualizar_codigo():
    try:
        os.chdir(PROYECTO_DIR)
        subprocess.run(["git", "pull", "origin", "main"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        pass  # Ignorar errores de actualización

ultimo_comando = None

while True:
    try:
        actualizar_codigo()

        # Obtener estado.json con menor latencia
        response = requests.get(GITHUB_URL, timeout=2)
        data = response.json()
        comando_actual = str(data.get("comando", ""))

        if comando_actual and comando_actual != ultimo_comando:
            try:
                arduino.write(comando_actual.encode())
                arduino.flush()
                print(f"✅ Comando enviado: {comando_actual}")
                ultimo_comando = comando_actual
            except serial.SerialException:
                pass  # Ignorar errores de comunicación

    except requests.exceptions.RequestException:
        pass  # Ignorar errores de conexión

    time.sleep(0.5)  # **Tiempo mínimo de espera: 500ms**