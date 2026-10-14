import http.cookies
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlsplit
from .servicio_auth import iniciar_sesion, sesion_actual, cerrar_sesion
from .templates import pagina_login, pagina_inicio


class LoginHandler(BaseHTTPRequestHandler):
    conexion = None

    def _token(self):
        cookies = http.cookies.SimpleCookie(self.headers.get("Cookie", ""))
        morsel = cookies.get("session")
        return morsel.value if morsel else None

    def _responder(self, estado, cuerpo, headers=None):
        datos = cuerpo.encode("utf-8")
        self.send_response(estado)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        for clave, valor in (headers or []):
            self.send_header(clave, valor)
        self.send_header("Content-Length", str(len(datos)))
        self.end_headers()
        self.wfile.write(datos)

    def _formulario(self):
        try:
            longitud = max(0, min(int(self.headers.get("Content-Length", "0")), 64 * 1024))
        except ValueError:
            longitud = 0
        return parse_qs(self.rfile.read(longitud).decode("utf-8", errors="replace"),
                        keep_blank_values=True)

    def do_GET(self):
        ruta = urlsplit(self.path).path
        if ruta == "/login":
            return self._responder(200, pagina_login())
        if ruta == "/":
            usuario = sesion_actual(self.conexion, self._token())
            if not usuario:
                return self._responder(303, "", [("Location", "/login")])
            return self._responder(200, pagina_inicio(usuario["username"]))
        self._responder(404, "No encontrado")

    def do_POST(self):
        valores = self._formulario()
        ruta = urlsplit(self.path).path
        if ruta == "/login":
            token = iniciar_sesion(self.conexion, valores.get("username", [""])[0], valores.get("password", [""])[0])
            if not token:
                return self._responder(200, pagina_login("Usuario o contraseña incorrectos"))
            cookie = f"session={token}; HttpOnly; SameSite=Lax; Path=/"
            return self._responder(303, "", [("Location", "/"), ("Set-Cookie", cookie)])
        if ruta == "/logout":
            cerrar_sesion(self.conexion, self._token())
            return self._responder(303, "", [("Location", "/login"), ("Set-Cookie", "session=; Max-Age=0; HttpOnly; SameSite=Lax; Path=/")])
        self._responder(404, "No encontrado")


def crear_servidor(conexion, host="127.0.0.1", puerto=8000):
    LoginHandler.conexion = conexion
    return HTTPServer((host, puerto), LoginHandler)
