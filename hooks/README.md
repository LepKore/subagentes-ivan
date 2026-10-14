# Hook de pre-push

El hook ejecuta toda la suite con `unittest` antes de cada `git push`. Si una
prueba falla, devuelve un código distinto de cero y Git cancela el push.

## Instalación

Desde la raíz del repositorio, en PowerShell:

```powershell
./hooks/instalar.ps1
```

El agente debe corregir los errores mostrados por la suite antes de volver a
intentar el push. No se usa `--no-verify`: saltarse el hook permitiría subir
código no verificado.
