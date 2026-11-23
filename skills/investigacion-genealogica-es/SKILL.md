---
name: investigacion-genealogica-es
description: Investiga genealogía en España, contrasta personas y relaciones con fuentes, mantiene hipótesis separadas y prepara árboles o GEDCOM revisables. Úsala para búsquedas genealógicas españolas, revisión de homónimos, árboles colaborativos y exportaciones; no para afirmar parentescos sin evidencia.
---

# Investigación genealógica en España

Produce una investigación trazable. Cada afirmación debe poder distinguirse
como documento, testimonio, inferencia o hipótesis.

La investigación que originó esta skill utiliza https://www.arxparrvalencia.org/.
Para búsquedas valencianas o peticiones sobre ese portal, lee
[references/arxiu-valencia.md](references/arxiu-valencia.md). Su cobertura es
parcial por parroquia y periodo; no extrapoles los resultados a toda España.
Incluye `scripts/consultar-arxiu.js`, ejecutable por el usuario en la consola
del portal. Antes de prepararlo, lee [references/consulta-consola.md](references/consulta-consola.md).

## Antes de actuar

1. Localiza la memoria o el conjunto de datos existente antes de preguntar de
   nuevo por personas ya registradas.
2. Conserva el material original y su referencia. Una transcripción o índice
   ayuda a buscar, pero no sustituye automáticamente al documento original.
3. Determina territorio, periodo y tipo de acontecimiento. Para elegir fuentes
   españolas, lee [references/fuentes-espana.md](references/fuentes-espana.md).

## Criterio de identidad

No unas personas solo por nombre o apellido. Compara, cuando estén disponibles:

- padres, pareja, hijos y otros vínculos;
- localidad, parroquia y movimientos geográficos;
- fechas y una cronología biológicamente posible;
- profesión, estado civil, domicilio, apodos y testigos;
- signatura, libro, folio, asiento y transcripción.

Registra contradicciones. Si la evidencia no basta, conserva candidatos
separados y describe qué documento resolvería la duda. Una búsqueda fallida,
un error de acceso o una colección incompleta no constituyen una prueba de
ausencia.

Para graduar conclusiones, usa [references/evidencia.md](references/evidencia.md).

## Datos y salidas

Mantén una fuente de verdad estructurada con identificadores estables para
personas, familias y fuentes. Guarda las hipótesis fuera de los hechos
aceptados. No edites el GEDCOM a mano: genéralo desde el modelo y valida
referencias, ciclos, duplicados y cronología.

Para crear o revisar el modelo, lee
[references/modelo-json.md](references/modelo-json.md). La skill incluye
`scripts/genealogy_tool.py`, que valida el JSON, exporta GEDCOM y valida el
archivo generado sin dependencias externas.

Cuando la tarea incluya GEDCOM o Family Echo, lee
[references/gedcom.md](references/gedcom.md). Cuando incluya publicación o
colaboración, lee [references/publicacion.md](references/publicacion.md).

## Resultado esperado

Entrega lo que corresponda a la petición:

- plan de búsqueda con fuentes y variantes;
- inventario de resultados positivos, negativos explícitos e incidencias;
- tabla de hechos y relaciones con fuente y confianza;
- lista de contradicciones y próximos documentos decisivos;
- cambios propuestos al árbol, sin convertir hipótesis en hechos;
- exportación GEDCOM generada y validada cuando se solicite.

No publiques, subas ni sincronices árboles o datos externos sin autorización
para ese destino.
