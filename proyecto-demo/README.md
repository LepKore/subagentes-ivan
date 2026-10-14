# Proyecto demo: gestión de notas

Demo educativa de un flujo de calidad con subagentes: pruebas, revisión y corrección. El módulo implementa operaciones básicas para gestionar notas de estudiantes de Programación I.

## Estructura

- `notas.py`: funciones de cálculo, validación, reportes y búsqueda en una base SQLite en memoria.
- `test_notas.py`: suite de 59 pruebas unitarias con `unittest`.

## Requisitos

- Python 3.x
- Solo se utiliza la biblioteca estándar.

## Uso

Desde la raíz del repositorio:

```bash
python proyecto-demo/notas.py
```

También puede ejecutarse desde `proyecto-demo`:

```bash
python notas.py
```

El programa muestra la búsqueda de Ana, el cálculo de una nota final y el estado de la nota 51.

## Pruebas

Desde la raíz del repositorio:

```bash
python -m unittest discover -s proyecto-demo -v
```

Desde `proyecto-demo`:

```bash
python -m unittest discover -s .
```

Estado actual: 59 pruebas pasan correctamente.

## API pública

| Función | Descripción | Retorno |
|---|---|---|
| `calcular_promedio(notas)` | Calcula el promedio; una lista vacía produce `0.0`. | `float` |
| `nota_final(parcial1, parcial2, examen_final, practicas)` | Aplica la ponderación oficial. | `float` |
| `es_aprobado(nota)` | Comprueba si la nota alcanza el umbral. | `bool` |
| `estado(nota)` | Devuelve el estado académico. | `str` |
| `validar_nota(nota)` | Comprueba que la nota sea numérica y esté dentro del rango. | `bool` |
| `crear_base_demo()` | Crea y carga una base SQLite en memoria. | `sqlite3.Connection` |
| `buscar_estudiante(conexion, nombre)` | Busca estudiantes por nombre exacto. | `list` de tuplas |
| `mejores_estudiantes(estudiantes, cantidad=3)` | Ordena estudiantes por nota descendente y limita la cantidad. | `list` |
| `reporte_aprobados(estudiantes)` | Obtiene nombres de estudiantes aprobados. | `list` de nombres |
| `reporte_reprobados(estudiantes)` | Obtiene nombres de estudiantes reprobados. | `list` de nombres |

## Reglas de negocio

- Las notas están en la escala de 0 a 100.
- Se aprueba con 51 o más (`>= 51`).
- La nota final usa parciales al 20% cada uno, examen final al 40% y prácticas al 20%. Los pesos suman 1.0.

## Configuración

`ADMIN_PASSWORD` se lee desde una variable de entorno mediante `os.environ.get`. Si no está definida, su valor es una cadena vacía.

## Notas de seguridad

- Las consultas SQL usan parámetros, por lo que el nombre buscado se trata como dato y no como código SQL.
- No hay credenciales hardcodeadas en el código fuente.

## Login

El paquete `auth/` contiene un login y logout web mínimo basado únicamente en la biblioteca
estándar. Usa SQLite, PBKDF2-HMAC-SHA256 con salt por usuario y sesiones mediante cookies
`HttpOnly` y `SameSite=Lax`.

Para crear un usuario inicial sin guardar secretos en el código:

```powershell
$env:ADMIN_USERNAME = "admin"
$env:ADMIN_PASSWORD = "cambia-esta-contrasena"
```

Las pruebas del login están en `tests/test_login.py` y se ejecutan con la suite general.

### Ejecutar el login

Desde `proyecto-demo`:

```bash
python -m auth
```

Opciones: `--host` (por defecto `127.0.0.1`), `--puerto` (por defecto `8000`) y `--db` (por defecto `login.db`).

El servidor imprime la URL y las credenciales del usuario de prueba:

- URL: `http://127.0.0.1:8000/login`
- Usuario: `demo`
- Contraseña: `demo1234`

Ese usuario se crea solo la primera vez; en arranques posteriores se reutiliza. Ctrl+C detiene el servidor.
