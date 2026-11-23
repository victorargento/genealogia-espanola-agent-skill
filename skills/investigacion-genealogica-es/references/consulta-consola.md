# Preparar una consulta

Entrega el archivo completo scripts/consultar-arxiu.js con CONFIG adaptado a la
petición. No pidas que el usuario programe. Campos conocidos del flujo original:
nom (nombre), a1 y a2 (apellidos), nompa (padre), nomma (madre), nomcon y cognomcj
(nombre y primer apellido del cónyuge). Verifica los campos del formulario antes
de añadir otros. El script utiliza el endpoint observado en el proyecto,
listados_genealogia_nou1.php; no es una API oficial garantizada.

Pide abrir https://www.arxparrvalencia.org/genealogiac_nou.php?origen=3, comprobar
el acceso y ejecutar el archivo en la consola. Si el navegador muestra una
advertencia de pegado, no indiques que la desactive; ofrece consulta manual.
Explica que el código consulta ese dominio y descarga resultados localmente.

Una consulta por ejecución, máximo 20 páginas por defecto y pausa de 3 segundos.
El usuario puede detener con archivoFamiliar.detener() y descargar de nuevo con
archivoFamiliar.descargar(). Para continuar, cambia paginaInicial al valor
siguiente_pagina del JSON, conservando filtros y archivos de todos los tramos.
El estado tramo_hasta_final no demuestra que estén presentes los tramos previos.

Al recibir el JSON, conserva filtros, fecha, URL, texto y filas. Cuenta IDs
distintos; distingue fichas de personas. Un error o límite no es resultado
negativo. Compara filiación, fechas y pareja antes de proponer identidades.
Los JSON descargados no son el modelo del exportador: primero hay que analizar
y convertir los hallazgos al modelo descrito en modelo-json.md. Conserva las
hipótesis y originales aparte; genera GEDCOM solo tras revisión.

No se ha probado esta versión genérica contra una sesión real del portal.
