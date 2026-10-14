# Contrato del login

`auth.db_auth` contiene persistencia SQLite; `auth.seguridad`, hash PBKDF2-HMAC-SHA256;
`auth.servicio_auth`, autenticación y sesiones; `auth.templates`, HTML escapado; `auth.servidor`, HTTP.

API: `crear_base(ruta=":memory:")`, `crear_usuario(conexion, username, password)`,
`buscar_usuario(conexion, username)`, `iniciar_sesion(conexion, username, password)`,
`sesion_actual(conexion, token)` y `cerrar_sesion(conexion, token)`.

HTTP: `GET /login` muestra formulario; `POST /login` redirige a `/` si es válido y muestra error
genérico si no; `GET /` exige sesión; `POST /logout` invalida la sesión y redirige a `/login`.

Seguridad: PBKDF2-HMAC-SHA256 con salt aleatorio, tokens aleatorios almacenados como hash,
consultas parametrizadas y cookies `HttpOnly; SameSite=Lax`.
