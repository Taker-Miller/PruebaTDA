import tkinter as tk
from tkinter import ttk, messagebox, Menu
from gui import SistemaDeAyuda
from logica import validar_usuario, crear_usuario

class LoginRegistro:
    def __init__(self, root, launch_main_app):
        self.root = root
        self.launch_main_app = launch_main_app
        self.root.title("Sistema de Gestión de Tiques - Login")
        self.frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.crear_interfaz_login()

    def crear_interfaz_login(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        ttk.Label(self.frame, text="Usuario:").pack(pady=10)
        self.usuario_entry = ttk.Entry(self.frame)
        self.usuario_entry.pack()

        ttk.Label(self.frame, text="Contraseña:").pack(pady=10)
        self.contrasena_entry = ttk.Entry(self.frame, show="*")
        self.contrasena_entry.pack()

        self.menu_button = ttk.Menubutton(self.frame, text="Seleccionar Rol", direction="below")
        self.menu = Menu(self.menu_button, tearoff=0)
        self.menu_button["menu"] = self.menu
        self.codigo_entry = tk.StringVar()
        self.codigo_acceso_entry = None  # Entry for código de acceso
        self.roles = ["Administrador", "Ejecutivo de Área Específica", "Jefe de Mesa", "Ejecutivo de Mesa de Ayuda", "Técnico de Soporte", "Usuario"]
        for rol in self.roles:
            self.menu.add_radiobutton(label=rol, variable=self.codigo_entry, value=rol, command=self.actualizar_seleccion_rol)
        self.menu_button.pack(pady=10)

        self.iniciar_sesion_button = ttk.Button(self.frame, text="Iniciar Sesión", command=self.iniciar_sesion)
        self.iniciar_sesion_button.pack(pady=20)
        ttk.Button(self.frame, text="Registrar", command=self.crear_interfaz_registro).pack(pady=10)

    def actualizar_seleccion_rol(self):
        seleccion = self.codigo_entry.get()
        self.menu_button.config(text=seleccion)
        
        # Mostrar u ocultar el campo de código de acceso según el rol seleccionado
        if seleccion in ["Administrador", "Ejecutivo de Área Específica", "Jefe de Mesa", "Ejecutivo de Mesa de Ayuda", "Técnico de Soporte"]:
            if not self.codigo_acceso_entry:
                ttk.Label(self.frame, text="Código de acceso:").pack(pady=10)
                self.codigo_acceso_entry = ttk.Entry(self.frame, show="*")
                self.codigo_acceso_entry.pack()
        else:
            if self.codigo_acceso_entry:
                self.codigo_acceso_entry.destroy()
                self.codigo_acceso_entry = None

    def iniciar_sesion(self):
        usuario = self.usuario_entry.get()
        contraseña = self.contrasena_entry.get()
        rol = self.codigo_entry.get()
        codigo_acceso = self.codigo_acceso_entry.get() if self.codigo_acceso_entry else ""

        if not usuario or not contraseña or not rol:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        usuario_valido, tipo_usuario = validar_usuario(usuario, contraseña, rol, codigo_acceso)
        if usuario_valido and tipo_usuario == rol:
            messagebox.showinfo("Inicio de sesión", f"Inicio de sesión exitoso como {tipo_usuario}.")
            self.launch_main_app(tipo_usuario)  # Pasa el tipo_usuario como argumento
        else:
            messagebox.showerror("Error", "Usuario, contraseña o código de acceso incorrectos.")

    def crear_interfaz_registro(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        ttk.Label(self.frame, text="Usuario:").pack(pady=10)
        self.nuevo_usuario_entry = ttk.Entry(self.frame)
        self.nuevo_usuario_entry.pack()

        ttk.Label(self.frame, text="Correo electrónico:").pack(pady=10)
        self.correo_entry = ttk.Entry(self.frame)
        self.correo_entry.pack()

        ttk.Label(self.frame, text="Contraseña:").pack(pady=10)
        self.nueva_contrasena_entry = ttk.Entry(self.frame, show="*")
        self.nueva_contrasena_entry.pack()

        self.menu_button = ttk.Menubutton(self.frame, text="Seleccionar Rol", direction="below")
        self.menu = Menu(self.menu_button, tearoff=0)
        self.menu_button["menu"] = self.menu
        self.codigo_registro_entry = tk.StringVar()
        self.codigo_acceso_registro_entry = None  # Entry for código de acceso
        for rol in self.roles:
            self.menu.add_radiobutton(label=rol, variable=self.codigo_registro_entry, value=rol, command=self.actualizar_seleccion_rol_registro)
        self.menu_button.pack(pady=10)

        self.registrar_button = ttk.Button(self.frame, text="Registrar", command=self.registrar_usuario)
        self.registrar_button.pack(pady=20)
        ttk.Button(self.frame, text="Volver al inicio", command=self.crear_interfaz_login).pack(pady=10)

    def actualizar_seleccion_rol_registro(self):
        seleccion = self.codigo_registro_entry.get()
        self.menu_button.config(text=seleccion)

        # Mostrar u ocultar el campo de código de acceso según el rol seleccionado
        if seleccion in ["Administrador", "Ejecutivo de Área Específica", "Jefe de Mesa", "Ejecutivo de Mesa de Ayuda", "Técnico de Soporte"]:
            if not self.codigo_acceso_registro_entry:
                ttk.Label(self.frame, text="Código de acceso:").pack(pady=10)
                self.codigo_acceso_registro_entry = ttk.Entry(self.frame, show="*")
                self.codigo_acceso_registro_entry.pack()
        else:
            if self.codigo_acceso_registro_entry:
                self.codigo_acceso_registro_entry.destroy()
                self.codigo_acceso_registro_entry = None

    def registrar_usuario(self):
        usuario = self.nuevo_usuario_entry.get()
        correo = self.correo_entry.get()
        contraseña = self.nueva_contrasena_entry.get()
        rol = self.codigo_registro_entry.get()
        codigo_acceso = self.codigo_acceso_registro_entry.get() if self.codigo_acceso_registro_entry else ""

        if not usuario or not correo or not contraseña or not rol:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if "@" not in correo:
            messagebox.showerror("Error", "El correo electrónico debe contener '@'.")
            return

        if rol in ["Administrador", "Ejecutivo de Área Específica", "Jefe de Mesa", "Ejecutivo de Mesa de Ayuda", "Técnico de Soporte"] and codigo_acceso != "1234":
            messagebox.showerror("Error", "Código de acceso incorrecto.")
            return

        if crear_usuario(usuario, correo, contraseña, rol):
            messagebox.showinfo("Registro", "Usuario registrado exitosamente.")
            self.crear_interfaz_login()
        else:
            messagebox.showerror("Error", "No se pudo registrar el usuario.")

if __name__ == "__main__":
    root = tk.Tk()
    def launch_main_app(tipo_usuario):
        for widget in root.winfo_children():
            widget.destroy()
        SistemaDeAyuda(root, tipo_usuario)

    app = LoginRegistro(root, launch_main_app)
    root.mainloop()
