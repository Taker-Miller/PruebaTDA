import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from register import crear_interfaz_registro
from logica import validar_usuario, registrar_incidencia, obtener_todas_las_incidencias, actualizar_incidencia, borrar_incidencia, registrar_asignacion, obtener_todas_las_asignaciones, obtener_todos_los_usuarios, borrar_usuario, borrar_asignacion, obtener_todos_los_tecnicos
from datetime import datetime

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de sesión - Sistema de Mesa de Ayuda")
        self.root.geometry("400x300")
        self.root.configure(bg='#f0f0f0')
        self.user_id = None
        self.user_type = None
        self.crear_interfaz_inicio_sesion()

    def crear_interfaz_inicio_sesion(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg='#f0f0f0')
        frame.pack(padx=50, pady=50)

        tk.Label(frame, text="Nombre de usuario:", bg='#f0f0f0', font=('Arial', 12)).pack()
        self.username_entry = tk.Entry(frame, font=('Arial', 12), bd=2)
        self.username_entry.pack(pady=8)

        tk.Label(frame, text="Contraseña:", bg='#f0f0f0', font=('Arial', 12)).pack()
        self.password_entry = tk.Entry(frame, show="*", font=('Arial', 12), bd=2)
        self.password_entry.pack(pady=8)

        button_frame = tk.Frame(frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X, expand=True)
        tk.Button(button_frame, text="Iniciar sesión", command=self.intentar_inicio_sesion, relief='raised', bd=3, font=('Arial', 12)).pack(side=tk.LEFT, expand=True)
        tk.Button(button_frame, text="Registrar", command=lambda: crear_interfaz_registro(self.root, self.crear_interfaz_inicio_sesion, self.crear_interfaz_inicio_sesion), relief='raised', bd=3, font=('Arial', 12)).pack(side=tk.RIGHT, expand=True)

    def intentar_inicio_sesion(self):
        nombre_usuario = self.username_entry.get()
        contrasena = self.password_entry.get()
        if not nombre_usuario or not contrasena:
            messagebox.showerror("Error de Inicio de Sesión", "El nombre de usuario y la contraseña no pueden estar vacíos.")
            return

        usuario = validar_usuario(nombre_usuario, contrasena)
        if usuario:
            self.user_id = usuario[0]
            self.user_type = usuario[1]
            self.crear_interfaz_principal()
        else:
            messagebox.showerror("Error de Inicio de Sesión", "Nombre de usuario o contraseña incorrectos.")

    def crear_interfaz_principal(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Sistema de Mesa de Ayuda")
        self.root.geometry("1000x600")

        main_frame = tk.Frame(self.root, bg='#d0d0d0')
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.Frame(main_frame, bg='#e0e0e0', width=200)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        tk.Button(left_frame, text="Registrar Incidencia", command=self.crear_interfaz_registrar_incidencia, font=('Arial', 12)).pack(pady=10)
        tk.Button(left_frame, text="Incidencias", command=self.crear_interfaz_lista_incidencias, font=('Arial', 12)).pack(pady=10)
        tk.Button(left_frame, text="Asignaciones", command=self.crear_interfaz_lista_asignaciones, font=('Arial', 12)).pack(pady=10)
        tk.Button(left_frame, text="Usuarios", command=self.crear_interfaz_lista_usuarios, font=('Arial', 12)).pack(pady=10)
        tk.Button(left_frame, text="Asignar Incidencia", command=self.crear_interfaz_asignar_incidencia, font=('Arial', 12)).pack(pady=10)
        if self.user_type == 'Administrador':
            tk.Button(left_frame, text="Informes", command=self.crear_interfaz_lista_informes, font=('Arial', 12)).pack(pady=10)

        center_frame = tk.Frame(main_frame, bg='#ffffff')
        center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tk.Label(center_frame, text="Bienvenido al Sistema de Mesa de Ayuda", font=('Helvetica', 16), bg='#ffffff').pack(pady=20)

        img = Image.open("cliente.png")
        img = img.resize((100, 100), Image.LANCZOS)
        self.img_tk = ImageTk.PhotoImage(img)
        tk.Label(center_frame, image=self.img_tk, bg='#ffffff').pack(pady=10)

    def crear_interfaz_registrar_incidencia(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Registrar Incidencia")
        self.root.geometry("600x400")

        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20)

        tk.Label(frame, text="Título:", font=('Arial', 12)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.title_entry = tk.Entry(frame, font=('Arial', 12), width=40)
        self.title_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Descripción:", font=('Arial', 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.description_entry = tk.Entry(frame, font=('Arial', 12), width=40)
        self.description_entry.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Estado:", font=('Arial', 12)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.status_entry = tk.Entry(frame, font=('Arial', 12), width=40)
        self.status_entry.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="Fecha de Creación:", font=('Arial', 12)).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.creation_date_entry = DateEntry(frame, font=('Arial', 12), width=40, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.creation_date_entry.grid(row=3, column=1, pady=5)

        tk.Label(frame, text="Fecha de Actualización:", font=('Arial', 12)).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.update_date_entry = DateEntry(frame, font=('Arial', 12), width=40, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.update_date_entry.grid(row=4, column=1, pady=5)

        tk.Button(frame, text="Guardar Incidencia", command=self.guardar_incidencia, font=('Arial', 12)).grid(row=5, columnspan=2, pady=10)
        tk.Button(frame, text="Regresar", command=self.crear_interfaz_principal, font=('Arial', 12)).grid(row=6, columnspan=2, pady=10)

    def guardar_incidencia(self):
        titulo = self.title_entry.get()
        descripcion = self.description_entry.get()
        estado = self.status_entry.get()
        fecha_creacion = self.creation_date_entry.get_date().strftime('%Y-%m-%d')
        fecha_actualizacion = self.update_date_entry.get_date().strftime('%Y-%m-%d')
        if registrar_incidencia(titulo, descripcion, estado, fecha_creacion, fecha_actualizacion, self.user_id):
            messagebox.showinfo("Registro de Incidencia", "Incidencia registrada exitosamente.")
            self.crear_interfaz_principal()
        else:
            messagebox.showerror("Error", "No se pudo registrar la incidencia.")

    def crear_interfaz_lista_incidencias(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Lista de Incidencias")
        self.root.geometry("800x600")

        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        columnas = ("IDIncidencia", "Titulo", "Descripción", "Estado", "FechaCreacion", "FechaActualizacion", "IDUsuario")
        self.tree = ttk.Treeview(frame, columns=columnas, show='headings')
        self.tree.pack(fill=tk.BOTH, expand=True)

        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)

        self.cargar_incidencias()

        tk.Button(frame, text="Actualizar", command=self.actualizar_incidencia_gui, font=('Arial', 12)).pack(pady=10)
        tk.Button(frame, text="Borrar", command=self.borrar_incidencia, font=('Arial', 12)).pack(pady=10)
        tk.Button(frame, text="Regresar", command=self.crear_interfaz_principal, font=('Arial', 12)).pack(pady=10)

    def cargar_incidencias(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        incidencias = obtener_todas_las_incidencias()
        for incidencia in incidencias:
            self.tree.insert('', tk.END, values=incidencia)

    def actualizar_incidencia_gui(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una incidencia para actualizar.")
            return

        incidencia = self.tree.item(selected_item)['values']

        ventana_actualizar = tk.Toplevel(self.root)
        ventana_actualizar.title("Actualizar Incidencia")
        ventana_actualizar.geometry("400x300")

        tk.Label(ventana_actualizar, text="Título:", font=('Arial', 12)).grid(row=0, column=0, sticky=tk.W, pady=5)
        titulo_entry = tk.Entry(ventana_actualizar, font=('Arial', 12), width=30)
        titulo_entry.grid(row=0, column=1, pady=5)
        titulo_entry.insert(0, incidencia[1])

        tk.Label(ventana_actualizar, text="Descripción:", font=('Arial', 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        descripcion_entry = tk.Entry(ventana_actualizar, font=('Arial', 12), width=30)
        descripcion_entry.grid(row=1, column=1, pady=5)
        descripcion_entry.insert(0, incidencia[2])

        tk.Label(ventana_actualizar, text="Estado:", font=('Arial', 12)).grid(row=2, column=0, sticky=tk.W, pady=5)
        estado_entry = tk.Entry(ventana_actualizar, font=('Arial', 12), width=30)
        estado_entry.grid(row=2, column=1, pady=5)
        estado_entry.insert(0, incidencia[3])

        tk.Label(ventana_actualizar, text="Fecha de Actualización:", font=('Arial', 12)).grid(row=3, column=0, sticky=tk.W, pady=5)
        fecha_actualizacion_entry = DateEntry(ventana_actualizar, font=('Arial', 12), width=30, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        fecha_actualizacion_entry.grid(row=3, column=1, pady=5)
        fecha_actualizacion_entry.set_date(datetime.now())

        tk.Button(ventana_actualizar, text="Guardar Cambios", font=('Arial', 12), command=lambda: self.guardar_incidencia_actualizada(incidencia[0], titulo_entry.get(), descripcion_entry.get(), estado_entry.get(), fecha_actualizacion_entry.get_date().strftime('%Y-%m-%d'), ventana_actualizar)).grid(row=4, columnspan=2, pady=10)

    def guardar_incidencia_actualizada(self, id_incidencia, titulo, descripcion, estado, fecha_actualizacion, ventana):
        if actualizar_incidencia(id_incidencia, titulo, descripcion, estado, fecha_actualizacion):
            messagebox.showinfo("Actualizar Incidencia", "Incidencia actualizada exitosamente.")
            self.cargar_incidencias()
            ventana.destroy()
        else:
            messagebox.showerror("Error", "No se pudo actualizar la incidencia.")

    def borrar_incidencia(self):
        if self.user_type != 'Administrador':
            messagebox.showerror("Error", "Solo los administradores pueden borrar incidencias.")
            return

        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una incidencia para borrar.")
            return

        id_incidencia = self.tree.item(selected_item)['values'][0]
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea borrar esta incidencia?"):
            if borrar_incidencia(id_incidencia):
                messagebox.showinfo("Borrar Incidencia", "Incidencia borrada exitosamente.")
                self.cargar_incidencias()
            else:
                messagebox.showerror("Error", "No se pudo borrar la incidencia.")

    def crear_interfaz_lista_asignaciones(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Lista de Asignaciones")
        self.root.geometry("800x600")

        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        columnas = ("IDAsignacion", "IDIncidencia", "IDTecnico", "FechaAsignacion")
        self.assignment_tree = ttk.Treeview(frame, columns=columnas, show='headings')
        self.assignment_tree.pack(fill=tk.BOTH, expand=True)

        for col in columnas:
            self.assignment_tree.heading(col, text=col)
            self.assignment_tree.column(col, anchor=tk.CENTER)

        self.cargar_asignaciones()

        tk.Button(frame, text="Borrar Asignación", command=self.borrar_asignacion, font=('Arial', 12)).pack(pady=10)
        tk.Button(frame, text="Regresar", command=self.crear_interfaz_principal, font=('Arial', 12)).pack(pady=10)

    def cargar_asignaciones(self):
        for i in self.assignment_tree.get_children():
            self.assignment_tree.delete(i)
        asignaciones = obtener_todas_las_asignaciones()
        for asignacion in asignaciones:
            self.assignment_tree.insert('', tk.END, values=asignacion)

    def borrar_asignacion(self):
        if self.user_type != 'Administrador':
            messagebox.showerror("Error", "Solo los administradores pueden borrar asignaciones.")
            return

        selected_item = self.assignment_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una asignación para borrar.")
            return

        id_asignacion = self.assignment_tree.item(selected_item)['values'][0]
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea borrar esta asignación?"):
            if borrar_asignacion(id_asignacion):
                messagebox.showinfo("Borrar Asignación", "Asignación borrada exitosamente.")
                self.cargar_asignaciones()
            else:
                messagebox.showerror("Error", "No se pudo borrar la asignación.")

    def crear_interfaz_lista_usuarios(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Lista de Usuarios")
        self.root.geometry("800x600")

        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        columnas = ("IDUsuario", "Nombre", "Correo", "Tipo")
        self.user_tree = ttk.Treeview(frame, columns=columnas, show='headings')
        self.user_tree.pack(fill=tk.BOTH, expand=True)

        for col in columnas:
            self.user_tree.heading(col, text=col)
            self.user_tree.column(col, anchor=tk.CENTER)

        self.cargar_usuarios()

        tk.Button(frame, text="Borrar Usuario", command=self.borrar_usuario, font=('Arial', 12)).pack(pady=10)
        tk.Button(frame, text="Regresar", command=self.crear_interfaz_principal, font=('Arial', 12)).pack(pady=10)

    def cargar_usuarios(self):
        for i in self.user_tree.get_children():
            self.user_tree.delete(i)
        usuarios = obtener_todos_los_usuarios()
        for usuario in usuarios:
            self.user_tree.insert('', tk.END, values=usuario)

    def borrar_usuario(self):
        if self.user_type != 'Administrador':
            messagebox.showerror("Error", "Solo los administradores pueden borrar usuarios.")
            return

        selected_item = self.user_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un usuario para borrar.")
            return

        id_usuario = self.user_tree.item(selected_item)['values'][0]
        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea borrar este usuario?"):
            if borrar_usuario(id_usuario):
                messagebox.showinfo("Borrar Usuario", "Usuario borrado exitosamente.")
                self.cargar_usuarios()
            else:
                messagebox.showerror("Error", "No se pudo borrar el usuario.")

    def crear_interfaz_asignar_incidencia(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Asignar Incidencia")
        self.root.geometry("600x400")

        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20)

        tk.Label(frame, text="Seleccionar Incidencia:", font=('Arial', 12)).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.incidencia_combobox = ttk.Combobox(frame, font=('Arial', 12), width=37)
        self.incidencia_combobox.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Seleccionar Técnico:", font=('Arial', 12)).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.tecnico_combobox = ttk.Combobox(frame, font=('Arial', 12), width=37)
        self.tecnico_combobox.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Fecha de Asignación:", font=('Arial', 12)).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.fecha_asignacion_entry = DateEntry(frame, font=('Arial', 12), width=40, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.fecha_asignacion_entry.grid(row=2, column=1, pady=5)

        tk.Button(frame, text="Asignar Incidencia", command=self.asignar_incidencia, font=('Arial', 12)).grid(row=3, columnspan=2, pady=10)
        tk.Button(frame, text="Regresar", command=self.crear_interfaz_principal, font=('Arial', 12)).grid(row=4, columnspan=2, pady=10)

        self.cargar_incidencias_y_tecnicos()

    def cargar_incidencias_y_tecnicos(self):
        incidencias = obtener_todas_las_incidencias()
        tecnicos = obtener_todos_los_tecnicos()

        self.incidencia_combobox['values'] = [f"{incidencia[0]} - {incidencia[1]}" for incidencia in incidencias]
        self.tecnico_combobox['values'] = [f"{tecnico[0]} - {tecnico[1]}" for tecnico in tecnicos]

    def asignar_incidencia(self):
        incidencia_seleccionada = self.incidencia_combobox.get().split(' - ')[0]
        tecnico_seleccionado = self.tecnico_combobox.get().split(' - ')[0]
        fecha_asignacion = self.fecha_asignacion_entry.get_date().strftime('%Y-%m-%d')

        if not incidencia_seleccionada or not tecnico_seleccionado or not fecha_asignacion:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if registrar_asignacion(incidencia_seleccionada, tecnico_seleccionado, fecha_asignacion):
            messagebox.showinfo("Asignación", "Incidencia asignada exitosamente.")
            self.crear_interfaz_principal()
        else:
            messagebox.showerror("Error", "No se pudo asignar la incidencia.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()
