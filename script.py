import requests
import serial
import time

# URL del archivo RAW en GitHub (actualízala con tu repositorio)
GITHUB_URL = "https://raw.githubusercontent.com/KVNSS002/CONTROLAR-MOTOR/main/estado.json"

# Configurar el puerto correcto para Arduino (verificar en Arduino IDE)
SERIAL_PORT = "COM7"  # Cambia según tu configuración
BAUDRATE = 9600

# Intentar conectar con Arduino
try:
    arduino = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    time.sleep(2)  # Esperar conexión
except serial.SerialException:
    print(f"Error: No se pudo abrir el puerto {SERIAL_PORT}. Verifica la conexión.")
    exit()

while True:
    try:
        # Obtener estado.json desde GitHub
        response = requests.get(GITHUB_URL, timeout=10)
        response.raise_for_status()  # Lanza una excepción si la respuesta no es 200

        data = response.json()
        
        if "comando" in data:  # Verificar existencia de la clave
            comando = str(data["comando"])

            try:
                arduino.write(comando.encode())
                arduino.flush()  # Asegurar envío de datos
                print(f"✅ Comando enviado a Arduino: {comando}")
            except serial.SerialException:
                print("⚠ Error al enviar datos al Arduino.")

        else:
            print("⚠ Advertencia: No se encontró 'comando' en el JSON.")

    except requests.exceptions.RequestException as e:
        print(f"⚠ Error en la conexión: {e}")

    time.sleep(2)  # Revisar cambios cada 2 segundos