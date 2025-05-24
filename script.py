import requests
import serial
import time

# URL del archivo RAW en GitHub (actualízala con tu repositorio)
GITHUB_URL = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPOSITORIO/main/estado.json"

# Configurar el puerto correcto para Arduino (verificar en Arduino IDE)
SERIAL_PORT = "COM7"  # Cambia según tu configuración (Windows: COMX, Linux/Mac: /dev/ttyUSB0)
BAUDRATE = 9600

# Iniciar conexión serial con Arduino
try:
    arduino = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    time.sleep(2)  # Esperar conexión
except serial.SerialException:
    print(f"Error: No se pudo abrir el puerto {SERIAL_PORT}. Verifica la conexión.")
    exit()

while True:
    try:
        # Obtener estado.json desde GitHub
        response = requests.get(GITHUB_URL)
        
        if response.status_code == 200:
            data = response.json()
            comando = str(data["comando"])  # Convertir a cadena

            # Enviar comando a Arduino
            arduino.write(comando.encode())
            print(f"Comando enviado a Arduino: {comando}")
        else:
            print("Error al obtener datos de GitHub:", response.status_code)

    except Exception as e:
        print(f"Error en el script: {e}")

    time.sleep(2)  # Revisar cambios cada 2 segundos