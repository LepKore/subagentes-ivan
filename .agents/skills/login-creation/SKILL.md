---
name: login-creation
description: Coordina la creación de un login mínimo con SQLite mediante cuatro subagentes.
---

Eres el orquestador de OpenCode. Ejecuta los subagentes EN ORDEN y nunca los hagas llamarse entre sí:

1. Lee `docs/login-CONTRATO.md`.
2. Llama a `login-BD` para implementar `auth/db_auth.py`.
3. Pasa su resumen a `login-backend` para implementar seguridad, sesiones y servidor HTTP.
4. Pasa los resúmenes a `login-frontend` para implementar la plantilla accesible y escapada.
5. Pasa todos los resúmenes a `login-tests`, que crea pruebas sin tocar producción.
6. Ejecuta `python -m unittest discover -s proyecto-demo -v`.

Cada subagente modifica directamente su parte y responde con archivos, decisiones, comandos,
resultados y pendientes. No modifiques `notas.py`, `test_notas.py` ni `.claude/`.
Al final muestra etapa | subagente | resultado y verifica suite verde, login/logout E2E,
hash con salt, ausencia de secretos y errores visibles.
