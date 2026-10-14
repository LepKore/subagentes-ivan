import http.client
import os
import shutil
import sqlite3
import sys
import tempfile
import threading
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth import __main__ as main_module
from auth.__main__ import PASSWORD_DEMO, USUARIO_DEMO, main, preparar
from auth.db_auth import buscar_usuario, crear_base, crear_usuario
from auth.seguridad import crear_hash, hash_token
from auth.servidor import crear_servidor
from auth.servicio_auth import cerrar_sesion, iniciar_sesion, sesion_actual
from auth.templates import pagina_login


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.db = crear_base()
        crear_usuario(self.db, "ana", "secreto")

    def tearDown(self):
        self.db.close()

    def test_contrato_db_y_salt_distinto(self):
        usuario = buscar_usuario(self.db, "ana")
        self.assertIsNotNone(usuario)
        self.assertNotIn(b"secreto", usuario["password_hash"])
        salt1, digest1 = crear_hash("secreto")
        salt2, digest2 = crear_hash("secreto")
        self.assertNotEqual(salt1, salt2)
        self.assertNotEqual(digest1, digest2)

    def test_contrasena_no_se_almacena_en_claro(self):
        fila = self.db.execute("SELECT password_hash, salt FROM usuarios WHERE username = 'ana'").fetchone()
        self.assertNotIn(b"secreto", fila[0])
        self.assertNotEqual(fila[0], b"secreto")
        self.assertEqual(len(fila[1]), 16)

    def test_login_valido_invalido_y_usuario_inexistente(self):
        token = iniciar_sesion(self.db, "ana", "secreto")
        self.assertIsNotNone(token)
        self.assertIsNone(iniciar_sesion(self.db, "ana", "incorrecta"))
        self.assertIsNone(iniciar_sesion(self.db, "nadie", "secreto"))

    def test_sesion_token_solo_se_guarda_como_hash_y_logout(self):
        token = iniciar_sesion(self.db, "ana", "secreto")
        fila = self.db.execute("SELECT token_hash FROM sesiones").fetchone()
        self.assertEqual(fila[0], hash_token(token))
        self.assertNotEqual(fila[0], token)
        self.assertEqual(sesion_actual(self.db, token)["username"], "ana")
        cerrar_sesion(self.db, token)
        self.assertIsNone(sesion_actual(self.db, token))

    def test_html_escapado_y_formulario_accesible(self):
        html = pagina_login('<script>alert("x")</script>')
        self.assertNotIn('<script>alert("x")</script>', html)
        self.assertIn("&lt;script&gt;", html)
        self.assertIn('role="alert"', html)
        self.assertIn('autocomplete="username"', html)
        self.assertIn('autocomplete="current-password"', html)


class TestLoginHTTP(unittest.TestCase):
    def setUp(self):
        # El servidor atiende en otro hilo; la conexión de prueba permite ese uso.
        self.db = crear_base()
        self.db.close()
        self.db = sqlite3.connect(":memory:", check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        # Reutilizar el esquema oficial evita cualquier fixture paralelo a producción.
        self.db.execute("CREATE TABLE usuarios (id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, password_hash BLOB NOT NULL, salt BLOB NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)")
        self.db.execute("CREATE TABLE sesiones (token_hash TEXT PRIMARY KEY, user_id INTEGER NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)")
        crear_usuario(self.db, "ana", "secreto")
        self.server = crear_servidor(self.db, puerto=0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.host, self.port = self.server.server_address

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.db.close()

    def request(self, method, path, body=None, cookie=None):
        conn = http.client.HTTPConnection(self.host, self.port)
        headers = {"Content-Type": "application/x-www-form-urlencoded"} if body else {}
        if cookie:
            headers["Cookie"] = cookie
        conn.request(method, path, body=body, headers=headers)
        response = conn.getresponse()
        data = response.read().decode("utf-8")
        result = response.status, dict(response.getheaders()), data
        conn.close()
        return result

    def test_get_login_es_html_accesible(self):
        status, headers, body = self.request("GET", "/login")
        self.assertEqual(status, 200)
        self.assertIn("text/html", headers["Content-Type"])
        self.assertIn('<label for="username">Usuario</label>', body)
        self.assertIn('<label for="password">Contraseña</label>', body)
        self.assertNotIn('<script>', body)

    def test_login_http_valido_cookie_segura_y_acceso_protegido(self):
        status, headers, _ = self.request("POST", "/login", "username=ana&password=secreto")
        self.assertEqual(status, 303)
        self.assertEqual(headers["Location"], "/")
        cookie = headers["Set-Cookie"]
        self.assertRegex(cookie, r"^session=[^;]+")
        self.assertIn("HttpOnly", cookie)
        self.assertIn("SameSite=Lax", cookie)
        self.assertIn("Path=/", cookie)
        status, _, body = self.request("GET", "/", cookie=cookie.split(";", 1)[0])
        self.assertEqual(status, 200)
        self.assertIn("ana", body)

    def test_login_http_invalido_mensaje_generico(self):
        status, _, body = self.request("POST", "/login", "username=ana&password=nope")
        self.assertEqual(status, 200)
        self.assertIn("Usuario o contraseña incorrectos", body)
        self.assertNotIn("nope", body)

    def test_ruta_protegida_redirige_y_logout_invalida(self):
        status, headers, _ = self.request("GET", "/")
        self.assertEqual(status, 303)
        self.assertEqual(headers["Location"], "/login")
        _, login_headers, _ = self.request("POST", "/login", "username=ana&password=secreto")
        cookie = login_headers["Set-Cookie"].split(";", 1)[0]
        status, headers, _ = self.request("POST", "/logout", cookie=cookie)
        self.assertEqual(status, 303)
        self.assertEqual(headers["Location"], "/login")
        self.assertIn("Max-Age=0", headers["Set-Cookie"])
        status, headers, _ = self.request("GET", "/", cookie=cookie)
        self.assertEqual(status, 303)
        self.assertEqual(headers["Location"], "/login")


class TestArranque(unittest.TestCase):
    """Prueba de humo del punto de entrada `python -m auth`."""

    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tempdir, True)
        self.db = crear_base(os.path.join(self.tempdir, "login.db"))
        self.addCleanup(self.db.close)

    def test_preparar_crea_el_usario_una_sola_vez(self):
        self.assertTrue(preparar(self.db))
        self.assertFalse(preparar(self.db))
        filas = self.db.execute("SELECT COUNT(*) FROM usuarios").fetchone()[0]
        self.assertEqual(filas, 1)
        usuario = buscar_usuario(self.db, USUARIO_DEMO)
        self.assertIsNotNone(usuario)
        self.assertIsNone(sesion_actual(self.db, None))

    def test_main_prepara_la_base_y_arranca_el_servidor(self):
        """main() debe levantar el servidor; aquí se corta en el primer tick."""
        rutas = []

        class ServidorFalso:
            server_address = ("127.0.0.1", 8000)

            def serve_forever(self):
                raise KeyboardInterrupt

            def server_close(self):
                pass

        def crear_falso(conexion, host, puerto):
            rutas.append((host, puerto))
            return ServidorFalso()

        ruta_db = os.path.join(self.tempdir, "otro.db")
        with mock.patch.object(main_module, "crear_servidor", side_effect=crear_falso):
            self.assertEqual(main(["--db", ruta_db]), 0)
        self.assertEqual(rutas, [("127.0.0.1", 8000)])
        self.assertTrue(os.path.exists(ruta_db))
        self.assertIsNotNone(buscar_usuario(crear_base(ruta_db), USUARIO_DEMO))


if __name__ == "__main__":
    unittest.main()
