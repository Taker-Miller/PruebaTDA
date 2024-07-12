import mysql.connector
from mysql.connector import Error
from datetime import datetime

def crear_conexion():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='ticket'
    )

def ejecutar_query(query, params=None):
    conn = crear_conexion()
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        if query.strip().upper().startswith("SELECT"):
            result = cursor.fetchall()
            return result
        conn.commit()
        return True
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def validar_usuario(nombre_usuario, contrasena, tipo, codigo_acceso=None):
    query = "SELECT * FROM usuarios WHERE Nombre = %s AND Contraseña = %s AND Tipo = %s"
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute(query, (nombre_usuario, contrasena, tipo))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    if not usuario:
        return False, None
    if tipo != "Usuario" and codigo_acceso != "1234":
        return False, None
    return True, tipo

def crear_usuario(nombre, correo, contrasena, tipo):
    query = "INSERT INTO usuarios (Nombre, Correo, Contraseña, Tipo) VALUES (%s, %s, %s, %s)"
    return ejecutar_query(query, (nombre, correo, contrasena, tipo))

def desactivar_usuario(nombre_usuario):
    query = "UPDATE usuarios SET Activo = 0 WHERE Nombre = %s"
    return ejecutar_query(query, (nombre_usuario,))

def obtener_usuarios_activos():
    query = "SELECT Nombre FROM usuarios WHERE Activo = 1"
    return ejecutar_query(query)

def obtener_usuarios_desactivados():
    query = "SELECT Nombre FROM usuarios WHERE Activo = 0"
    return ejecutar_query(query)

def reactivar_usuario(nombre_usuario):
    query = "UPDATE usuarios SET Activo = 1 WHERE Nombre = %s"
    return ejecutar_query(query, (nombre_usuario,))

def obtener_todos_los_tiques():
    query = "SELECT IDTique, NombreCliente, FechaCreacion, TipoTique, Criticidad, AreaDestino, Estado FROM tiques"
    return ejecutar_query(query)

def obtener_tiques_por_area(area):
    query = "SELECT IDTique, NombreCliente, FechaCreacion, TipoTique, Criticidad, AreaDestino, Estado FROM tiques WHERE AreaDestino = %s"
    return ejecutar_query(query, (area,))

def asignar_tique_a_area(id_tique, area):
    query = "UPDATE tiques SET AreaDestino = %s, Estado = 'A resolución' WHERE IDTique = %s"
    return ejecutar_query(query, (area, id_tique))

def agregar_observacion_y_cerrar_tique(id_tique, observacion, estado):
    query = "UPDATE tiques SET Observacion = %s, Estado = %s WHERE IDTique = %s"
    return ejecutar_query(query, (observacion, estado, id_tique))

def actualizar_estado_tique(id_tique, estado):
    query = "UPDATE tiques SET Estado = %s WHERE IDTique = %s"
    return ejecutar_query(query, (estado, id_tique))

def asignar_tique_a_varios_ejecutivos(id_tique, ejecutivos):
    for ejecutivo in ejecutivos:
        query = "INSERT INTO asignaciones (IDTique, IDEjecutivo) VALUES (%s, %s)"
        if not ejecutar_query(query, (id_tique, ejecutivo)):
            return False
    return True

def registrar_tique(nombre_cliente, rut, telefono, email, tipo_tique, criticidad, detalle_servicio, detalle_problema, area_destino, ejecutivo):
    query = """
    INSERT INTO tiques (NombreCliente, Rut, Telefono, Email, TipoTique, Criticidad, DetalleServicio, DetalleProblema, AreaDestino, Ejecutivo)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    return ejecutar_query(query, (nombre_cliente, rut, telefono, email, tipo_tique, criticidad, detalle_servicio, detalle_problema, area_destino, ejecutivo))

def obtener_ejecutivos():
    query = "SELECT Nombre FROM usuarios WHERE Tipo = 'Ejecutivo de Área' OR Tipo = 'Ejecutivo de Mesa de Ayuda'"
    return ejecutar_query(query)

def filtrar_tiques(fecha=None, criticidad=None, tipo=None, abierto_por=None, cerrado_por=None, area=None):
    query = "SELECT * FROM tiques WHERE True"
    params = []
    if fecha:
        query += " AND FechaCreacion = %s"
        params.append(fecha)
    if criticidad:
        query += " AND Criticidad = %s"
        params.append(criticidad)
    if tipo:
        query += " AND TipoTique = %s"
        params.append(tipo)
    if abierto_por:
        query += " AND AbiertoPor = %s"
        params.append(abierto_por)
    if cerrado_por:
        query += " AND CerradoPor = %s"
        params.append(cerrado_por)
    if area:
        query += " AND AreaDestino = %s"
        params.append(area)
    return ejecutar_query(query, params)

def enviar_notificacion_email(destinatario, mensaje):
    print(f"Enviando correo a {destinatario}: {mensaje}")

def enviar_notificacion_sms(destinatario, mensaje):
    print(f"Enviando SMS a {destinatario}: {mensaje}")
