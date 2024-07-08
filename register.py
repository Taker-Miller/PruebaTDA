import tkinter as tk
from tkinter import messagebox
from logica import registrar_usuario

def crear_interfaz_registro(root, build_login_gui, build_main_app_gui):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Registro - Sistema de Mesa de Ayuda")
    root.geometry("300x400")

    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)

    tk.Label(frame, text="Nombre de usuario:").pack()
    username_entry = tk.Entry(frame)
    username_entry.pack(pady=5)

    tk.Label(frame, text="Correo electrónico:").pack()
    email_entry = tk.Entry(frame)
    email_entry.pack(pady=5)

    tk.Label(frame, text="Contraseña:").pack()
    password_entry = tk.Entry(frame, show="*")
    password_entry.pack(pady=5)

    tk.Label(frame, text="Tipo de usuario:").pack()
    tipo_usuario = tk.StringVar(root)
    tipo_usuario.set("Usuario")
    tipo_usuario_menu = tk.OptionMenu(frame, tipo_usuario, "Administrador", "Técnico", "Usuario")
    tipo_usuario_menu.pack(pady=5)

    tk.Button(frame, text="Registrar usuario", command=lambda: handle_register(username_entry.get(), email_entry.get(), password_entry.get(), tipo_usuario.get(), root, build_login_gui)).pack(pady=10)
    tk.Button(frame, text="Regresar", command=build_login_gui).pack(pady=10)

def handle_register(username, email, password, tipo, root, build_login_gui):
    if not username or not email or not password or not tipo:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return
    
    if "@" not in email:
        messagebox.showerror("Error", "El correo electrónico debe contener '@'.")
        return

    if registrar_usuario(username, email, password, tipo):
        messagebox.showinfo("Registro", "Usuario registrado exitosamente.")
        build_login_gui()
    else:
        messagebox.showerror("Error", "No se pudo registrar el usuario.")
