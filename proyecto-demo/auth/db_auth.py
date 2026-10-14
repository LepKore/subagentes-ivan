import os
import sqlite3
from .seguridad import crear_hash, hash_token


def crear_base(ruta=":memory:"):
    conexion = sqlite3.connect(ruta)
    conexion.row_factory = sqlite3.Row
    conexion.execute(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL,
            salt BLOB NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conexion.execute(
        """
        CREATE TABLE IF NOT EXISTS sesiones (
            token_hash TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES usuarios(id)
        )
        """
    )
    conexion.commit()
    return conexion


def crear_usuario(conexion, username, password):
    salt, digest = crear_hash(password)
    cursor = conexion.execute("INSERT INTO usuarios (username, password_hash, salt) VALUES (?, ?, ?)", (username, digest, salt))
    conexion.commit()
    return cursor.lastrowid


def buscar_usuario(conexion, username):
    fila = conexion.execute("SELECT id, username, password_hash, salt FROM usuarios WHERE username = ?", (username,)).fetchone()
    return dict(fila) if fila else None


def guardar_sesion(conexion, token, user_id):
    conexion.execute("INSERT INTO sesiones (token_hash, user_id) VALUES (?, ?)", (hash_token(token), user_id))
    conexion.commit()


def buscar_sesion(conexion, token):
    return conexion.execute("SELECT u.id, u.username FROM sesiones s JOIN usuarios u ON u.id = s.user_id WHERE s.token_hash = ?", (hash_token(token),)).fetchone()


def borrar_sesion(conexion, token):
    conexion.execute("DELETE FROM sesiones WHERE token_hash = ?", (hash_token(token),))
    conexion.commit()


def seed_desde_entorno(conexion):
    username = os.environ.get("ADMIN_USERNAME")
    password = os.environ.get("ADMIN_PASSWORD")
    if username and password and not buscar_usuario(conexion, username):
        crear_usuario(conexion, username, password)
