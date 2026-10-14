from html import escape


# Plantilla mínima de acceso para la demo web.
def pagina_login(error=""):
    mensaje = f'<p role="alert">{escape(error)}</p>' if error else ""
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Iniciar sesión</title></head>
<body><main><h1>Iniciar sesión</h1>{mensaje}<form method="post" action="/login">
<label for="username">Usuario</label><input id="username" name="username" autocomplete="username" required autofocus>
<label for="password">Contraseña</label><input id="password" name="password" type="password" autocomplete="current-password" required>
<label><input type="checkbox" name="recordar"> Recuérdame</label>
<button type="submit">Entrar</button></form></main></body></html>'''


def pagina_inicio(usuario):
    return f'<!doctype html><html lang="es"><body><main><h1>Hola, {escape(usuario)}</h1><form method="post" action="/logout"><button type="submit">Cerrar sesión</button></form></main></body></html>'
