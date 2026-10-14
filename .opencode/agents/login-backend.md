---
description: Implementa seguridad, autenticación, sesiones y servidor HTTP del login.
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

Lee el contrato y el resumen de BD. Trabaja en `proyecto-demo/auth/seguridad.py`, `servicio_auth.py`
y `servidor.py`. Usa PBKDF2-HMAC-SHA256, salt, `compare_digest`, tokens aleatorios y cookies
`HttpOnly; SameSite=Lax`. Implementa login, logout y página protegida, sin registro ni recuperación.
Ejecuta una prueba de humo y reporta cambios, API y resultados.
