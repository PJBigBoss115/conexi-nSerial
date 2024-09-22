import socket
import serial

def iniciar_servidor(ip: str, puerto: int, puerto_serial: str, baudrate: int):
    # Configurar el puerto serial (Arduino)
    ser = serial.Serial(puerto_serial, baudrate)
    
    # Crear socket TCP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((ip, puerto))
    servidor.listen(1)
    print(f"Servidor escuchando en {ip}:{puerto}...")
    
    conn, addr = servidor.accept()
    print(f"Conexión establecida con {addr}")

    try:
        while True:
            # Leer del puerto serial (Arduino)
            if ser.in_waiting > 0:
                datos_serial = ser.readline().decode('utf-8').strip()
                print(f"Datos serial recibidos: {datos_serial}")
                
                # Enviar datos por la red a la otra computadora
                conn.sendall(datos_serial.encode('utf-8'))

            # Recibir datos de la otra computadora
            datos_red = conn.recv(1024).decode('utf-8')
            if datos_red:
                print(f"Datos de la otra computadora: {datos_red}")
                
                # Escribir datos en el puerto serial (Arduino)
                ser.write(datos_red.encode('utf-8'))

    except KeyboardInterrupt:
        print("Servidor interrumpido.")
    
    finally:
        # Cerrar conexiones
        conn.close()
        servidor.close()
        ser.close()

# Cambiar el puerto serial según tu sistema
if _name_ == "_main_":
    iniciar_servidor("0.0.0.0", 12345, "COM3", 9600)
