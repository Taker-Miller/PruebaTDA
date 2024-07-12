import mysql.connector
from mysql.connector import Error

def crear_conexion():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='',
        database='ticket'
    )

def validar_usuario(nombre_usuario, contraseña):
    query = "SELECT * FROM usuarios WHERE Nombre = %s AND Contraseña = %s"
    conn = crear_conexion()
    cursor = conn.cursor()
    cursor.execute(query, (nombre_usuario, contraseña))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    if usuario:
        return True, usuario[3] 
    return False, None

def crear_usuario(nombre, correo, contraseña, tipo):
    query = "INSERT INTO usuarios (Nombre, Correo, Contraseña, Tipo) VALUES (%s, %s, %s, %s)"
    conn = crear_conexion()
    cursor = conn.cursor()
    try:
        cursor.execute(query, (nombre, correo, contraseña, tipo))
        conn.commit()
        return True
    except Error as e:
        print(f"Error: {e}")
        return False
    finally:
        cursor.close()
        conn.close()
