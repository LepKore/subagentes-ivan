"""Punto de entrada de la aplicación de login.

Uso:
    python -m auth [--host 127.0.0.1] [--puerto 8000] [--db login.db]
"""
import argparse
import sys

from .db_auth import buscar_usuario, crear_base, crear_usuario
from .servidor import crear_servidor

USUARIO_DEMO = "demo"
PASSWORD_DEMO = "demo1234"


def parse_args(argv=None):
    analizador = argparse.ArgumentParser(description="Arranca el servidor de login.")
    analizador.add_argument("--host", default="127.0.0.1", help="Dirección de escucha")
    analizador.add_argument("--puerto", type=int, default=8000, help="Puerto de escucha")
    analizador.add_argument("--db", default="login.db", help="Ruta de la base de datos SQLite")
    return analizador.parse_args(argv)


def preparar(conexion, usuario=USUARIO_DEMO, password=PASSWORD_DEMO):
    """Registra el usuario de demostración solo si no existe. Devuelve True si lo creó."""
    if buscar_usuario(conexion, usuario):
        return False
    crear_usuario(conexion, usuario, password)
    return True


def main(argv=None):
    args = parse_args(argv)
    conexion = crear_base(args.db)
    creado = preparar(conexion)
    servidor = crear_servidor(conexion, args.host, args.puerto)
    url = f"http://{args.host}:{args.puerto}"
    print(f"Servidor de login escuchando en {url}")
    print(f"Abre {url}/login en el navegador.")
    if creado:
        print(f"Usuario de prueba creado: {USUARIO_DEMO} / {PASSWORD_DEMO}")
    else:
        print(f"Usuario de prueba existente: {USUARIO_DEMO}")
    print("Pulsa Ctrl+C para detener.")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        servidor.server_close()
        conexion.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())