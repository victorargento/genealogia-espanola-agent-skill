# Empieza aquí

Esta skill ayuda a investigar familiares en Arxiu Parroquial València. Su
cobertura valenciana es parcial por parroquia, sacramento y periodo. No es un
buscador de toda España ni un servicio oficial del archivo.

## 1. Instalar

Descarga el repositorio y abre su carpeta. Requisito para las herramientas:
Python 3.10 o posterior. El script del navegador no necesita Python.

En Codex puedes pedir:

> Usa skill-installer para instalar investigacion-genealogica-es desde la carpeta
> skills/investigacion-genealogica-es del repositorio
> https://github.com/victorargento/genealogia-espanola-agent-skill

Para instalación local en Codex o Claude Code, desde la carpeta descargada:

```powershell
python scripts/install_skill.py --target codex --scope user
python scripts/install_skill.py --target claude --scope user
```

Ejecuta solo el comando de tu aplicación. El instalador copia una skill; no
instala Codex, Claude ni Python, y no sobrescribe una skill ya existente.
Si no aparece, abre una sesión nueva o reinicia la aplicación.

En Claude con soporte para cargar skills, sube un ZIP de la carpeta
skills/investigacion-genealogica-es. La disponibilidad depende de la modalidad.
En un chat de ChatGPT sin instalación de skills, adjuntar archivos permite
trabajar con ellos en esa conversación; no equivale a instalar una skill
persistente. Pide que lea SKILL.md y sus referencias y comprueba si puede ejecutar
Python. Si no puede, ejecuta los comandos localmente.

## 2. Pedir la primera búsqueda

> Usa investigacion-genealogica-es. Quiero investigar a [nombre y apellidos],
> relacionado con [localidad], hacia [año aproximado]. Sé que [familiares].
> Comprueba la cobertura de Arxiu Parroquial València y prepárame el archivo
> completo de consulta para el navegador. No inventes los datos que falten.

## 3. Consultar el archivo

Abre https://www.arxparrvalencia.org/genealogiac_nou.php?origen=3 y comprueba que
ves el formulario. Abre herramientas de desarrollador (F12), pestaña Consola,
y ejecuta el script preparado después de revisarlo. Si prefieres no ejecutar
código o el navegador impide pegarlo, usa el formulario manualmente y guarda
las fichas y sus enlaces. No necesitas cambiar protecciones del navegador.

El script descarga un JSON. Consulta solo el dominio del archivo; no sube tu
árbol a otros servicios. Conserva los JSON aunque el navegador guarde caché.
Para detener: archivoFamiliar.detener(). Para repetir descarga:
archivoFamiliar.descargar(). Un error de acceso conserva resultados parciales.

## 4. Analizar y continuar

Adjunta el JSON al chat y escribe:

> Analiza estas fichas. Separa documentos, testimonios e hipótesis; conserva
> fuentes y contradicciones. Dime qué consultas están completas y prepara
> únicamente las páginas pendientes o una nueva búsqueda justificada.

No todos los resultados serán familiares. El agente debe preparar un modelo
revisable antes de generar el árbol.

## 5. Exportar para Family Echo

> Con las relaciones revisadas, prepara el modelo JSON y un GEDCOM para Family
> Echo. Conserva las reservas y explícame cualquier información no exportable.
> No subas todavía los datos a ningún servicio.

Importa el GEDCOM en una familia nueva y comprueba fechas, tildes, fuentes y
parentescos. La validación local no sustituye esa comprobación. Para publicar
una copia en GitHub se necesita una revisión de privacidad adicional: la marca
living:false por sí sola no anonimiza notas ni documentos.

## Estado de las pruebas

Probados con ejemplo ficticio: instalación local y generación/validación básica
de GEDCOM. Pendientes: sesión real de Claude, importación real en Family Echo y
consulta del nuevo script genérico en el portal. No prometemos esos resultados.
