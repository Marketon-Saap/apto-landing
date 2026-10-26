# APTO Landing Madre

Repo dedicado del landing madre APTO gestionado por Marketon (Fractional CMO 2026H2).

- **URL producción**: https://landing.apto.mx/
- **Backend Worker**: `apto-landing-api.marketon-saap.workers.dev`
- **HubSpot**: pipeline "Marketon" · portal 2583031
- **Google Ads**: cuenta 7021324934 · Enhanced Conversions activas
- **GTM**: GTM-K7J6MQ8
- **Meta Pixel**: 721335916342252

Deploy: push a `main` → GitHub Pages actualiza en <1 min · Cloudflare no interviene (hosting es GitHub Pages).

Fork del contenido original en `MktGrupoPlasenciaAutomotriz/marketon-clients/clients/apto/landing/` — se mantiene ese repo como historial de trabajo multi-cliente Marketon.

## Chat Jazz en la landing (desde el 26-oct-2026)

- `jazz-widget.js` es una **copia de despliegue**: el canónico vive en `marketon-clients/clients/apto/chat-worker/widget/jazz-widget.js` y se copia tal cual aquí y a `previews/apto/jazz-chat-20261026/`. No se edita aquí.
- Se carga al final de `index.html` con `window.JAZZ_CHAT = { api: 'https://apto-chat-api.marketon-saap.workers.dev' }`. El cerebro es el Worker `apto-chat-api` (cuenta Marketon-SaaP); `GET /health` dice qué cerebro contesta (claude | jazz | mock) y si la base de conversaciones está conectada.
- **Prospectos:** el chat nunca registra por su cuenta. Cuando la persona quiere contacto, abre el formulario de la landing prellenado (nombre, correo, empresa, puesto, industria, tamaño y su reto) y ella lo envía; entra por el mismo Worker `apto-landing-api` → HubSpot, con `form_origin_cta = chat` (`marketon_form_origin` en HubSpot).
- **Medición:** `capture.js` manda `lead_channel` (`chat` | `landing_page`) y `chat_session_id` en `form_submit_success` y en `context.meta`; en GTM el tag 84 (`generate_lead`) lleva `lead_channel` y los eventos `chat_*` (chat_open, chat_start = primer mensaje, chat_message, chat_reply, chat_lead_prefill, chat_action, chat_error, chat_close) los manda el tag "GA4 · Landing · chat Jazz". Dimensiones personalizadas en GA4: `lead_channel`, `chat_session_id`, `chat_action`.
- **Conversaciones:** cada turno se guarda en la base D1 `apto-leads` (tablas `chat_sessions` y `chat_messages`), sin IPs.
- **Apagar el chat:** quitar las dos líneas del `<script>` de Jazz al final de `index.html` y hacer push (GitHub Pages redepliega en menos de un minuto). El Worker puede seguir vivo sin la landing.
