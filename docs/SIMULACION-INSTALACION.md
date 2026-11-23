# Simulación de instalación

Fecha de la última prueba: 23/11/2026.

## Escenario

Una persona clona el repositorio e instala la misma skill en un proyecto limpio
para Codex y Claude Code. Después revisa una familia ficticia, aplica el filtro
de publicación, genera un GEDCOM y lo valida.

## Instalación simulada

El instalador creó estas rutas aisladas:

```text
.agents/skills/investigacion-genealogica-es/  Codex
.claude/skills/investigacion-genealogica-es/  Claude Code
```

Las dos copias coincidieron byte por byte con la skill canónica.

## Resultado funcional

- Modelo público: 3 personas, 1 familia y 3 fuentes.
- GEDCOM: 5.5.1 UTF-8, 7 registros, 11 referencias y 53 líneas.
- Enlaces `INDI`/`FAM`: recíprocos.
- Nacimiento inferido: conservado como año, con nota de evidencia.
- Personas vivas o de estado desconocido: rechazadas en modo público.
- Escritura pública: atómica; un rechazo no altera el GEDCOM anterior.
- Errores esperados: salida JSON breve y código de salida distinto de cero.

Una prueba independiente con un agente nuevo confirmó que la skill instalada es
autosuficiente para validar el modelo, generar el GEDCOM y revisar privacidad.
La primera ejecución reveló que faltaban herramientas dentro de la carpeta de
la skill; se añadieron y la segunda ejecución completó el flujo sin escribir un
generador adicional.

## Límites pendientes

- La validación local no sustituye una importación real en Family Echo.
- La detección de posibles homónimos requiere razonamiento y fuentes; el script
  solo impide duplicados de identificador y relaciones estructuralmente
  inválidas.
- La cronología automática es deliberadamente conservadora y no convierte años
  aproximados en fechas exactas.
- El disparo implícito de la skill depende del agente anfitrión; esta prueba usó
  una invocación dirigida para evaluar el contenido y las herramientas.
