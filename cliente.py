import socket
import serial

def iniciar_cliente(ip: str, puerto: int, puerto_serial: str, baudrate: int):
    # Configurar el puerto serial (Arduino)
    ser = serial.Serial(puerto_serial, baudrate)

    # Crear socket TCP
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Conectar al servidor
        cliente.connect((ip, puerto))
        print(f"Conectado al servidor en {ip}:{puerto}")

        while True:
            # Leer del puerto serial (Arduino)
            if ser.in_waiting > 0:
                datos_serial = ser.readline().decode('utf-8').strip()
                print(f"Datos serial recibidos: {datos_serial}")
                
                # Enviar datos al servidor
                cliente.sendall(datos_serial.encode('utf-8'))

            # Recibir datos del servidor (otra computadora)
            datos_red = cliente.recv(1024).decode('utf-8')
            if datos_red:
                print(f"Datos del servidor: {datos_red}")
                
                # Escribir datos en el puerto serial (Arduino)
                ser.write(datos_red.encode('utf-8'))

    except KeyboardInterrupt:
        print("Cliente interrumpido.")
    
    finally:
        # Cerrar conexiones
        cliente.close()
        ser.close()

# Cambiar el puerto serial según tu sistema
if __name__ == "__main__":
    iniciar_cliente("192.168.10.1", 12345, "COM3", 9600) 
