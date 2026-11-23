# Política del árbol público

El repositorio público puede incluir un árbol genealógico derivado del proyecto
privado, pero nunca la base completa ni una rama Git con información privada.

## Se publica

- personas fallecidas cuya publicación haya sido revisada;
- fechas y localidades históricas respaldadas por fuentes;
- relaciones documentadas o hipótesis claramente etiquetadas;
- citas archivísticas y enlaces permitidos;
- un GEDCOM generado a partir de esos mismos datos públicos.

## Se excluye

- personas vivas o de estado vital incierto en generaciones recientes;
- domicilios, teléfonos, correos, identificadores y documentos personales;
- testimonios familiares que no estén destinados a publicación;
- imágenes cuya licencia o archivo de origen no permita redistribución;
- resultados brutos que puedan contener información ajena al árbol publicado.

## Flujo de publicación

1. Generar `data/public/arbol.json` desde la base privada mediante una lista
   explícita de personas admitidas.
2. Ejecutar `scripts/validate_tree.py data/public/arbol.json --public`.
3. Revisar manualmente el diff y las fuentes.
4. Generar el GEDCOM público.
5. Publicar ambos en la rama principal del repositorio público.

Una rama separada no es una medida de privacidad. Si un dato entra en cualquier
rama o commit remoto, debe considerarse potencialmente público.
