# Modelo JSON interoperable

El modelo tiene `version`, `people`, `families`, `sources` y `hypotheses`.
Todos los identificadores son estables y únicos.

## Personas

```json
{
  "id": "I1",
  "given_names": "Ana María",
  "surnames": "Navarro Ruiz",
  "sex": "F",
  "living": false,
  "events": [
    {
      "type": "birth",
      "date": "1882-04-12",
      "precision": "exact",
      "place": "Localidad, España",
      "status": "documented",
      "source_ids": ["S1"]
    }
  ]
}
```

`living` admite `true`, `false` o ausencia/null cuando se desconoce. En modo
público solo se admite el valor explícito `false`; un estado desconocido se
excluye hasta revisarlo.

`precision` puede ser `exact`, `month`, `year` o `about`. No completes las
partes ausentes de una fecha. `status` puede ser `documented`, `testimony`,
`inferred`, `hypothesis` o `rejected`.

## Familias

Una familia tiene `id`, una o dos personas en `partners`, cero o más `children`,
`status`, `source_ids` y eventos opcionales. Una persona no puede ser su propio
progenitor ni pertenecer como hijo a dos familias parentales en este modelo
simplificado.

## Fuentes e hipótesis

Cada fuente incluye `id`, `title` y, cuando existan, `repository`, `citation` y
`url`. Las hipótesis deben conservar su afirmación, personas afectadas,
evidencias a favor, contradicciones y documento decisivo pendiente. No uses una
hipótesis como relación GEDCOM confirmada.

## Herramienta incluida

Desde la carpeta de la skill:

```powershell
python scripts/genealogy_tool.py validate arbol.json --public
python scripts/genealogy_tool.py export-public arbol.json arbol-publico.ged
python scripts/genealogy_tool.py validate-gedcom arbol.ged
```

`export-public` valida privacidad y solo reemplaza el archivo de salida cuando
la generación termina correctamente. `export` queda disponible para árboles
privados y no debe confundirse con una publicación.
