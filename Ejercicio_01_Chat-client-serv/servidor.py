# Implementa un servidor de chat simple con sockets TCP que permita la 
# comunicación entre dos clientes de manera simultánea. 
import socket
import select

IP_SERVER = '192.168.100.37'
PORT = 9220

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((IP_SERVER, PORT))
servidor.listen(2)
print(f"Servidor escuchando en {IP_SERVER}:{PORT}...")

clientes = []
while len(clientes) < 2:
    cliente, addr = servidor.accept()
    print(f"Cliente conectado: {addr}")
    clientes.append(cliente)

print("Dos clientes conectados. ¡Chat iniciado!")

while True:
    # Esperamos que cualquiera de los dos clientes envíe algo
    listos, _, _ = select.select(clientes, [], [])
    
    for sock in listos:
        try:
            data = sock.recv(1024).decode()
            if not data:
                print("Un cliente se desconectó.")
                break
            
            # Enviar el mensaje al otro cliente
            otro = clientes[1] if sock == clientes[0] else clientes[0]
            otro.send(data.encode())
            
        except:
            print("Error en conexión.")
            break
    else:
        continue
    break

servidor.close()