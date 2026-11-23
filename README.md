# Genealogía española para agentes

**Primera vez:** lee [Empieza aquí](docs/EMPIEZA-AQUI.md), con instrucciones de
instalación, búsqueda, descarga, análisis y exportación, y textos para copiar.

Herramientas y una skill reutilizable para investigar genealogía en España con
Codex, Claude y otros agentes compatibles con Agent Skills.

## Origen y alcance actual

Este proyecto nace de búsquedas familiares realizadas en
[Arxiu Parroquial València](https://www.arxparrvalencia.org/), nuestra fuente
principal de investigación. Su buscador identifica los archivos diocesanos de
Oriola-Alacant y València: el enfoque práctico actual es valenciano.
No cubre toda España ni garantiza todos los municipios, parroquias o años de
la Comunitat Valenciana. Consulta siempre los fondos indexados por parroquia.

La orientación para otras regiones españolas es una guía de fuentes; todavía
no hay conectores de búsqueda nacionales implementados en esta distribución.
Se incluye una consulta genérica para ejecutar en la consola del portal:
`skills/investigacion-genealogica-es/scripts/consultar-arxiu.js`. El agente prepara
los filtros y el usuario ejecuta la consulta en su navegador. Los lotes privados
familiares quedan fuera. Proyecto independiente, sin afiliación al archivo.

La simulación comprueba copias de instalación y herramientas locales. No acredita
una ejecución en Claude real ni una importación en Family Echo. El filtro
`living: false` es un control técnico, no una revisión completa de privacidad.

El proyecto ayuda a:

- planificar búsquedas según territorio, época y tipo de documento;
- registrar hechos, testimonios e hipótesis sin mezclarlos;
- mantener separados los homónimos hasta disponer de evidencia suficiente;
- validar relaciones y cronología;
- generar un GEDCOM 5.5.1 para aplicaciones como Family Echo;
- revisar una exportación antes de compartirla, si su propietario lo solicita.

## Estructura

```text
skills/investigacion-genealogica-es/  Skill portable
scripts/                              Validación y exportación GEDCOM
examples/                             Familia ficticia para probar el flujo
data/public/                          Nota de separación de datos privados
docs/                                 Política de publicación y contribución
.github/ISSUE_TEMPLATE/               Errores reproducibles con datos ficticios
```

## Instalación de la skill

La carpeta `skills/investigacion-genealogica-es` es la fuente canónica. El
instalador local la copia al directorio que descubre cada herramienta:

```powershell
# Instalar para el usuario actual en Codex y Claude Code
python scripts/install_skill.py --target both --scope user

# Instalar solo dentro de un proyecto concreto
python scripts/install_skill.py --target both --scope project --project-dir C:\ruta\al\proyecto
```

Codex utiliza `.agents/skills` y Claude Code utiliza `.claude/skills`. El
instalador se detiene si ya existe una skill con el mismo nombre; no sobrescribe
una instalación anterior.

En claude.ai también puede comprimirse y subirse la carpeta canónica como skill
personal desde la configuración de Skills, cuando la cuenta lo permita.

## Prueba local

```powershell
python scripts/validate_tree.py examples/familia-ficticia.json --public
python skills/investigacion-genealogica-es/scripts/genealogy_tool.py export-public examples/familia-ficticia.json work/familia-ficticia.ged
python skills/investigacion-genealogica-es/scripts/genealogy_tool.py validate-gedcom work/familia-ficticia.ged
```

La prueba completa de instalación en Codex y Claude se ejecuta con:

```powershell
python scripts/simulate_install.py
```

Véase [`docs/SIMULACION-INSTALACION.md`](docs/SIMULACION-INSTALACION.md).

El JSON es la fuente de verdad. Los archivos GEDCOM son exportaciones generadas;
no deben editarse manualmente ni utilizarse para guardar hipótesis complejas.

## Privacidad

Este repositorio comparte herramientas, instrucciones y ejemplos ficticios.
No incluye el árbol del autor, sus consultas ni sus resultados; tampoco se
prevé publicarlos en otra rama. La guía de publicación es opcional para quien
decida compartir sus propios datos. Véase
[`docs/PUBLIC_TREE_POLICY.md`](docs/PUBLIC_TREE_POLICY.md).

## Licencia

Código e instrucciones bajo licencia MIT. Los documentos históricos y sus
imágenes conservan las condiciones de sus archivos de origen.
