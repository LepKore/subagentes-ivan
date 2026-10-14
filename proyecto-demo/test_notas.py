"""Pruebas unitarias para `proyecto-demo/notas.py`.

Fuente de verdad (NO el código actual):
  - Docstring del módulo: "Escala de notas: 0 a 100. Se aprueba con 51 o más."
  - Constante `NOTA_APROBACION = 51`.
  - Comentario de `nota_final`:
      "Ponderación oficial: parciales 20% c/u, examen final 40%, prácticas 20%"
    => los pesos suman 1.0 (0.2 + 0.2 + 0.4 + 0.2), no 1.1.
  - Nombres y firmas: `mejores_estudiantes` => "mejores" implica orden
    descendente por nota; `reporte_aprobados` / `reporte_reprobados` deben
    formar una partición completa de la lista de entrada.

Si el código contradice la documentación, la prueba FALLA a propósito.
Este archivo NO modifica `notas.py`.
"""
import os
import sys
import unittest

# Permite ejecutar tanto `python -m unittest discover -s proyecto-demo`
# (desde la raíz del repo) como `python -m unittest test_notas`
# (desde dentro de proyecto-demo).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import notas  # noqa: E402


# Datos de referencia: los mismos 4 estudiantes que crea `crear_base_demo`.
DATOS_DEMO = [
    {"id": 1, "nombre": "Ana", "nota": 85.0},
    {"id": 2, "nombre": "Luis", "nota": 51.0},
    {"id": 3, "nombre": "Sofia", "nota": 40.0},
    {"id": 4, "nombre": "Diego", "nota": 72.0},
]


class TestCalcularPromedio(unittest.TestCase):
    """`calcular_promedio(notas)` -> media aritmética de la lista de notas."""

    def test_caso_normal(self):
        """Caso normal: media de [80, 70, 90] es 80.0."""
        self.assertEqual(notas.calcular_promedio([80, 70, 90]), 80.0)

    def test_caso_normal_desordenado(self):
        """El resultado no debe depender del orden de entrada."""
        self.assertEqual(notas.calcular_promedio([90, 80, 70]), 80.0)

    def test_lista_vacia_devuelve_cero(self):
        """BORDE: lista vacía. La media de "nada" es 0, no una excepción.

        Una función que revienta con ZeroDivisionError aborta cualquier
        reporte promedio; el contrato implícito de una media aritmética
        sobre el conjunto vacío es el elemento neutro de la suma.
        """
        self.assertEqual(notas.calcular_promedio([]), 0.0)

    def test_un_solo_elemento(self):
        """BORDE: un único elemento; la media es ese mismo elemento."""
        self.assertEqual(notas.calcular_promedio([75]), 75.0)

    def test_todos_los_mismos(self):
        """BORDE: lista constante."""
        self.assertEqual(notas.calcular_promedio([50, 50, 50, 50]), 50.0)

    def test_escala_0_a_100(self):
        """BORDE: extremos de la escala documentada (0 a 100)."""
        self.assertEqual(notas.calcular_promedio([0, 100]), 50.0)

    def test_no_altera_la_lista_original(self):
        """La función no debe mutar su argumento."""
        original = [80, 70, 90]
        copia = list(original)
        notas.calcular_promedio(original)
        self.assertEqual(original, copia)


class TestNotaFinal(unittest.TestCase):
    """`nota_final` debe aplicar 20% / 20% / 40% / 20% (suma = 1.0)."""

    def test_ejemplo_documentado_del_guion(self):
        """Ejemplo del guion de clase: (80, 70, 90, 100) debe dar 86.0.

        80*0.2 = 16.0 | 70*0.2 = 14.0 | 90*0.4 = 36.0 | 100*0.2 = 20.0
        Total = 86.0
        """
        self.assertAlmostEqual(
            notas.nota_final(80, 70, 90, 100), 86.0, places=7,
            msg="nota_final(80,70,90,100) debe ser 86.0 con pesos 20/20/40/20",
        )

    def test_todas_las_notas_iguales_conserva_la_nota(self):
        """BORDE: con los cuatro insumos en X, la nota final debe ser X.

        Es la propiedad de coherencia de una ponderación que suma 1.0.
        """
        for x in (0, 20, 50, 70, 100):
            with self.subTest(nota=x):
                self.assertAlmostEqual(
                    notas.nota_final(x, x, x, x), float(x), places=7,
                    msg=f"nota_final({x},{x},{x},{x}) debe devolver {x}.0",
                )

    def test_todos_100_da_100(self):
        """BORDE superior: 100 en todo no puede superar el tope de la escala."""
        self.assertAlmostEqual(
            notas.nota_final(100, 100, 100, 100), 100.0, places=7,
            msg="nota_final(100,100,100,100) debe ser 100.0 (escala 0-100)",
        )

    def test_todos_cero_da_cero(self):
        """BORDE inferior: 0 en todo debe dar 0.0."""
        self.assertEqual(notas.nota_final(0, 0, 0, 0), 0.0)

    def test_pesos_suman_uno(self):
        """BORDE: si el peso total fuera > 1.0, cualquier nota se inflaría.

        70 en los cuatro insumos debe devolver 70.0, no un valor mayor.
        """
        self.assertAlmostEqual(
            notas.nota_final(70, 70, 70, 70), 70.0, places=7,
            msg="nota_final(70,70,70,70) debe ser 70.0; un resultado mayor "
                "indica que los pesos suman mas de 1.0",
        )

    def test_no_supera_100_con_notas_maximas(self):
        """La nota final no puede exceder el máximo de la escala (100)."""
        resultado = notas.nota_final(100, 100, 100, 100)
        self.assertLessEqual(
            resultado, 100.0,
            msg=f"la nota final no puede superar 100, se obtuvo {resultado}",
        )

    def test_practicas_valen_el_20_por_ciento(self):
        """Aísla el peso de prácticas: 100 solo en prácticas debe dar 20.0."""
        self.assertAlmostEqual(
            notas.nota_final(0, 0, 0, 100), 20.0, places=7,
            msg="las practicas valen el 20%: nota_final(0,0,0,100) = 20.0",
        )

    def test_examen_final_vale_el_40_por_ciento(self):
        """Aísla el examen final: 100 solo en examen debe dar 40.0."""
        self.assertAlmostEqual(
            notas.nota_final(0, 0, 100, 0), 40.0, places=7,
            msg="el examen final vale el 40%: nota_final(0,0,100,0) = 40.0",
        )


class TestEstado(unittest.TestCase):
    """`estado(nota)` -> "APROBADO" si nota >= 51, si no "REPROBADO"."""

    def test_limite_inferior_51_aprueba(self):
        """BORDE CRÍTICO: la documentación dice "se aprueba con 51 o más"."""
        self.assertEqual(
            notas.estado(51), "APROBADO",
            msg="51 es nota de aprobacion: debe devolver 'APROBADO'",
        )

    def test_justo_por_debajo_50_reprueba(self):
        """BORDE: 50 está por debajo del umbral."""
        self.assertEqual(notas.estado(50), "REPROBADO")

    def test_51_por_flipar_antes_de_52(self):
        """BORDE: el corte es inclusivo (>=), no exclusivo (>)."""
        self.assertEqual(notas.estado(51), notas.estado(52))

    def test_cota_maxima_100_aprueba(self):
        """BORDE: 100 en la escala debe aprobar."""
        self.assertEqual(notas.estado(100), "APROBADO")

    def test_cota_minima_0_reprueba(self):
        """BORDE: 0 en la escala debe reprobar."""
        self.assertEqual(notas.estado(0), "REPROBADO")

    def test_rango_interno(self):
        """Caso normal en medio de la escala."""
        self.assertEqual(notas.estado(75), "APROBADO")
        self.assertEqual(notas.estado(25), "REPROBADO")

    def test_todas_las_notas_validas(self):
        """Coherencia: todo valor 0..100 devuelve APROBADO iff nota >= 51."""
        for nota in range(0, 101):
            with self.subTest(nota=nota):
                esperado = "APROBADO" if nota >= notas.NOTA_APROBACION else "REPROBADO"
                self.assertEqual(notas.estado(nota), esperado)


class TestValidarNota(unittest.TestCase):
    """`validar_nota(nota)` -> False si la nota está fuera del rango 0..100."""

    def test_negativa_rechazada(self):
        """BORDE: una nota negativa no es válida."""
        self.assertFalse(notas.validar_nota(-1))

    def test_cero_es_valido(self):
        """BORDE: 0 está dentro de la escala 0..100."""
        self.assertTrue(notas.validar_nota(0))

    def test_100_es_valido(self):
        """BORDE: 100 es el máximo de la escala y es válido."""
        self.assertTrue(notas.validar_nota(100))

    def test_101_rechazada(self):
        """FUERA DE RANGO: 101 excede el máximo documentado (0 a 100)."""
        self.assertFalse(
            notas.validar_nota(101),
            msg="101 esta fuera de la escala 0-100 y debe ser invalida",
        )

    def test_150_rechazada(self):
        """FUERA DE RANGO: nota claramente imposible."""
        self.assertFalse(
            notas.validar_nota(150),
            msg="150 esta fuera de la escala 0-100 y debe ser invalida",
        )

    def test_negativa_absorbe_rechazada(self):
        """FUERA DE RANGO por debajo."""
        self.assertFalse(notas.validar_nota(-0.01))

    def test_todo_rango_valido_aceptado(self):
        """Coherencia: todo entero 0..100 debe aceptarse."""
        for nota in range(0, 101):
            with self.subTest(nota=nota):
                self.assertTrue(notas.validar_nota(nota))

    def test_todo_fuera_de_rango_rechazado(self):
        """Coherencia: nada fuera de 0..100 debe aceptarse."""
        for nota in (-50, -1, 101, 150, 1000):
            with self.subTest(nota=nota):
                self.assertFalse(notas.validar_nota(nota))

    def test_entrada_no_numerica_no_se_acepta_en_silencio(self):
        """ENTRADA MALICIOSA: un texto no debe pasar por "válido".

        Aceptar la cadena "ochenta" como nota válida es una falsa garantía
        de validación. Se acepta indistintamente que la función rechace
        (devuelva False) o que levante TypeError/ValueError.
        """
        try:
            resultado = notas.validar_nota("ochenta")
        except (TypeError, ValueError):
            return  # lanzar excepción también es un rechazo válido
        self.assertFalse(
            resultado,
            msg="validar_nota('ochenta') no debe devolver True: la entrada no "
                "es una nota numérica dentro de la escala 0-100",
        )


class TestBaseDemoYBusqueda(unittest.TestCase):
    """`crear_base_demo` / `buscar_estudiante` sobre SQLite."""

    def setUp(self):
        self.conexion = notas.crear_base_demo()

    def tearDown(self):
        self.conexion.close()

    def test_base_demo_tiene_cuatro_estudiantes(self):
        """Caso normal: la tabla se crea con las 4 filas de la demo."""
        total = self.conexion.execute(
            "SELECT COUNT(*) FROM estudiantes"
        ).fetchone()[0]
        self.assertEqual(total, 4)

    def test_base_demo_datos_correctos(self):
        """Caso normal: (id, nombre, nota) de cada fila."""
        filas = self.conexion.execute(
            "SELECT id, nombre, nota FROM estudiantes ORDER BY id"
        ).fetchall()
        self.assertEqual(
            filas,
            [(1, "Ana", 85), (2, "Luis", 51), (3, "Sofia", 40), (4, "Diego", 72)],
        )

    def test_base_demo_es_una_base_usable(self):
        """La conexión devuelta debe permitir consultas."""
        self.assertIsInstance(self.conexion.execute("SELECT 1").fetchone(), tuple)

    def test_buscar_existente(self):
        """Caso normal: búsqueda exacta por nombre."""
        self.assertEqual(
            notas.buscar_estudiante(self.conexion, "Ana"), [(1, "Ana", 85)]
        )

    def test_buscar_inexistente_devuelve_lista_vacia(self):
        """BORDE: nombre que no existe."""
        self.assertEqual(notas.buscar_estudiante(self.conexion, "Zoe"), [])

    def test_buscar_nombre_con_espacios(self):
        """BORDE: cadena vacía y espacios (no deben ser nombres válidos)."""
        self.assertEqual(notas.buscar_estudiante(self.conexion, ""), [])
        self.assertEqual(notas.buscar_estudiante(self.conexion, "   "), [])

    def test_buscar_es_sensible_a_mayusculas(self):
        """BORDE: la búsqueda es exacta; 'ana' no es 'Ana'."""
        self.assertEqual(notas.buscar_estudiante(self.conexion, "ana"), [])

    def test_inyeccion_sql_or_siempre_verdadero(self):
        """ENTRADA MALICIOSA: tautología SQL inyectada.

        El nombre "Ana' OR '1'='1" no debe devolver la tabla entera.
        """
        malicioso = "Ana' OR '1'='1"
        resultado = notas.buscar_estudiante(self.conexion, malicioso)
        self.assertEqual(
            resultado, [],
            msg="INYECCION SQL: buscar_estudiante debe tratar el nombre como "
                "dato literal, no como SQL. Con %r se obtuvo %r (se devolvieron "
                "todos los estudiantes de la tabla)" % (malicioso, resultado),
        )

    def test_inyeccion_sql_comentario_linea(self):
        """ENTRADA MALICIOSA: comentario SQL para truncar la condición."""
        malicioso = "Ana'--"
        resultado = notas.buscar_estudiante(self.conexion, malicioso)
        self.assertEqual(
            resultado, [],
            msg="INYECCION SQL: con %r se obtuvo %r; el guion doble comenta el "
                "resto de la consulta y filtra fuera de la condición"
                % (malicioso, resultado),
        )

    def test_inyeccion_sql_no_rompe_la_base(self):
        """ENTRADA MALICIOSA: intentar ejecutar sentencias encadenadas.

        El nombre "Ana'; DROP TABLE estudiantes; --" debe Ser rechazado sin
        efectos secundarios: se espera lista vacía y base intacta.
        """
        malicioso = "Ana'; DROP TABLE estudiantes; --"
        try:
            resultado = notas.buscar_estudiante(self.conexion, malicioso)
        except Exception as exc:  # noqa: BLE001 - cualquier excepción es un fallo
            self.fail(
                "INYECCION SQL: buscar_estudiante(%r) lanzó %s: %s. Con una "
                "consulta parametrizada debe devolver [] sin error."
                % (malicioso, type(exc).__name__, exc)
            )
        self.assertEqual(
            resultado, [],
            msg="INYECCION SQL: %r debe devolver lista vacía, se obtuvo %r"
                % (malicioso, resultado),
        )
        restantes = self.conexion.execute(
            "SELECT COUNT(*) FROM estudiantes"
        ).fetchone()[0]
        self.assertEqual(
            restantes, 4,
            msg="INYECCION SQL: la tabla estudiantes debe seguir intacta "
                "(4 filas), quedan %d" % restantes,
        )

    def test_inyeccion_union_select(self):
        """ENTRADA MALICIOSA: inyección UNION para filtrar columnas ajenas."""
        malicioso = "' UNION SELECT 1, 'hacker', 0 --"
        resultado = notas.buscar_estudiante(self.conexion, malicioso)
        self.assertEqual(
            resultado, [],
            msg="INYECCION SQL (UNION): %r debe devolver [], se obtuvo %r"
                % (malicioso, resultado),
        )


class TestMejoresEstudiantes(unittest.TestCase):
    """`mejores_estudiantes` => orden descendente por nota, los mejores primero."""

    def test_orden_descendente(self):
        """Caso normal: la lista debe venir de mayor a menor nota."""
        resultado = notas.mejores_estudiantes(DATOS_DEMO)
        notas_orden = [e["nota"] for e in resultado]
        self.assertEqual(
            notas_orden, sorted(notas_orden, reverse=True),
            msg="mejores_estudiantes debe devolver las notas en orden "
                "descendente, se obtuvo %r" % (notas_orden,),
        )

    def test_cantidad_por_defecto_trae_los_tres_mejores(self):
        """BORDE: `cantidad=3` por defecto -> Ana (85), Diego (72), Luis (51)."""
        resultado = notas.mejores_estudiantes(DATOS_DEMO)
        self.assertEqual([e["nombre"] for e in resultado], ["Ana", "Diego", "Luis"])

    def test_cantidad_explicita_1(self):
        """BORDE: pedir solo 1 debe devolver el de mayor nota."""
        resultado = notas.mejores_estudiantes(DATOS_DEMO, cantidad=1)
        self.assertEqual([e["nombre"] for e in resultado], ["Ana"])

    def test_cantidad_explicita_2(self):
        """BORDE: pedir 2 devuelve Ana (85) y Diego (72)."""
        resultado = notas.mejores_estudiantes(DATOS_DEMO, cantidad=2)
        self.assertEqual([e["nombre"] for e in resultado], ["Ana", "Diego"])

    def test_cantidad_mayor_que_la_lista(self):
        """BORDE: pedir más de los que hay no debe inventar filas."""
        resultado = notas.mejores_estudiantes(DATOS_DEMO, cantidad=99)
        self.assertEqual(len(resultado), len(DATOS_DEMO))

    def test_lista_vacia(self):
        """BORDE: lista vacía."""
        self.assertEqual(notas.mejores_estudiantes([]), [])

    def test_no_altera_la_lista_original(self):
        """La función no debe mutar ni reordenar el argumento."""
        original = list(DATOS_DEMO)
        notas.mejores_estudiantes(original)
        self.assertEqual([e["nombre"] for e in original],
                         ["Ana", "Luis", "Sofia", "Diego"])


class TestReportes(unittest.TestCase):
    """`reporte_aprobados` y `reporte_reprobados` deben ser complementarios."""

    def test_aprobados_caso_normal(self):
        """Caso normal: sin casos límite, solo 85 y 72 superan 51."""
        datos = [{"nombre": "Ana", "nota": 85.0}, {"nombre": "Diego", "nota": 72.0}]
        self.assertEqual(notas.reporte_aprobados(datos), ["Ana", "Diego"])

    def test_aprobados_lista_vacia(self):
        """BORDE: lista vacía."""
        self.assertEqual(notas.reporte_aprobados([]), [])

    def test_aprobados_incluye_el_limite_51(self):
        """BORDE CRÍTICO: Luis tiene 51 y debe estar entre los aprobados."""
        self.assertIn(
            "Luis", notas.reporte_aprobados(DATOS_DEMO),
            msg="un estudiante con 51 debe aparecer en reporte_aprobados "
                "(regla: se aprueba con 51 o más)",
        )

    def test_aprobados_excluye_50_y_menos(self):
        """BORDE: 50 y 40 no aprueban."""
        self.assertEqual(notas.reporte_aprobados(DATOS_DEMO), ["Ana", "Diego", "Luis"])

    def test_reprobados_caso_normal(self):
        """Caso normal: sin casos límite, solo 40 reprueba."""
        datos = [{"nombre": "Ana", "nota": 85.0}, {"nombre": "Sofia", "nota": 40.0}]
        self.assertEqual(notas.reporte_reprobados(datos), ["Sofia"])

    def test_reprobados_lista_vacia(self):
        """BORDE: lista vacía."""
        self.assertEqual(notas.reporte_reprobados([]), [])

    def test_reprobados_excluye_el_limite_51(self):
        """BORDE CRÍTICO: Luis con 51 NO debe salir como reprobado."""
        self.assertNotIn(
            "Luis", notas.reporte_reprobados(DATOS_DEMO),
            msg="un estudiante con 51 no debe aparecer en reporte_reprobados",
        )

    def test_particion_completa_sin_solapes_ni_huecos(self):
        """Coherencia: aprobados + reprobados = todos, y no se solapan.

        Este es el invariante clave del par de reportes: sobre los datos de
        la demo (85, 51, 40, 72) cada estudiante debe aparecer exactamente
        una vez en la unión y nunca en ambos.
        """
        aprobados = notas.reporte_aprobados(DATOS_DEMO)
        reprobados = notas.reporte_reprobados(DATOS_DEMO)
        todos = [e["nombre"] for e in DATOS_DEMO]

        self.assertEqual(
            sorted(aprobados), sorted(set(aprobados)),
            msg="reporte_aprobados no debe repetir nombres: %r" % (aprobados,),
        )
        self.assertEqual(
            sorted(reprobados), sorted(set(reprobados)),
            msg="reporte_reprobados no debe repetir nombres: %r" % (reprobados,),
        )
        self.assertEqual(
            sorted(aprobados + reprobados), sorted(todos),
            msg="PARTICION ROTA: aprobados %r + reprobados %r no cubren "
                "exactamente %r (faltan o sobran elementos)"
                % (aprobados, reprobados, todos),
        )
        self.assertEqual(
            set(aprobados) & set(reprobados), set(),
            msg="PARTICION ROTA: %r aparece a la vez como aprobado y reprobado"
                % sorted(set(aprobados) & set(reprobados)),
        )

    def test_particion_respeta_el_limite_51(self):
        """Coherencia: con notas 50 y 51, el corte debe ser 50=REPROBADO, 51=APROBADO."""
        datos = [{"nombre": "Carla", "nota": 50.0}, {"nombre": "Luis", "nota": 51.0}]
        self.assertEqual(notas.reporte_aprobados(datos), ["Luis"])
        self.assertEqual(notas.reporte_reprobados(datos), ["Carla"])

    def test_reportes_coinciden_con_estado(self):
        """Coherencia: el criterio del reporte debe ser el de `estado()`.

        Ningún estudiante puede estar aprobado por reporte pero reprobado por
        `estado()`, ni al revés.
        """
        for e in DATOS_DEMO:
            with self.subTest(estudiante=e["nombre"]):
                en_aprobados = e["nombre"] in notas.reporte_aprobados(DATOS_DEMO)
                en_reprobados = e["nombre"] in notas.reporte_reprobados(DATOS_DEMO)
                self.assertEqual(
                    en_aprobados, notas.estado(e["nota"]) == "APROBADO",
                    msg="%s (nota %s) aparece aprobado=%s pero estado() dice %s"
                        % (e["nombre"], e["nota"], en_aprobados, notas.estado(e["nota"])),
                )
                self.assertEqual(
                    en_reprobados, notas.estado(e["nota"]) == "REPROBADO",
                    msg="%s (nota %s) aparece reprobado=%s pero estado() dice %s"
                        % (e["nombre"], e["nota"], en_reprobados, notas.estado(e["nota"])),
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
