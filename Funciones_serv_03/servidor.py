# Programa un sistema cliente-servidor que permita a un cliente enviar 
# operaciones aritméticas en formato texto (ej. '4+5') y el servidor devuelva el 
# resultado. 

import socket

IP_SERVER = '192.168.100.37'
PORT = 9220

def math_eval(adicion):
    return eval(adicion)
    
def _runservidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((IP_SERVER, PORT))
    servidor.listen(1)
    print(f"Servidor escuchando en : {IP_SERVER}:{PORT}")
    while True:
        conx, addr = servidor.accept()
        print(f"Conexión aceptada :-> {addr}")
        while True:
            data = conx.recv(1024)
            if not data:
                break
            resultado = math_eval(data.decode())
            conx.sendall(str(resultado).encode())
        conx.close()

if __name__ == '__main__':
    _runservidor()
