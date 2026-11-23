# Contribuir

Las contribuciones pueden mejorar la skill, corregir scripts o añadir fuentes
regionales verificadas. Este repositorio no aloja un árbol familiar ni recibe
propuestas de parentesco del autor.

Para informar de un error, usa la plantilla **Problema con la herramienta** y
un ejemplo ficticio mínimo. No adjuntes consultas, resultados ni datos familiares.
Enlaza las fuentes archivísticas cuando propongas documentación nueva.

## Cambios de código o instrucciones

Ejecuta antes de proponer el cambio:

```powershell
python scripts/validate_tree.py examples/familia-ficticia.json --public
python scripts/export_gedcom.py examples/familia-ficticia.json work/familia-ficticia.ged
python scripts/validate_gedcom.py work/familia-ficticia.ged
python scripts/simulate_install.py
```
