# ...existing code...
#!/usr/bin/env python3
# Cliente GUI básico para el servidor de chat TCP usando tkinter.

import socket
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText

IP_SERVER = '192.168.100.37'
PORT_HOST = 9200

class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente Chat - Tkinter")
        self.sock = None
        self.recv_thread = None
        self.running = False

        # --- UI ---
        mainframe = ttk.Frame(root, padding="8")
        mainframe.grid(row=0, column=0, sticky="nsew")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Conexión: IP y puerto
        conn_frame = ttk.Frame(mainframe)
        conn_frame.grid(row=0, column=0, sticky="ew", pady=(0,8))
        conn_frame.columnconfigure(1, weight=1)

        ttk.Label(conn_frame, text="Servidor:").grid(row=0, column=0, sticky="w")
        self.ip_entry = ttk.Entry(conn_frame)
        self.ip_entry.grid(row=0, column=1, sticky="ew", padx=4)
        self.ip_entry.insert(0, IP_SERVER)

        ttk.Label(conn_frame, text="Puerto:").grid(row=0, column=2, sticky="w", padx=(8,0))
        self.port_entry = ttk.Entry(conn_frame, width=6)
        self.port_entry.grid(row=0, column=3, sticky="w")
        self.port_entry.insert(0, str(PORT_HOST))

        self.connect_btn = ttk.Button(conn_frame, text="Conectar", command=self.connect)
        self.connect_btn.grid(row=0, column=4, padx=(8,0))
        self.disconnect_btn = ttk.Button(conn_frame, text="Desconectar", command=self.disconnect, state="disabled")
        self.disconnect_btn.grid(row=0, column=5, padx=(4,0))

        # Área de chat
        self.chat_area = ScrolledText(mainframe, state="disabled", wrap="word", width=60, height=20)
        self.chat_area.grid(row=1, column=0, sticky="nsew")
        mainframe.rowconfigure(1, weight=1)

        # Entrada de mensaje y botón enviar
        entry_frame = ttk.Frame(mainframe)
        entry_frame.grid(row=2, column=0, sticky="ew", pady=(8,0))
        entry_frame.columnconfigure(0, weight=1)

        self.msg_entry = ttk.Entry(entry_frame)
        self.msg_entry.grid(row=0, column=0, sticky="ew")
        self.msg_entry.bind("<Return>", lambda e: self.send_message())

        self.send_btn = ttk.Button(entry_frame, text="Enviar", command=self.send_message, state="disabled")
        self.send_btn.grid(row=0, column=1, padx=(8,0))

        # Estado
        self.status_var = tk.StringVar(value="Desconectado")
        status_label = ttk.Label(mainframe, textvariable=self.status_var, anchor="w")
        status_label.grid(row=3, column=0, sticky="ew", pady=(6,0))

        # Cerrar ventana -> desconectar correctamente
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def append_chat(self, text):
        self.chat_area.configure(state="normal")
        self.chat_area.insert("end", text + "\n")
        self.chat_area.yview_moveto(1.0)
        self.chat_area.configure(state="disabled")

    def connect(self):
        if self.running:
            return
        server = self.ip_entry.get().strip() or IP_SERVER
        try:
            port = int(self.port_entry.get().strip() or PORT_HOST)
        except ValueError:
            messagebox.showerror("Error", "Puerto inválido.")
            return

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((server, port))
        except Exception as e:
            messagebox.showerror("Conexión fallida", f"No se pudo conectar: {e}")
            self.sock = None
            return

        self.running = True
        self.recv_thread = threading.Thread(target=self.receive_loop, daemon=True)
        self.recv_thread.start()

        self.connect_btn.configure(state="disabled")
        self.disconnect_btn.configure(state="normal")
        self.send_btn.configure(state="normal")
        self.status_var.set(f"Conectado a {server}:{port}")
        self.append_chat(f"-- Conectado a {server}:{port} --")

    def send_message(self):
        if not self.sock or not self.running:
            messagebox.showwarning("No conectado", "Primero conecta al servidor.")
            return
        msg = self.msg_entry.get().strip()
        if not msg:
            return
        try:
            # enviar y mostrar en chat local
            self.sock.send(msg.encode("utf-8"))
            self.append_chat(f"[Tú] {msg}")
            self.msg_entry.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar: {e}")
            self.disconnect()

    def receive_loop(self):
        try:
            while self.running:
                try:
                    data = self.sock.recv(1024)
                except OSError:
                    # socket cerrado
                    break
                if not data:
                    # conexión cerrada por servidor
                    self.root.after(0, lambda: self.append_chat("-- Conexión cerrada por el servidor --"))
                    break
                mensaje = data.decode("utf-8")
                # manejar cierre ordenado
                if mensaje == "CERRAR":
                    self.root.after(0, lambda: self.append_chat("[Servidor] CERRAR"))
                    self.root.after(0, lambda: self.disconnect())
                    break
                # actualizar GUI desde hilo principal
                self.root.after(0, lambda m=mensaje: self.append_chat(f"[Usuario] {m}"))
        finally:
            self.running = False
            self.root.after(0, self._on_disconnected_ui)

    def _on_disconnected_ui(self):
        self.connect_btn.configure(state="normal")
        self.disconnect_btn.configure(state="disabled")
        self.send_btn.configure(state="disabled")
        self.status_var.set("Desconectado")

    def disconnect(self):
        if not self.running:
            # asegurar estado UI
            self._on_disconnected_ui()
            if self.sock:
                try:
                    self.sock.close()
                except:
                    pass
                self.sock = None
            return

        self.running = False
        try:
            if self.sock:
                # intentar cerrar ordenadamente
                try:
                    self.sock.send("CERRAR".encode("utf-8"))
                except:
                    pass
                self.sock.close()
        finally:
            self.sock = None
            self._on_disconnected_ui()
            self.append_chat("-- Desconectado --")

    def on_close(self):
        # Llamado al cerrar ventana
        self.disconnect()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
