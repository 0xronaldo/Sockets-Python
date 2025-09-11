# Desarrolla un servidor que pueda atender múltiples clientes usando hilos, 
# donde cada cliente puede enviar un mensaje y el servidor responde con la 
# cantidad de caracteres del mensaje. 

import socket
import threading


IP_SERVER = '192.168.100.37'
PORT = 9220

# Función que maneja a cada cliente
def manejar_cliente(cliente, direccion):
    print(f"Cliente conectado desde {direccion}")
    try:
        while True:
            mensaje = cliente.recv(1024).decode('utf-8')
            if not mensaje:
                break  # Cliente cerró conexión
            print(f"Recibido de {direccion}: '{mensaje}'")
            longitud = len(mensaje)
            respuesta = f"Tu mensaje tiene {longitud} caracteres."
            cliente.send(respuesta.encode('utf-8'))
    except Exception as e:
        print(f"Error con cliente {direccion}: {e}")
    finally:
        cliente.close()
        print(f"Cliente {direccion} desconectado.")

# Función principal del servidor
def run_multserv():
    
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((IP_SERVER, PORT))
    servidor.listen(5)
    print(f"Servidor escuchando en puerto {PORT}...")

    try:
        while True:
            cliente, direccion = servidor.accept()
            hilo = threading.Thread(target=manejar_cliente, args=(cliente, direccion))
            hilo.daemon = True  # Para que se cierre al terminar el programa
            hilo.start()
    except KeyboardInterrupt:
        print("\nServidor detenido manualmente.")
    finally:
        servidor.close()


if __name__ == "__main__":
    run_multserv()