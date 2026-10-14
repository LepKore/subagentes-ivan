---
description: Implementa la persistencia SQLite mínima y segura del login.
mode: subagent
temperature: 0.2
permission:
  edit: allow
  bash:
    "*": ask
    "python *": allow
    "cd *": allow
  webfetch: deny
  task: deny
---

Lee `docs/login-CONTRATO.md`. Trabaja solo en `proyecto-demo/auth/db_auth.py` y `__init__.py` si hace falta.
Implementa `crear_base`, `crear_usuario` y `buscar_usuario`, tabla `usuarios`, consultas parametrizadas
y contraseñas nunca almacenadas en claro. No hardcodees secretos. Ejecuta la suite existente y reporta cambios.
