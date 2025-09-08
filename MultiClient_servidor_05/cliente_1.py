# Desarrolla un servidor que pueda atender múltiples clientes usando hilos, 
# donde cada cliente puede enviar un mensaje y el servidor responde con la 
# cantidad de caracteres del mensaje. 


import socket

IP_SERVER = '192.168.100.37'
PUERTO = 9220
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((IP_SERVER, PUERTO))
print("Conectado al servidor.")
get_name = input("Ingresa tu nombre: ")
try:
    while True:
        mensaje = input("Tú: ").strip()
        if mensaje.lower() == 'salir':
            break
        if not mensaje:
            print(" Mensaje vacío, no enviado.")
            continue
        cliente.send(mensaje.encode('utf-8'))
        respuesta = cliente.recv(1024).decode('utf-8')
        print(f"{get_name}: {respuesta}")
except Exception as e:
    print(f"Error: {e}")
finally:
    cliente.close()
    print("Conexión cerrada.")