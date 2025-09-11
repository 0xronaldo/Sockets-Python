# Crea un servidor de archivos que permita a un cliente solicitar un archivo de 
# texto y recibirlo completo en la descarga.


import socket, os



def srv_archivos():
    IP_SERVER = '192.168.29.247'
    PUERTO = 9220

    print("=== SERVIDOR DE ARCHIVOS ===")
    print(f'Iniciando servidor: {IP_SERVER}')
    print(f"Esperando conexiones en puerto {PUERTO}...")
    # Crear socket
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((IP_SERVER, PUERTO))
    servidor.listen(1)

    while True:
        print("\nEsperando cliente...")
        cliente, direccion = servidor.accept()
        print(f"Cliente conectado desde: {direccion}")

        try:
            # Recibir nombre del archivo
            nombre_archivo = cliente.recv(2048).decode('utf-8').strip()
            print(f"Archivo solicitado: '{nombre_archivo}'")

            # Validar extensión .txt
            if not nombre_archivo.endswith(('.txt', '.pdf')):
                cliente.send(b"ERROR: Solo se permiten archivos .txt y .pdf")
                cliente.close()
                print(" Solicitud rechazada: extensión no permitida")
                continue

            # Verificar existencia
            if not os.path.exists(nombre_archivo):
                cliente.send(b"ERROR: Archivo no encontrado")
                cliente.close()
                print("Archivo no encontrado")
                continue

            # Leer y enviar archivo completo
            with open(nombre_archivo, 'rb') as f:
                contenido = f.read()
                cliente.sendall(contenido)
                print(f"Archivo '{nombre_archivo}' enviado correctamente")

        except Exception as e:
            print(f"Error al manejar cliente: {e}")

        finally:
            cliente.close()
            print("Cliente desconectado.")
if __name__ == '__main__':
    srv_archivos()
