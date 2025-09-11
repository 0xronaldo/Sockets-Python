# Diseña un servidor que reciba números enviados por un cliente y responda 
# con el número mayor y menor de la lista recibida. 

import socket

IP_SERVER = '192.168.29.247'
PORT = 9220

def operacion(lista):
    mayor_a = max(lista)
    menor_b = min(lista)
    return f"Mayor: {mayor_a}, Menor: {menor_b}"

def _runservidor():
    # modo alternativo 
    # srv = socket.socket()
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((IP_SERVER, PORT))
    servidor.listen(1)
    print(f"Servidor escuchando en {IP_SERVER}:{PORT}")
    while True:
        conx, addr = servidor.accept()
        print(f"Conexión aceptada de {addr}")
        while True:
            data = conx.recv(1024)
            if not data:
                break
            try:
                lista = list(map(int, data.decode().split(",")))
                resultado = operacion(lista)
            except Exception as e:
                resultado = f"Error: {e}"
            conx.sendall(resultado.encode())
        conx.close()

if __name__ == "__main__":
    _runservidor()
