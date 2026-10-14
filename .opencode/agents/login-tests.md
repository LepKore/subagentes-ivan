---
description: Escribe y ejecuta pruebas unittest para el login completo.
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

Trabaja solo en `proyecto-demo/tests/` y no modifiques producción. Cubre salt distinto, ausencia de
contraseña en claro, login válido e inválido, usuario inexistente, sesión, logout, cookie segura,
HTML escapado y errores visibles. Ejecuta `python -m unittest discover -s proyecto-demo -v` y reporta fallos.
