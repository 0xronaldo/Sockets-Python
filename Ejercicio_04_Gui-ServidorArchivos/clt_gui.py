import socket
import tkinter as tk
from tkinter import messagebox, scrolledtext


IP_SERVER = '192.168.29.247'
PORT = 9220

def descargar_archivo():
    servidor_ip = ip_entry.get().strip()
    servidor_puerto = puerto_entry.get().strip()
    nombre_archivo = archivo_entry.get().strip()

    if not servidor_ip:
        messagebox.showwarning("Advertencia", "Ingresa la IP del servidor")
        return
    if not servidor_puerto.isdigit():
        messagebox.showwarning("Advertencia", "Ingresa un puerto válido")
        return
    if not nombre_archivo:
        messagebox.showwarning("Advertencia", "Ingresa el nombre del archivo")
        return

    try:
        # Conectar al servidor
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((servidor_ip, int(servidor_puerto)))

        # Enviar nombre del archivo
        client_socket.send(nombre_archivo.encode('utf-8'))

        # Recibir respuesta
        with open(f"descargado_{nombre_archivo}", 'wb') as f:
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                f.write(data)

        client_socket.close()
        log_text.config(state=tk.NORMAL)
        log_text.insert(tk.END, f" Archivo '{nombre_archivo}' descargado como 'descargado_{nombre_archivo}'\n")
        log_text.see(tk.END)
        log_text.config(state=tk.DISABLED)
        messagebox.showinfo("Éxito", f"Archivo guardado como 'descargado_{nombre_archivo}'")

    except Exception as e:
        log_text.config(state=tk.NORMAL)
        log_text.insert(tk.END, f" Error: {e}\n")
        log_text.see(tk.END)
        log_text.config(state=tk.DISABLED)
        messagebox.showerror("Error", f"No se pudo descargar el archivo: {e}")

# Función para escribir en el log (aunque ya lo hacemos arriba, lo dejamos claro)
def log(mensaje):
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, mensaje + "\n")
    log_text.see(tk.END)
    log_text.config(state=tk.DISABLED)

# Configuración de la ventana
root = tk.Tk()
root.title("Cliente de Archivos")
root.geometry("500x400")

# Entrada de IP
tk.Label(root, text="IP del Servidor:").pack(pady=5)
ip_entry = tk.Entry(root, width=30)
ip_entry.insert(0, IP_SERVER)  # localhost por defecto
ip_entry.pack(pady=5)

# Entrada de Puerto
tk.Label(root, text="Puerto:").pack(pady=5)
puerto_entry = tk.Entry(root, width=10)
puerto_entry.insert(0, PORT)
puerto_entry.pack(pady=5)

# Entrada de nombre de archivo
tk.Label(root, text="Nombre del archivo :").pack(pady=5)
archivo_entry = tk.Entry(root, width=40)
archivo_entry.pack(pady=5)

# Botón de descarga
tk.Button(root, text="Descargar Archivo", command=descargar_archivo, bg="#4CAF50", fg="white").pack(pady=15)

# Log de actividad
tk.Label(root, text="Log de Descargas:").pack(pady=5)
log_text = scrolledtext.ScrolledText(root, height=10, state=tk.DISABLED)
log_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Iniciar interfaz
root.mainloop()