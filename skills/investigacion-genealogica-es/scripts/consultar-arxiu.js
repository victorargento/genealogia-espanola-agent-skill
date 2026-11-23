// PEGA ESTE ARCHIVO COMPLETO EN LA CONSOLA DEL BUSCADOR DEL ARCHIVO.
// Cambia solo CONFIG. No necesita instalar nada ni enviar datos a otro servicio.
(async () => {
  const CONFIG = {
    etiqueta: 'mi-consulta',
    campos: { nom: '', a1: '', a2: '' },
    paginaInicial: 1,
    maxPaginas: 20,
    pausaMs: 3000,
    usarCache: true
  };
  const HOSTS = ['www.arxparrvalencia.org', 'arxparrvalencia.org'];
  if (!Object.values(CONFIG.campos).some(v => String(v ?? '').trim())) {
    console.error('Rellena CONFIG.campos con los datos de una búsqueda concreta. No se ejecutan búsquedas vacías.');
    return;
  }
  if (location.protocol !== 'https:' || !HOSTS.includes(location.hostname)) {
    console.error('Abre primero https://www.arxparrvalencia.org/genealogiac_nou.php?origen=3 y ejecuta el script allí.');
    return;
  }
  if (window.archivoFamiliar?.ejecutando) {
    console.warn('Ya hay una consulta activa. Para detenerla: archivoFamiliar.detener()');
    return;
  }
  const resultado = {
    version: 1, fuente: 'Arxiu Parroquial València',
    iniciado: new Date().toISOString(), configuracion: CONFIG,
    tipo_evidencia: 'Texto y tablas del índice web; no actas originales',
    estado: 'en_curso', paginas: [], incidencias: []
  };
  let parar = false, controlador;
  function descargar() {
    const blob = new Blob([JSON.stringify(resultado, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `archivo-${CONFIG.etiqueta.replace(/[^a-z0-9-]/gi, '-')}-${Date.now()}.json`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 10000);
  }
  window.archivoFamiliar = {
    ejecutando: true, resultado, descargar,
    detener() { parar = true; controlador?.abort(); }
  };
  const url = new URL('/listados_genealogia_nou1.php', location.origin);
  for (const [k, v] of Object.entries(CONFIG.campos)) {
    if (v !== '' && v != null) url.searchParams.set(k, String(v));
  }
  url.searchParams.set('filtre', 'P');
  url.searchParams.set('orden', 'apelli');
  const inicio = Math.max(1, Math.trunc(Number(CONFIG.paginaInicial) || 1));
  const limite = Math.min(50, Math.max(1, Math.trunc(Number(CONFIG.maxPaginas) || 20)));
  let huboPeticion = false;
  try {
    for (let pagina = inicio; pagina < inicio + limite; pagina++) {
      resultado.siguiente_pagina = pagina;
      if (parar) { resultado.estado = 'detenido'; break; }
      url.searchParams.set('pagina', String(pagina));
      const clave = 'archivo-familiar:v1:' + url.href;
      let ficha = null;
      if (CONFIG.usarCache) {
        try { ficha = JSON.parse(localStorage.getItem(clave)); } catch { /* caché opcional */ }
      }
      if (!ficha) {
        if (huboPeticion) await new Promise(r => setTimeout(r, Math.max(2000, CONFIG.pausaMs || 2000)));
        if (parar) { resultado.estado = 'detenido'; break; }
        controlador = new AbortController();
        const timeout = setTimeout(() => controlador.abort(), 45000);
        let respuesta, html;
        try {
          huboPeticion = true;
          respuesta = await fetch(url.href, { credentials: 'same-origin', signal: controlador.signal });
          if (!respuesta.ok) throw new Error(`HTTP ${respuesta.status}; no equivale a cero resultados.`);
          html = await respuesta.text();
        } finally { clearTimeout(timeout); }
        const doc = new DOMParser().parseFromString(html, 'text/html');
        doc.querySelectorAll('script,style,noscript').forEach(n => n.remove());
        const texto = doc.body.textContent.replace(/\s+/g, ' ').trim();
        const cero = /No hemos encontrado ning[uú]n registro que cumpla sus condiciones de b[uú]squeda/i.test(texto);
        const paginacion = texto.match(/Mostrando p[aá]gina\s*(\d+)\s*de\s*(\d+)/i);
        const id = texto.match(/IDENTIFICADOR\s*(\d+)/i)?.[1] || null;
        if (!cero && (!paginacion || !id)) {
          throw new Error('Respuesta no reconocida: puede ser Cloudflare, un error o un cambio de página. No se considera consulta negativa. Abre el buscador normalmente y comprueba el acceso.');
        }
        if (paginacion && Number(paginacion[1]) !== pagina) throw new Error('La página recibida no coincide con la solicitada.');
        ficha = {
          url: url.href, recuperado: new Date().toISOString(), pagina,
          total_paginas: cero ? 0 : Number(paginacion[2]),
          identificador: id, sin_resultados: cero, texto,
          filas: Array.from(doc.querySelectorAll('tr'))
            .filter(tr => !tr.querySelector('table'))
            .map(tr => Array.from(tr.children).map(td => td.textContent.replace(/\s+/g, ' ').trim()))
        };
        try { localStorage.setItem(clave, JSON.stringify(ficha)); }
        catch { resultado.incidencias.push('No se pudo guardar una página en la caché; sí se incluye en el archivo.'); }
      }
      resultado.paginas.push(ficha);
      console.log(`Guardada página ${pagina}/${ficha.total_paginas}; ficha ${ficha.identificador || 'sin resultados'}`);
      if (ficha.sin_resultados || pagina >= ficha.total_paginas) {
        resultado.estado = inicio === 1 ? 'completo' : 'tramo_hasta_final';
        break;
      }
      resultado.siguiente_pagina = pagina + 1;
    }
    if (resultado.estado === 'en_curso') resultado.estado = 'limite_alcanzado';
    if (['completo', 'tramo_hasta_final'].includes(resultado.estado)) delete resultado.siguiente_pagina;
  } catch (error) {
    resultado.estado = parar ? 'detenido' : 'error';
    resultado.incidencias.push({ url: url.href, mensaje: String(error.message || error) });
    console.warn('Consulta detenida; se conserva lo obtenido.', error.message);
  } finally {
    resultado.finalizado = new Date().toISOString();
    window.archivoFamiliar.ejecutando = false;
    descargar();
    console.log('Resultado:', resultado.estado, 'Páginas guardadas:', resultado.paginas.length);
    console.log('Si no se descarga, ejecuta archivoFamiliar.descargar(). Para ver el resultado: archivoFamiliar.resultado');
  }
})();
