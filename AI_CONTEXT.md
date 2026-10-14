# Contexto del proyecto

> Última verificación: 2026-10-12

## 1. Propósito del proyecto
Demo educativa de un flujo con subagentes y una aplicación mínima de gestión de notas.

## 2. Stack tecnológico y arquitectura
Frontend: HTML mínimo servido por Python. Backend: Python. Persistencia: SQLite. Tests: unittest.

## 3. Estructura del proyecto (mapeo)
`proyecto-demo/`: aplicación y pruebas. `.agents/skills/`: skills locales. `.opencode/agents/`: agentes OpenCode.
No modificar `proyecto-demo/notas.py` ni `proyecto-demo/test_notas.py` salvo petición explícita.

## 4. Comandos críticos
Desarrollo: `python proyecto-demo/notas.py`.
Testing: `python -m unittest discover -s proyecto-demo -v`.
Lint / typecheck: N/A. Deploy: N/A.

## 5. Reglas y convenciones estrictas
Usar biblioteca estándar, funciones pequeñas, unittest, consultas parametrizadas y no exponer secretos.

## 6. Estado actual y registro de cambios
Completado: demo de notas y flujo de calidad. En progreso: skill y subagentes de login y paquete `auth/`.
