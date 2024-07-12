import mysql.connector
from mysql.connector import Error

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

def validar_usuario(nombre_usuario, contraseña):
    query = "SELECT * FROM usuarios WHERE Nombre = %s AND Contraseña = %s"
    result = ejecutar_query(query, (nombre_usuario, contraseña))
    if result:
        usuario = result[0]
        return True, usuario[3]  # Devolviendo el tipo de usuario
    return False, None

def crear_usuario(nombre, correo, contraseña, tipo):
    query = "INSERT INTO usuarios (Nombre, Correo, Contraseña, Tipo) VALUES (%s, %s, %s, %s)"
    return ejecutar_query(query, (nombre, correo, contraseña, tipo))
