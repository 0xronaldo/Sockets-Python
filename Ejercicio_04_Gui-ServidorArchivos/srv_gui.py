import socket
import threading
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Variables globales
is_running = False
server_socket = None
IP_SERVER = '192.168.29.247'
PORT = 9220


# Función para escribir en el log
def log(message):
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, message + "\n")
    log_text.see(tk.END)
    log_text.config(state=tk.DISABLED)

# Función para manejar cada cliente
def handle_client(client_socket):
    try:
        # Recibir nombre del archivo
        filename = client_socket.recv(1024).decode('utf-8').strip()
        log(f"Solicitud de archivo: {filename}")

        # Validar extensión
        if not filename.endswith(('.txt', '.pdf', '.docx')):
            client_socket.send(b"ERROR: Solo se permiten archivos tipo documento")
            client_socket.close()
            return

        # Verificar existencia
        if not os.path.exists(filename):
            client_socket.send(b"ERROR: Archivo no encontrado")
            client_socket.close()
            return

        # Enviar contenido del archivo
        with open(filename, 'rb') as f:
            data = f.read()
            client_socket.sendall(data)
            log(f"Archivo '{filename}' enviado correctamente.")

    except Exception as e:
        log(f"Error manejando cliente: {e}")
    finally:
        client_socket.close()

# Función para aceptar clientes
def accept_clients():
    global is_running, server_socket
    while is_running:
        try:
            client_socket, addr = server_socket.accept()
            log(f"Cliente conectado: {addr}")
            threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()
        except OSError:
            break  # Socket cerrado

# Función para iniciar el servidor
def start_server():
    global is_running, server_socket
    if is_running:
        return

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((IP_SERVER, PORT))
        server_socket.listen(5)
        is_running = True
        start_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)
        log(f"Servidor iniciado en puerto {PORT}")

        threading.Thread(target=accept_clients, daemon=True).start()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo iniciar el servidor: {e}")

# Función para detener el servidor
def stop_server():
    global is_running, server_socket
    is_running = False
    if server_socket:
        server_socket.close()
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)
    log("Servidor detenido.")

# Cliente de prueba (opcional)
def create_test_client():
    def send_request():
        filename = entry.get()
        if not filename:
            messagebox.showwarning("Advertencia", "Ingresa un nombre de archivo")
            return

        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((IP_SERVER, PORT))
            client.send(filename.encode('utf-8'))

            with open(f"descargado_{filename}", 'wb') as f:
                while True:
                    data = client.recv(4096)
                    if not data:
                        break
                    f.write(data)

            messagebox.showinfo("Éxito", f"Archivo '{filename}' descargado como 'descargado_{filename}'")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo descargar: {e}")
        finally:
            client.close()

    client_win = tk.Toplevel()
    client_win.title("Cliente de Prueba")
    client_win.geometry("300x150")

    tk.Label(client_win, text="Nombre del archivo :").pack(pady=5)
    entry = tk.Entry(client_win)
    entry.pack(pady=5)

    tk.Button(client_win, text="Descargar", command=send_request).pack(pady=10)


# Configuración de la ventana principal
root = tk.Tk()
root.title("Servidor de Archivos")
root.geometry("500x450")

tk.Label(root, text="Puerto:").pack(pady=5)
port_entry = tk.Entry(root)
port_entry.insert(0, PORT)  
port_entry.pack(pady=5)

start_button = tk.Button(root, text="Iniciar Servidor", command=start_server)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Detener Servidor", command=stop_server, state=tk.DISABLED)
stop_button.pack(pady=5)

tk.Label(root, text="Log del Servidor:").pack(pady=5)
log_text = scrolledtext.ScrolledText(root, height=15, state=tk.DISABLED)
log_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Botón para abrir cliente de prueba
tk.Button(root, text="Abrir Cliente de Prueba", command=create_test_client).pack(pady=5)

# Iniciar el loop de Tkinter
root.mainloop()