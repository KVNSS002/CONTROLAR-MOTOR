import requests
import serial
import time
import os
import subprocess

# URL del archivo RAW en GitHub
GITHUB_URL = "https://raw.githubusercontent.com/KVNSS002/CONTROLAR-MOTOR/main/estado.json"

# Configuración del puerto serial de Arduino
SERIAL_PORT = "COM7"
BAUDRATE = 9600

# Directorio del proyecto Git
PROYECTO_DIR = "C:\\Users\\kevin\\Documents\\PROYECTOS GIT\\CONTROLAR-MOTOR"

# Intentar conectar con Arduino
try:
    arduino = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    time.sleep(2)  # Esperar conexión
except serial.SerialException:
    print(f"Error: No se pudo abrir el puerto {SERIAL_PORT}. Verifica la conexión.")
    exit()

# Función para actualizar el código automáticamente
def actualizar_codigo():
    try:
        os.chdir(PROYECTO_DIR)  # Cambiar al directorio del proyecto
        subprocess.run(["git", "pull", "origin", "main"], check=True)  # Descargar cambios
    except Exception as e:
        print(f"⚠ Error al actualizar el código: {e}")

ultimo_comando = None

while True:
    try:
        # Actualizar el código antes de verificar el JSON
        actualizar_codigo()

        # Obtener estado.json desde GitHub
        response = requests.get(GITHUB_URL, timeout=5)
        response.raise_for_status()

        data = response.json()
        
        if "comando" in data:
            comando_actual = str(data["comando"])

            if comando_actual != ultimo_comando:
                try:
                    arduino.write(comando_actual.encode())
                    arduino.flush()
                    print(f"✅ Comando enviado a Arduino: {comando_actual}")
                    ultimo_comando = comando_actual
                except serial.SerialException:
                    print("⚠ Error al enviar datos al Arduino.")
        else:
            print("⚠ No se encontró 'comando' en el JSON.")

    except requests.exceptions.RequestException as e:
        print(f"⚠ Error en la conexión: {e}")

    time.sleep(0.1)  # Revisar cambios cada 100ms (casi instantáneo)