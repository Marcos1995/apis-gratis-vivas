<!-- managed-by-telegram-cursor-bot:agent-kit -->
# Contexto del proyecto

## Produccion
- URL: https://github.com/Marcos1995/apis-gratis-vivas
- Vista: https://marcos1995.github.io/apis-gratis-vivas/ (repo público; Chrome)
- Vista local: `index.html`

## Estado
- `fetch.py` parsea el README de public-apis (tablas Auth/HTTPS/CORS), hace un GET de 10 s por URL y escribe `data/items.json` y `data/history.json`.
- Cada página lleva estado (vivo/muerto), latencia, autenticación, HTTPS, CORS y uptime de 30 días. Grupo = categoría del README.
- Vivo = HTTP 2xx, 3xx, 401, 403 o 405. El historial solo añade una fila cuando cambia estado, auth, HTTPS o CORS.
- `build.py` genera el sitio en `_site/` (no editar; viene del site-kit).

## Stack
- Python 3, solo stdlib (`urllib`). Sin dependencias.

## Comandos utiles
- Instalar: nada
- Test: `python fetch.py && python build.py` (indexables en la línea `ok:` de build; mínimo 300)
- Dev: `python build.py` y abrir `_site/index.html`

## Notas para el agente
- No editar `build.py` ni `.github/workflows/update.yml`.
- Fuente: https://github.com/public-apis/public-apis (MIT). Si el README no responde o hay menos de 300 APIs, salir con código 1 sin tocar `data/`.
- Lean kit (ver AGENTS.md)
