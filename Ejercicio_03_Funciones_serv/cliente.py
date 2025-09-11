# Programa un sistema cliente-servidor que permita a un cliente enviar 
# operaciones aritméticas en formato texto (ej. '4+5') y el servidor devuelva el 
# resultado. 

import socket 

IP_SERVER = '192.168.29.247'
PORT = 9220


def cliente():
    clt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clt.connect((IP_SERVER, PORT))
    print("Ingrese datos (o 'salir' para salir):")
    while True:

        try:
            operacion = input("Ingrese la operación: ")
            if operacion == 'salir':
                break
            clt.sendall(operacion.encode())
            resultado = clt.recv(1024)
            print(f"Resultado: {resultado.decode()}")
        except Exception as e:
            print(f"Error: {e}")
    clt.close()

if __name__ == "__main__":
    cliente()