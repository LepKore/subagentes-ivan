from .db_auth import buscar_usuario, guardar_sesion, buscar_sesion, borrar_sesion
from .seguridad import verificar_password, token_sesion


def iniciar_sesion(conexion, username, password):
    if not isinstance(username, str) or not isinstance(password, str):
        return None
    usuario = buscar_usuario(conexion, username)
    if not usuario or not verificar_password(password, usuario["salt"], usuario["password_hash"]):
        return None
    token = token_sesion()
    guardar_sesion(conexion, token, usuario["id"])
    return token


def sesion_actual(conexion, token):
    if not token:
        return None
    fila = buscar_sesion(conexion, token)
    return dict(fila) if fila else None


def cerrar_sesion(conexion, token):
    if token:
        borrar_sesion(conexion, token)
