# Implementa un servidor de chat simple con sockets TCP que permita la 
# comunicación entre dos clientes de manera simultánea. 

import socket


def clt_conexion():
    IP_SERVER = '192.168.100.37'
    PORT_SERVER = 9220  # puerto
    
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((IP_SERVER, PORT_SERVER))
    print("Conectado al servidor.")
    print("[+] Conectado ::[ok]:")

    while True:
        mensaje = input("[+] Cliente -> ")
        cliente.send(mensaje.encode())
        respuesta = cliente.recv(1024).decode()
        print(f"Otro: {respuesta}")

if __name__ == '__main__':
    clt_conexion()