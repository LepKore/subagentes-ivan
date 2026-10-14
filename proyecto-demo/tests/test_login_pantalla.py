"""Pruebas de la pantalla de login (HTML generado por `auth.templates`).

Ejecutar: python -m unittest discover -s proyecto-demo -v

Nota: `test_recuerda_usuario_existe` falla a propósito para demostrar
cómo GitHub Actions marca un test rojo en un pull request.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth.templates import pagina_login


class TestPantallaLogin(unittest.TestCase):
    def setUp(self):
        self.html = pagina_login()

    def test_tiene_titulo_y_encabezado(self):
        self.assertIn("<title>Iniciar sesión</title>", self.html)
        self.assertIn("<h1>Iniciar sesión</h1>", self.html)
        self.assertIn('<html lang="es">', self.html)

    def test_formulario_apunta_a_login_con_post(self):
        self.assertIn('<form method="post" action="/login">', self.html)
        self.assertIn('<button type="submit">Entrar</button>', self.html)

    def test_campos_usuario_y_contrasena_con_accesibilidad(self):
        self.assertIn('<label for="username">Usuario</label>', self.html)
        self.assertIn('name="username"', self.html)
        self.assertIn('autocomplete="username"', self.html)
        self.assertIn('<label for="password">Contraseña</label>', self.html)
        self.assertIn('type="password"', self.html)
        self.assertIn('autocomplete="current-password"', self.html)
        self.assertEqual(self.html.count("required"), 2)

    def test_mensaje_de_error_se_muestra_y_se_escapa(self):
        sin_error = pagina_login()
        self.assertNotIn('role="alert"', sin_error)
        con_error = pagina_login('Credenciales incorrectas <b>ana</b>')
        self.assertIn('<p role="alert">', con_error)
        self.assertIn("&lt;b&gt;ana&lt;/b&gt;", con_error)
        self.assertNotIn("<b>ana</b>", con_error)

    def test_recuerda_usuario_existe(self):
        # FALLA A PROPÓSITO: la casilla "Recuérdame" aún no está en la pantalla.
        self.assertIn('name="recordar"', self.html)


if __name__ == "__main__":
    unittest.main()