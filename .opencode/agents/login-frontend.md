---
description: Crea la interfaz HTML mínima, accesible y segura del login.
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

Lee el contrato y resúmenes anteriores. Trabaja en `proyecto-demo/auth/templates.py`.
Crea labels, autocomplete, password, foco inicial y `role=alert`. Escapa valores con `html.escape`.
No uses dependencias, JS ni recursos externos. Verifica entradas maliciosas y reporta pruebas.
