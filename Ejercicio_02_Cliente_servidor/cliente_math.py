

# Diseña un servidor que reciba números enviados por un cliente y responda 
# con el número mayor y menor de la lista recibida. 
# Autor: Sanchez Brayan

import socket


IP_SERVER = '192.168.100.37'
PORT = 9220


def _runcliente():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((IP_SERVER, PORT))
    while True:
        numeros = input("Ingrese una lista de números separados por comas: ")
        cliente.sendall(numeros.encode())
        data = cliente.recv(1024)
        print(f"Respuesta del servidor: {data.decode()}")
    cliente.close()




if __name__ == "__main__":
    _runcliente()