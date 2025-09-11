# Crea un servidor de archivos que permita a un cliente solicitar un archivo de 
# texto y recibirlo completo en la descarga.


import socket

def srv_cliente():
    IP_SERVER = '192.168.100.37'
    PORT = 9220

    print("=== CLIENTE DE DESCARGA ===")
    nombre_archivo = input("Ingresa el nombre de [Fichero]: ").strip()
    # Obtener la extensión del archivo
    ext = nombre_archivo.split('.')[-1]
    if not nombre_archivo:
        print("Nombre de archivo vacío.")
        exit()

    # Conectar al servidor
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente.connect((IP_SERVER, PORT))
        print(f"Conectado al servidor {IP_SERVER}:{PORT}")

        # Enviar nombre del archivo
        cliente.send(nombre_archivo.encode('utf-8'))

        # Recibir respuesta
        with open(f"descargado_{nombre_archivo}", 'wb') as f:
            while True:
                #aumentamos el tipo de codificacion a 4096 o 2048
                datos = cliente.recv(2048)
                if not datos:
                    break
                f.write(datos)

        print(f"Archivo guardado como 'descargado_{nombre_archivo}'")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        cliente.close()

if __name__ == '__main__':
    srv_cliente()