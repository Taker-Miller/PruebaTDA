import tkinter as tk
from tkinter import ttk, messagebox
from logica import (
    validar_usuario, crear_usuario, desactivar_usuario, 
    obtener_todos_los_tiques, filtrar_tiques, asignar_tique_a_area, registrar_tique, obtener_ejecutivos, obtener_usuarios_activos, obtener_usuarios_desactivados, reactivar_usuario, enviar_notificacion_email, enviar_notificacion_sms, obtener_tiques_por_area, agregar_observacion_y_cerrar_tique, actualizar_estado_tique, asignar_tique_a_varios_ejecutivos
)
import re

class SistemaDeAyuda:
    def __init__(self, root, tipo_usuario, area_especializada=None):
        self.root = root
        self.tipo_usuario = tipo_usuario
        self.area_especializada = area_especializada
        self.root.title("Sistema de Gestión de Tiques")
        self.menu = None
        self.tabla_tiques = None
        self.crear_interfaz_principal()

    def crear_interfaz_principal(self):
        self.root.geometry("1200x700")
        if self.menu is not None:
            self.menu.destroy()
        self.menu = ttk.Notebook(self.root)
        
        if self.tipo_usuario == "Administrador":
            self.crear_interfaz_administrador(self.menu)
        elif self.tipo_usuario == "Usuario":
            self.crear_interfaz_usuario(self.menu)
        elif self.tipo_usuario == "Técnico de Soporte":
            self.crear_interfaz_tecnico(self.menu)
        elif self.tipo_usuario == "Mesa de Ayuda":
            self.crear_interfaz_ejecutivo(self.menu)
        elif self.tipo_usuario == "Área":
            self.crear_interfaz_ejecutivo_area(self.menu)
        elif self.tipo_usuario == "Jefe de Mesa":
            self.crear_interfaz_jefe_mesa(self.menu)
        
        self.menu.pack(expand=1, fill="both")

    def crear_interfaz_administrador(self, menu):
        tab_admin = ttk.Frame(menu)
        menu.add(tab_admin, text='Administrador')
        
        ttk.Label(tab_admin, text="Gestión de Tiques - Administrador", font=("Arial", 16)).pack(pady=10)
        
        self.tabla_tiques = ttk.Treeview(tab_admin, columns=("ID", "NombreCliente", "FechaCreacion", "TipoTique", "Criticidad", "AreaDestino", "Estado"), show="headings")
        self.tabla_tiques.heading("ID", text="ID", command=lambda: self.ordenar_tabla("ID", False))
        self.tabla_tiques.heading("NombreCliente", text="Nombre del Cliente", command=lambda: self.ordenar_tabla("NombreCliente", False))
        self.tabla_tiques.heading("FechaCreacion", text="Fecha de Creación", command=lambda: self.ordenar_tabla("FechaCreacion", False))
        self.tabla_tiques.heading("TipoTique", text="Tipo de Tique", command=lambda: self.ordenar_tabla("TipoTique", False))
        self.tabla_tiques.heading("Criticidad", text="Criticidad", command=lambda: self.ordenar_tabla("Criticidad", False))
        self.tabla_tiques.heading("AreaDestino", text="Área de Destino", command=lambda: self.ordenar_tabla("AreaDestino", False))
        self.tabla_tiques.heading("Estado", text="Estado", command=lambda: self.ordenar_tabla("Estado", False))
        self.tabla_tiques.pack(fill=tk.BOTH, expand=True)
        
        self.cargar_tiques()

        self.filtros_frame = ttk.Frame(tab_admin)
        self.filtros_frame.pack(pady=10)

        ttk.Label(self.filtros_frame, text="Fecha específica:").grid(row=0, column=0)
        self.filtro_fecha = ttk.Entry(self.filtros_frame)
        self.filtro_fecha.grid(row=0, column=1)

        ttk.Label(self.filtros_frame, text="Criticidad:").grid(row=1, column=0)
        self.filtro_criticidad = ttk.Entry(self.filtros_frame)
        self.filtro_criticidad.grid(row=1, column=1)

        ttk.Label(self.filtros_frame, text="Tipo:").grid(row=2, column=0)
        self.filtro_tipo = ttk.Entry(self.filtros_frame)
        self.filtro_tipo.grid(row=2, column=1)

        ttk.Label(self.filtros_frame, text="Abierto por:").grid(row=3, column=0)
        self.filtro_abierto_por = ttk.Entry(self.filtros_frame)
        self.filtro_abierto_por.grid(row=3, column=1)

        ttk.Label(self.filtros_frame, text="Cerrado por:").grid(row=4, column=0)
        self.filtro_cerrado_por = ttk.Entry(self.filtros_frame)
        self.filtro_cerrado_por.grid(row=4, column=1)

        ttk.Label(self.filtros_frame, text="Área:").grid(row=5, column=0)
        self.filtro_area = ttk.Entry(self.filtros_frame)
        self.filtro_area.grid(row=5, column=1)

        ttk.Button(self.filtros_frame, text="Filtrar", command=self.filtrar_tiques).grid(row=6, columnspan=2, pady=10)

        ttk.Button(tab_admin, text="Asignar Tique a Área", command=self.mostrar_asignar_area).pack(pady=5)
        ttk.Button(tab_admin, text="Crear Usuario", command=self.mostrar_crear_usuario).pack(pady=5)
        ttk.Button(tab_admin, text="Desactivar Usuario", command=self.mostrar_desactivar_usuario).pack(pady=5)
        ttk.Button(tab_admin, text="Reactivar Usuario", command=self.mostrar_reactivar_usuario).pack(pady=5)

    def mostrar_crear_usuario(self):
        self.crear_usuario_window = tk.Toplevel(self.root)
        self.crear_usuario_window.title("Crear Usuario")

        ttk.Label(self.crear_usuario_window, text="Nombre de Usuario:").pack(pady=10)
        self.usuario_entry = ttk.Entry(self.crear_usuario_window)
        self.usuario_entry.pack(pady=10)

        ttk.Label(self.crear_usuario_window, text="Correo:").pack(pady=10)
        self.correo_entry = ttk.Entry(self.crear_usuario_window)
        self.correo_entry.pack(pady=10)

        ttk.Label(self.crear_usuario_window, text="Contraseña:").pack(pady=10)
        self.contrasena_entry = ttk.Entry(self.crear_usuario_window, show="*")
        self.contrasena_entry.pack(pady=10)

        ttk.Label(self.crear_usuario_window, text="Rol:").pack(pady=10)
        self.rol_combobox = ttk.Combobox(self.crear_usuario_window, values=["Administrador", "Mesa de Ayuda", "Técnico de Soporte", "Área", "Usuario"])
        self.rol_combobox.pack(pady=10)

        ttk.Label(self.crear_usuario_window, text="Código de acceso (solo para roles específicos):").pack(pady=10)
        self.codigo_acceso_entry = ttk.Entry(self.crear_usuario_window, show="*")
        self.codigo_acceso_entry.pack(pady=10)

        ttk.Button(self.crear_usuario_window, text="Crear Usuario", command=self.crear_usuario).pack(pady=10)

    def crear_usuario(self):
        nombre_usuario = self.usuario_entry.get()
        correo = self.correo_entry.get()
        contrasena = self.contrasena_entry.get()
        rol = self.rol_combobox.get()
        codigo_acceso = self.codigo_acceso_entry.get()

        if not nombre_usuario or not correo or not contrasena or not rol:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if rol in ["Administrador", "Mesa de Ayuda", "Técnico de Soporte", "Área"] and codigo_acceso != "1234":
            messagebox.showerror("Error", "Código de acceso incorrecto.")
            return

        if crear_usuario(nombre_usuario, correo, contrasena, rol):
            messagebox.showinfo("Éxito", "Usuario creado exitosamente.")
            self.crear_usuario_window.destroy()
        else:
            messagebox.showerror("Error", "No se pudo crear el usuario.")

    def crear_interfaz_usuario(self, menu):
        tab_usuario = ttk.Frame(menu)
        menu.add(tab_usuario, text='Usuario')

        ttk.Label(tab_usuario, text="Portal de Usuario", font=("Arial", 16)).pack(pady=10)
        ttk.Button(tab_usuario, text="Crear Tique", command=self.crear_tique).pack(pady=5)
        ttk.Button(tab_usuario, text="Cerrar Sesión", command=self.cerrar_sesion).pack(pady=5)

    def crear_interfaz_tecnico(self, menu):
        tab_tecnico = ttk.Frame(menu)
        menu.add(tab_tecnico, text='Técnico de Soporte')

        ttk.Label(tab_tecnico, text="Gestión de Tiques - Técnico de Soporte", font=("Arial", 16)).pack(pady=10)
        self.tabla_tiques = ttk.Treeview(tab_tecnico, columns=("ID", "NombreCliente", "FechaCreacion", "TipoTique", "Criticidad", "AreaDestino", "Estado"), show="headings")
        self.tabla_tiques.heading("ID", text="ID")
        self.tabla_tiques.heading("NombreCliente", text="Nombre del Cliente")
        self.tabla_tiques.heading("FechaCreacion", text="Fecha de Creación")
        self.tabla_tiques.heading("TipoTique", text="Tipo de Tique")
        self.tabla_tiques.heading("Criticidad", text="Criticidad")
        self.tabla_tiques.heading("AreaDestino", text="Área de Destino")
        self.tabla_tiques.heading("Estado", text="Estado")
        self.tabla_tiques.pack(fill=tk.BOTH, expand=True)

        self.cargar_tiques_area()

        ttk.Button(tab_tecnico, text="Agregar Observación y Cerrar Tique", command=self.mostrar_agregar_observacion).pack(pady=5)
        ttk.Button(tab_tecnico, text="Asignar a Ejecutivos", command=self.mostrar_asignar_ejecutivos).pack(pady=5)
        ttk.Button(tab_tecnico, text="Cerrar Sesión", command=self.cerrar_sesion).pack(pady=5)

    def crear_interfaz_ejecutivo(self, menu):
        tab_ejecutivo = ttk.Frame(menu)
        menu.add(tab_ejecutivo, text='Mesa de Ayuda')

        ttk.Label(tab_ejecutivo, text="Ejecutivo de Mesa de Ayuda", font=("Arial", 16)).pack(pady=10)
        self.tabla_tiques = ttk.Treeview(tab_ejecutivo, columns=("ID", "NombreCliente", "FechaCreacion", "TipoTique", "Criticidad", "AreaDestino", "Estado"), show="headings")
        self.tabla_tiques.heading("ID", text="ID")
        self.tabla_tiques.heading("NombreCliente", text="Nombre del Cliente")
        self.tabla_tiques.heading("FechaCreacion", text="Fecha de Creación")
        self.tabla_tiques.heading("TipoTique", text="Tipo de Tique")
        self.tabla_tiques.heading("Criticidad", text="Criticidad")
        self.tabla_tiques.heading("AreaDestino", text="Área de Destino")
        self.tabla_tiques.heading("Estado", text="Estado")
        self.tabla_tiques.pack(fill=tk.BOTH, expand=True)

        self.cargar_tiques_area()

        ttk.Button(tab_ejecutivo, text="Crear Tique", command=self.crear_tique).pack(pady=5)
        ttk.Button(tab_ejecutivo, text="Asignar Tique a Área", command=self.mostrar_asignar_area).pack(pady=5)
        ttk.Button(tab_ejecutivo, text="Cerrar Sesión", command=self.cerrar_sesion).pack(pady=5)

    def crear_interfaz_ejecutivo_area(self, menu):
        tab_ejecutivo_area = ttk.Frame(menu)
        menu.add(tab_ejecutivo_area, text='Área')

        ttk.Label(tab_ejecutivo_area, text="Ejecutivo del Área Específica", font=("Arial", 16)).pack(pady=10)
        self.tabla_tiques = ttk.Treeview(tab_ejecutivo_area, columns=("ID", "NombreCliente", "FechaCreacion", "TipoTique", "Criticidad", "AreaDestino", "Estado"), show="headings")
        self.tabla_tiques.heading("ID", text="ID")
        self.tabla_tiques.heading("NombreCliente", text="Nombre del Cliente")
        self.tabla_tiques.heading("FechaCreacion", text="Fecha de Creación")
        self.tabla_tiques.heading("TipoTique", text="Tipo de Tique")
        self.tabla_tiques.heading("Criticidad", text="Criticidad")
        self.tabla_tiques.heading("AreaDestino", text="Área de Destino")
        self.tabla_tiques.heading("Estado", text="Estado")
        self.tabla_tiques.pack(fill=tk.BOTH, expand=True)

        self.cargar_tiques_area()

        ttk.Button(tab_ejecutivo_area, text="Agregar Observación y Cerrar Tique", command=self.mostrar_agregar_observacion).pack(pady=5)
        ttk.Button(tab_ejecutivo_area, text="Cambiar Estado del Tique", command=self.mostrar_cambiar_estado).pack(pady=5)
        ttk.Button(tab_ejecutivo_area, text="Asignar a Ejecutivos", command=self.mostrar_asignar_ejecutivos).pack(pady=5)
        ttk.Button(tab_ejecutivo_area, text="Cerrar Sesión", command=self.cerrar_sesion).pack(pady=5)

    def crear_interfaz_jefe_mesa(self, menu):
        tab_jefe_mesa = ttk.Frame(menu)
        menu.add(tab_jefe_mesa, text='Jefe de Mesa')

        ttk.Label(tab_jefe_mesa, text="Jefe de Mesa", font=("Arial", 16)).pack(pady=10)
        ttk.Button(tab_jefe_mesa, text="Crear Usuario", command=self.mostrar_crear_usuario).pack(pady=5)
        ttk.Button(tab_jefe_mesa, text="Desactivar Usuario", command=self.mostrar_desactivar_usuario).pack(pady=5)
        ttk.Button(tab_jefe_mesa, text="Reactivar Usuario", command=self.mostrar_reactivar_usuario).pack(pady=5)
        ttk.Button(tab_jefe_mesa, text="Cerrar Sesión", command=self.cerrar_sesion).pack(pady=5)

    def cargar_tiques(self):
        if self.tabla_tiques:
            for row in self.tabla_tiques.get_children():
                self.tabla_tiques.delete(row)
            tiques = obtener_todos_los_tiques()
            if isinstance(tiques, list) and tiques:
                for tique in tiques:
                    self.tabla_tiques.insert("", tk.END, values=tique)
            else:
                messagebox.showerror("Error", "No se pudo cargar los tiques o no hay tiques disponibles.")

    def cargar_tiques_area(self):
        if self.tabla_tiques:
            for row in self.tabla_tiques.get_children():
                self.tabla_tiques.delete(row)
            tiques = obtener_tiques_por_area(self.area_especializada)
            if isinstance(tiques, list) and tiques:
                for tique in tiques:
                    self.tabla_tiques.insert("", tk.END, values=tique)
            else:
                messagebox.showerror("Error", "No se pudo cargar los tiques o no hay tiques disponibles.")

    def ordenar_tabla(self, col, reverse):
        datos = [(self.tabla_tiques.set(k, col), k) for k in self.tabla_tiques.get_children('')]
        datos.sort(reverse=reverse)
        for index, (val, k) in enumerate(datos):
            self.tabla_tiques.move(k, '', index)
        self.tabla_tiques.heading(col, command=lambda: self.ordenar_tabla(col, not reverse))

    def mostrar_asignar_area(self):
        if not self.tabla_tiques:
            messagebox.showerror("Error", "No hay tiques disponibles para asignar.")
            return
        
        selected_item = self.tabla_tiques.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, selecciona un tique para asignar.")
            return
        
        tique_id = self.tabla_tiques.item(selected_item)["values"][0]
        
        self.asignar_area_window = tk.Toplevel(self.root)
        self.asignar_area_window.title("Asignar Tique a Área")

        ttk.Label(self.asignar_area_window, text="Área de Destino:").pack(pady=10)
        self.area_entry = ttk.Entry(self.asignar_area_window)
        self.area_entry.pack(pady=10)

        ttk.Button(self.asignar_area_window, text="Asignar", command=lambda: self.asignar_area(tique_id)).pack(pady=10)

    def asignar_area(self, tique_id):
        area_destino = self.area_entry.get()
        if not area_destino:
            messagebox.showerror("Error", "El campo de área de destino no puede estar vacío.")
            return
        
        if asignar_tique_a_area(tique_id, area_destino):
            messagebox.showinfo("Éxito", "Tique asignado exitosamente.")
            self.asignar_area_window.destroy()
            self.cargar_tiques()
        else:
            messagebox.showerror("Error", "No se pudo asignar el tique a un área.")

    def mostrar_desactivar_usuario(self):
        usuarios = obtener_usuarios_activos()
        if not usuarios:
            messagebox.showerror("Error", "No hay usuarios activos para desactivar.")
            return

        self.desactivar_usuario_window = tk.Toplevel(self.root)
        self.desactivar_usuario_window.title("Desactivar Usuario")

        ttk.Label(self.desactivar_usuario_window, text="Nombre de Usuario:").pack(pady=10)
        self.usuario_combobox = ttk.Combobox(self.desactivar_usuario_window, values=[usuario[0] for usuario in usuarios])
        self.usuario_combobox.pack(pady=10)

        ttk.Button(self.desactivar_usuario_window, text="Desactivar", command=self.desactivar_usuario).pack(pady=10)

    def desactivar_usuario(self):
        nombre_usuario = self.usuario_combobox.get()
        if not nombre_usuario:
            messagebox.showerror("Error", "Por favor, selecciona un usuario.")
            return
        
        if desactivar_usuario(nombre_usuario):
            messagebox.showinfo("Éxito", "Usuario desactivado exitosamente.")
            self.desactivar_usuario_window.destroy()
        else:
            messagebox.showerror("Error", "No se pudo desactivar el usuario.")

    def mostrar_reactivar_usuario(self):
        usuarios = obtener_usuarios_desactivados()
        if not usuarios:
            messagebox.showerror("Error", "No hay usuarios desactivados para reactivar.")
            return

        self.reactivar_usuario_window = tk.Toplevel(self.root)
        self.reactivar_usuario_window.title("Reactivar Usuario")

        ttk.Label(self.reactivar_usuario_window, text="Nombre de Usuario:").pack(pady=10)
        self.usuario_combobox = ttk.Combobox(self.reactivar_usuario_window, values=[usuario[0] for usuario in usuarios])
        self.usuario_combobox.pack(pady=10)

        ttk.Button(self.reactivar_usuario_window, text="Reactivar", command=self.reactivar_usuario).pack(pady=10)

    def reactivar_usuario(self):
        nombre_usuario = self.usuario_combobox.get()
        if not nombre_usuario:
            messagebox.showerror("Error", "Por favor, selecciona un usuario.")
            return
        
        if reactivar_usuario(nombre_usuario):
            messagebox.showinfo("Éxito", "Usuario reactivado exitosamente.")
            self.reactivar_usuario_window.destroy()
        else:
            messagebox.showerror("Error", "No se pudo reactivar el usuario.")

    def filtrar_tiques(self):
        fecha = self.filtro_fecha.get()
        criticidad = self.filtro_criticidad.get()
        tipo = self.filtro_tipo.get()
        abierto_por = self.filtro_abierto_por.get()
        cerrado_por = self.filtro_cerrado_por.get()
        area = self.filtro_area.get()
        tiques = filtrar_tiques(fecha, criticidad, tipo, abierto_por, cerrado_por, area)
        for row in self.tabla_tiques.get_children():
            self.tabla_tiques.delete(row)
        for tique in tiques:
            self.tabla_tiques.insert("", tk.END, values=tique)

    def crear_tique(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(self.frame, text="Crear Tique", font=("Arial", 16)).pack(pady=10)

        self.campos = [
            ("nombre_cliente", "Nombre del cliente", ttk.Entry),
            ("rut", "Rut", ttk.Entry),
            ("telefono", "Teléfono", ttk.Entry),
            ("email", "Correo electrónico", ttk.Entry),
            ("tipo_tique", "Tipo de tique", ttk.Combobox, ["Felicitación", "Consulta", "Reclamo", "Problema"]),
            ("criticidad", "Criticidad", ttk.Combobox, ["Alta", "Media", "Baja"]),
            ("detalle_servicio", "Detalle del servicio", ttk.Entry),
            ("detalle_problema", "Detalle del problema", ttk.Entry),
            ("area_destino", "Área para derivar", ttk.Combobox, ["Mesa de Ayuda", "Técnico de Soporte", "Área"]),
            ("ejecutivo", "Ejecutivo", ttk.Combobox, self.obtener_lista_ejecutivos())
        ]

        self.entries = {}
        for key, label_text, widget, *options in self.campos:
            ttk.Label(self.frame, text=label_text).pack(pady=5)
            if options:
                entry = widget(self.frame, values=options[0])
            else:
                entry = widget(self.frame)
            entry.pack()
            self.entries[key] = entry

        ttk.Button(self.frame, text="Previsualizar", command=self.previsualizar_tique).pack(pady=20)
        ttk.Button(self.frame, text="Volver", command=self.volver_a_portal_usuario).pack(pady=10)

    def obtener_lista_ejecutivos(self):
        ejecutivos = obtener_ejecutivos()
        return [ejecutivo[0] for ejecutivo in ejecutivos]

    def previsualizar_tique(self):
        tique_data = {key: entry.get() for key, entry in self.entries.items()}
        if any(not value for value in tique_data.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        
        if not re.match(r'^\d{7,8}-[kK\d]$', tique_data["rut"]):
            messagebox.showerror("Error", "El RUT debe tener el formato 12345678-9.")
            return

        if not tique_data["telefono"].isdigit() or len(tique_data["telefono"]) != 9:
            messagebox.showerror("Error", "El teléfono debe ser numérico y tener 9 dígitos.")
            return

        preview_window = tk.Toplevel(self.root)
        preview_window.title("Previsualización del Tique")
        
        frame = ttk.Frame(preview_window, padding="10 10 10 10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        for key, value in tique_data.items():
            ttk.Label(frame, text=f"{key.replace('_', ' ').capitalize()}: {value}").pack(pady=5)
        
        ttk.Button(frame, text="Confirmar y Enviar", command=lambda: self.enviar_tique(tique_data, preview_window)).pack(pady=20)
        ttk.Button(frame, text="Cerrar", command=preview_window.destroy).pack(pady=10)

    def enviar_tique(self, tique_data, preview_window):
        preview_window.destroy()
        if registrar_tique(**tique_data):
            messagebox.showinfo("Éxito", "Tique registrado exitosamente.")
            self.volver_a_portal_usuario()
        else:
            messagebox.showerror("Error", "No se pudo registrar el tique.")

    def mostrar_agregar_observacion(self):
        if not self.tabla_tiques:
            messagebox.showerror("Error", "No hay tiques disponibles.")
            return

        selected_item = self.tabla_tiques.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, selecciona un tique para agregar observación.")
            return
        
        tique_id = self.tabla_tiques.item(selected_item)["values"][0]
        
        self.agregar_observacion_window = tk.Toplevel(self.root)
        self.agregar_observacion_window.title("Agregar Observación y Cerrar Tique")

        ttk.Label(self.agregar_observacion_window, text="Observación:").pack(pady=10)
        self.observacion_entry = ttk.Entry(self.agregar_observacion_window)
        self.observacion_entry.pack(pady=10)

        ttk.Label(self.agregar_observacion_window, text="Estado:").pack(pady=10)
        self.estado_combobox = ttk.Combobox(self.agregar_observacion_window, values=["Resuelto", "No aplicable"])
        self.estado_combobox.pack(pady=10)

        ttk.Button(self.agregar_observacion_window, text="Agregar Observación y Cerrar", command=lambda: self.agregar_observacion_y_cerrar(tique_id)).pack(pady=10)

    def agregar_observacion_y_cerrar(self, tique_id):
        observacion = self.observacion_entry.get()
        estado = self.estado_combobox.get()
        if not observacion or not estado:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        
        if agregar_observacion_y_cerrar_tique(tique_id, observacion, estado):
            messagebox.showinfo("Éxito", "Observación agregada y tique cerrado exitosamente.")
            self.agregar_observacion_window.destroy()
            self.cargar_tiques_area()
        else:
            messagebox.showerror("Error", "No se pudo agregar la observación y cerrar el tique.")

    def mostrar_asignar_ejecutivos(self):
        if not self.tabla_tiques:
            messagebox.showerror("Error", "No hay tiques disponibles.")
            return
        
        selected_item = self.tabla_tiques.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, selecciona un tique para asignar.")
            return
        
        tique_id = self.tabla_tiques.item(selected_item)["values"][0]
        
        self.asignar_ejecutivos_window = tk.Toplevel(self.root)
        self.asignar_ejecutivos_window.title("Asignar Tique a Ejecutivos")

        ttk.Label(self.asignar_ejecutivos_window, text="Ejecutivos:").pack(pady=10)
        self.ejecutivos_listbox = tk.Listbox(self.asignar_ejecutivos_window, selectmode=tk.MULTIPLE)
        for ejecutivo in self.obtener_lista_ejecutivos():
            self.ejecutivos_listbox.insert(tk.END, ejecutivo)
        self.ejecutivos_listbox.pack(pady=10)

        ttk.Button(self.asignar_ejecutivos_window, text="Asignar", command=lambda: self.asignar_ejecutivos(tique_id)).pack(pady=10)

    def asignar_ejecutivos(self, tique_id):
        seleccionados = self.ejecutivos_listbox.curselection()
        ejecutivos = [self.ejecutivos_listbox.get(i) for i in seleccionados]
        if not ejecutivos:
            messagebox.showerror("Error", "Por favor, selecciona al menos un ejecutivo.")
            return
        
        if asignar_tique_a_varios_ejecutivos(tique_id, ejecutivos):
            messagebox.showinfo("Éxito", "Tique asignado a ejecutivos exitosamente.")
            self.asignar_ejecutivos_window.destroy()
            self.cargar_tiques_area()
        else:
            messagebox.showerror("Error", "No se pudo asignar el tique a los ejecutivos.")

    def mostrar_cambiar_estado(self):
        if not self.tabla_tiques:
            messagebox.showerror("Error", "No hay tiques disponibles.")
            return

        selected_item = self.tabla_tiques.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, selecciona un tique para cambiar el estado.")
            return

        tique_id = self.tabla_tiques.item(selected_item)["values"][0]

        self.cambiar_estado_window = tk.Toplevel(self.root)
        self.cambiar_estado_window.title("Cambiar Estado del Tique")

        ttk.Label(self.cambiar_estado_window, text="Estado:").pack(pady=10)
        self.estado_combobox = ttk.Combobox(self.cambiar_estado_window, values=["Resuelto", "No aplicable"])
        self.estado_combobox.pack(pady=10)

        ttk.Button(self.cambiar_estado_window, text="Cambiar Estado", command=lambda: self.cambiar_estado(tique_id)).pack(pady=10)

    def cambiar_estado(self, tique_id):
        estado = self.estado_combobox.get()
        if not estado:
            messagebox.showerror("Error", "El campo de estado no puede estar vacío.")
            return

        if actualizar_estado_tique(tique_id, estado):
            messagebox.showinfo("Éxito", "Estado del tique actualizado exitosamente.")
            self.cambiar_estado_window.destroy()
            self.cargar_tiques_area()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el estado del tique.")

    def cerrar_sesion(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        LoginRegistro(self.root, self.launch_main_app)

    def volver_a_portal_usuario(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.crear_interfaz_principal()

    def launch_main_app(self, tipo_usuario, area_especializada=None):
        for widget in self.root.winfo_children():
            widget.destroy()
        SistemaDeAyuda(self.root, tipo_usuario, area_especializada)

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
        self.menu = tk.Menu(self.menu_button, tearoff=0)
        self.menu_button["menu"] = self.menu
        self.codigo_entry = tk.StringVar()
        self.codigo_acceso_entry = None
        self.roles = ["Administrador", "Área", "Jefe de Mesa", "Mesa de Ayuda", "Técnico de Soporte", "Usuario"]
        for rol in self.roles:
            self.menu.add_radiobutton(label=rol, variable=self.codigo_entry, value=rol, command=self.actualizar_seleccion_rol)
        self.menu_button.pack(pady=10)

        self.iniciar_sesion_button = ttk.Button(self.frame, text="Iniciar Sesión", command=self.iniciar_sesion)
        self.iniciar_sesion_button.pack(pady=20)
        ttk.Button(self.frame, text="Registrar", command=self.crear_interfaz_registro).pack(pady=10)

    def actualizar_seleccion_rol(self):
        seleccion = self.codigo_entry.get()
        self.menu_button.config(text=seleccion)
        
        if seleccion in ["Administrador", "Área", "Jefe de Mesa", "Mesa de Ayuda", "Técnico de Soporte"]:
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
            if tipo_usuario in ["Técnico de Soporte", "Área"]:
                area_especializada = tipo_usuario
                self.launch_main_app(tipo_usuario, area_especializada)
            else:
                self.launch_main_app(tipo_usuario)
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
        self.menu = tk.Menu(self.menu_button, tearoff=0)
        self.menu_button["menu"] = self.menu
        self.codigo_registro_entry = tk.StringVar()
        self.codigo_acceso_registro_entry = None
        for rol in self.roles:
            self.menu.add_radiobutton(label=rol, variable=self.codigo_registro_entry, value=rol, command=self.actualizar_seleccion_rol_registro)
        self.menu_button.pack(pady=10)

        self.registrar_button = ttk.Button(self.frame, text="Registrar", command=self.registrar_usuario)
        self.registrar_button.pack(pady=20)
        ttk.Button(self.frame, text="Volver al inicio", command=self.crear_interfaz_login).pack(pady=10)

    def actualizar_seleccion_rol_registro(self):
        seleccion = self.codigo_registro_entry.get()
        self.menu_button.config(text=seleccion)

        if seleccion in ["Administrador", "Área", "Jefe de Mesa", "Mesa de Ayuda", "Técnico de Soporte"]:
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

        if rol in ["Administrador", "Área", "Jefe de Mesa", "Mesa de Ayuda", "Técnico de Soporte"] and codigo_acceso != "1234":
            messagebox.showerror("Error", "Código de acceso incorrecto.")
            return

        if crear_usuario(usuario, correo, contraseña, rol):
            messagebox.showinfo("Registro", "Usuario registrado exitosamente.")
            self.crear_interfaz_login()
        else:
            messagebox.showerror("Error", "No se pudo registrar el usuario.")

if __name__ == "__main__":
    root = tk.Tk()
    def launch_main_app(tipo_usuario, area_especializada=None):
        for widget in root.winfo_children():
            widget.destroy()
       
