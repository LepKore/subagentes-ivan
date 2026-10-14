#!/usr/bin/env python3
"""Bloquea el push si la suite de pruebas del proyecto falla."""

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    print("[pre-push] Ejecutando pruebas...")
    resultado = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "proyecto-demo", "-v"],
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
    )
    if resultado.returncode != 0:
        print(
            "[pre-push] PUSH BLOQUEADO: las pruebas fallaron. "
            "Corrige los errores y vuelve a intentarlo.",
            file=sys.stderr,
        )
        return resultado.returncode
    print("[pre-push] Todas las pruebas pasaron. Push permitido.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
