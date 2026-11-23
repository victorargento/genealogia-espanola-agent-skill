# GEDCOM y Family Echo

Usa el modelo JSON como fuente de verdad y GEDCOM como formato de intercambio.
La exportación recomendada para compatibilidad amplia es GEDCOM 5.5.1 UTF-8.

Para una publicación usa `export-public`; esta orden rechaza personas vivas o
de estado desconocido antes de escribir el archivo.

## Antes de exportar

- valida que todos los identificadores referenciados existan;
- comprueba enlaces familiares recíprocos y ausencia de ciclos;
- conserva fechas aproximadas como aproximadas;
- no conviertas candidatos en padres o parejas confirmados;
- incluye citas y notas suficientes para entender las reservas;
- genera una edición pública separada cuando el destino sea público.

La codificación de evidencia de esta skill es estable: los hechos
`documented` usan las etiquetas GEDCOM ordinarias; `testimony`, `inferred` e
`hypothesis` añaden una nota `Estado de evidencia: <estado>`. Las hipótesis que
no deban formar todavía una relación quedan fuera de `FAM` y permanecen en el
modelo JSON.

## Family Echo

Prueba cada versión en una familia nueva antes de reemplazar el árbol de uso.
No presupongas que dos importaciones GEDCOM se fusionarán sin duplicados. Guarda
el archivo importado y la versión del modelo que lo produjo.

Una validación estructural local no demuestra que todas las aplicaciones vayan
a mostrar igual las notas, fuentes o eventos personalizados. Registra cualquier
pérdida observada durante la prueba de importación.
