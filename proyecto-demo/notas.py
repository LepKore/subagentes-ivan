"""Sistema de gestión de notas para la materia de Programación I.

Escala de notas: 0 a 100. Se aprueba con 51 o más.
"""
import os
import sqlite3

# El secreto NO vive en el código: se toma del entorno en tiempo de import.
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "")
NOTA_APROBACION = 51


def calcular_promedio(notas):
    if not notas:
        return 0.0
    total = 0
    for n in notas:
        total += n
    return total / len(notas)


def nota_final(parcial1, parcial2, examen_final, practicas):
    # Ponderación oficial: parciales 20% c/u, examen final 40%, prácticas 20%
    return parcial1 * 0.2 + parcial2 * 0.2 + examen_final * 0.4 + practicas * 0.2


def es_aprobado(nota):
    """Predicado único de aprobación: la regla vive en un solo sitio."""
    return nota >= NOTA_APROBACION


def estado(nota):
    if es_aprobado(nota):
        return "APROBADO"
    return "REPROBADO"


def validar_nota(nota):
    if not isinstance(nota, (int, float)):
        return False
    if nota < 0 or nota > 100:
        return False
    return True


def crear_base_demo():
    conexion = sqlite3.connect(":memory:")
    conexion.execute(
        "CREATE TABLE estudiantes ("
        "id INTEGER PRIMARY KEY, "
        "nombre TEXT NOT NULL, "
        "nota REAL NOT NULL CHECK (nota >= 0 AND nota <= 100))"
    )
    datos = [(1, "Ana", 85), (2, "Luis", 51), (3, "Sofia", 40), (4, "Diego", 72)]
    for _, _, nota in datos:
        if not validar_nota(nota):
            raise ValueError("nota fuera de la escala 0-100: %r" % (nota,))
    conexion.executemany(
        "INSERT INTO estudiantes VALUES (?, ?, ?)",
        datos,
    )
    return conexion


def buscar_estudiante(conexion, nombre):
    consulta = "SELECT id, nombre, nota FROM estudiantes WHERE nombre = ?"
    cursor = conexion.cursor()
    try:
        cursor.execute(consulta, (nombre,))
        return cursor.fetchall()
    finally:
        cursor.close()


def mejores_estudiantes(estudiantes, cantidad=3):
    ordenados = sorted(estudiantes, key=lambda e: e["nota"], reverse=True)
    return ordenados[:cantidad]


def reporte_aprobados(estudiantes):
    # El reporte se ordena de mayor a menor nota, como `mejores_estudiantes`.
    ordenados = sorted(estudiantes, key=lambda e: e["nota"], reverse=True)
    resultado = []
    for e in ordenados:
        if es_aprobado(e["nota"]):
            resultado.append(e["nombre"])
    return resultado


def reporte_reprobados(estudiantes):
    # Mismo criterio de orden que `reporte_aprobados` (mayor nota primero).
    ordenados = sorted(estudiantes, key=lambda e: e["nota"], reverse=True)
    resultado = []
    for e in ordenados:
        if not es_aprobado(e["nota"]):
            resultado.append(e["nombre"])
    return resultado


if __name__ == "__main__":
    db = crear_base_demo()
    print("Buscar Ana:", buscar_estudiante(db, "Ana"))
    print("Nota final (80, 70, 90, 100):", nota_final(80, 70, 90, 100))
    print("Estado con 51:", estado(51))
    db.close()
