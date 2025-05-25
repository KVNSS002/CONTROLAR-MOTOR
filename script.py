import requests
import serial
import time
import os
import subprocess

# Configuración global
GITHUB_URL = "https://raw.githubusercontent.com/KVNSS002/CONTROLAR-MOTOR/main/estado.json"
SERIAL_PORT = "COM7"
BAUDRATE = 9600
PROYECTO_DIR = r"C:\Users\kevin\Documents\PROYECTOS GIT\CONTROLAR-MOTOR"  # Directorio actualizado

# Conectar con Arduino
def conectar_arduino():
    try:
        arduino = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=0.5)
        time.sleep(1)  # Esperar conexión
        return arduino
    except serial.SerialException:
        print(f"Error: No se pudo abrir el puerto {SERIAL_PORT}. Verifica la conexión.")
        exit()

# Actualizar el código desde GitHub
def actualizar_codigo():
    try:
        os.chdir(PROYECTO_DIR)
        subprocess.run(["git", "fetch", "--all"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "reset", "--hard", "origin/main"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "pull", "origin", "main"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"⚠ Error al actualizar el código: {e}")

# Obtener el estado actualizado desde GitHub
def obtener_estado():
    try:
        response = requests.get(GITHUB_URL, timeout=2, headers={"Cache-Control": "no-cache"})
        response.raise_for_status()
        return response.json().get("comando", "")
    except requests.exceptions.RequestException:
        return None  # Ignorar errores de conexión

# Ejecutar ciclo de actualización y envío a Arduino
def ejecutar():
    arduino = conectar_arduino()
    ultimo_comando = None

    while True:
        actualizar_codigo()  # Descargar código actualizado
        comando_actual = obtener_estado()  # Leer JSON actualizado

        if comando_actual and comando_actual.strip() != ultimo_comando:
            try:
                arduino.write(comando_actual.encode())
                arduino.flush()
                print(f"Comando enviado: {comando_actual}")
                ultimo_comando = comando_actual
            except serial.SerialException:
                print("⚠ Error al enviar datos a Arduino.")

        time.sleep(0.5)  # Revisar cambios cada 500ms

# Iniciar ejecución
ejecutar()