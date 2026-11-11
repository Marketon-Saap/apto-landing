#!/usr/bin/env python3
"""Genera /desarrollo-de-software/index.html a partir de index.html (11-nov-2026).
Misma capa de diseño, formulario y medición; contenido enfocado en desarrollo de software
para la campaña "APTO · Desarrollo 2026H2". Todo el texto sale de lo ya publicado en la landing.
Uso: python3 tools/build_desarrollo.py  (desde la raíz del repo)"""
import re, json, os

src = open('index.html', encoding='utf-8').read()
s = src
URL = 'https://landing.apto.mx/desarrollo-de-software/'

def sub1(old, new):
    global s
    assert s.count(old) >= 1, old[:80]
    s = s.replace(old, new)

# 1) rutas relativas -> absolutas (la página vive en un subdirectorio)
s = re.sub(r'(\s(?:href|src|action|poster|data-src)=")(?!https?:|/|#|mailto:|tel:|data:|javascript:)([^"]+)"', r'\1/\2"', s)
s = re.sub(r'srcset="([^"]+)"', lambda m: 'srcset="' + ', '.join(('/' + p.strip()) if not p.strip().startswith(('/', 'http')) else p.strip() for p in m.group(1).split(',')) + '"', s)

# 2) head: title, description, canonical, og
TITLE = 'Desarrollo de software a la medida en México · APTO'
DESC = 'Software a la medida, aplicaciones, ecommerce B2B e integraciones con los sistemas que ya operas: arquitectura, desarrollo, pruebas y puesta en marcha.'
s = re.sub(r'<title>.*?</title>', f'<title>{TITLE}</title>', s, count=1, flags=re.S)
s = re.sub(r'(<meta name="description" content=")[^"]*"', rf'\g<1>{DESC}"', s, count=1)
s = re.sub(r'(<meta property="og:description" content=")[^"]*"', rf'\g<1>{DESC}"', s)
s = re.sub(r'(<meta content=")[^"]*(" property="og:description")', rf'\g<1>{DESC}\2', s)
s = re.sub(r'(<meta name="twitter:description" content=")[^"]*"', rf'\g<1>{DESC}"', s)
s = re.sub(r'(<meta property="og:title" content=")[^"]*"', rf'\g<1>{TITLE}"', s)
s = re.sub(r'(<meta content=")[^"]*(" property="og:title")', rf'\g<1>{TITLE}\2', s)
s = s.replace('<link rel="canonical" href="https://landing.apto.mx/">', f'<link rel="canonical" href="{URL}">')
# hreflang: cada página se declara a sí misma (antes apuntaba a la portada y contradecía la canónica)
s = s.replace('<link rel="alternate" hreflang="es-MX" href="https://landing.apto.mx/">', f'<link rel="alternate" hreflang="es-MX" href="{URL}">')
s = s.replace('<link rel="alternate" hreflang="x-default" href="https://landing.apto.mx/">', f'<link rel="alternate" hreflang="x-default" href="{URL}">')
s = s.replace('<meta property="og:url" content="https://landing.apto.mx/">', f'<meta property="og:url" content="{URL}">')

# 3) hero
s = re.sub(r'<h1>[^<]*</h1>', '<h1>Desarrollo de software a la medida para tu empresa.</h1>', s, count=1)
s = re.sub(r'(<p class="hero-sub">)[^<]*(</p>)', r'\1Desarrollamos software a la medida, aplicaciones e integraciones que facilitan el trabajo diario, cuando lo que hay en el mercado no se adapta a tu operación.\2', s, count=1)

# 4) Qué hacemos -> Qué desarrollamos
chips = ['Software a la medida', 'Desarrollo de sistemas', 'Desarrollo de aplicaciones', 'Aplicaciones móviles',
         'Ecommerce y plataformas B2B', 'Integraciones con sistemas existentes', 'Arquitectura de software empresarial',
         'Automatización con inteligencia artificial', 'Diseño de producto digital (UX/UI)', 'Desarrollo front y back end']
ul = '<ul class="servicios__list">' + ''.join(f'<li><a href="#productos" data-track="servicio_chip_click" data-item="{c}">{c}</a></li>' for c in chips) + '</ul>'
serv = ('<section class="servicios" id="servicios" aria-labelledby="servicios-title">\n<div class="container">\n'
        '<p class="eyebrow">Qué desarrollamos</p>\n'
        '<h2 id="servicios-title" class="servicios__title">Desarrollo de software a la medida, aplicaciones, plataformas de ecommerce B2B e integraciones con los sistemas que ya operas.</h2>\n'
        '<p class="lead">Cuando lo que existe en el mercado no se adapta a tu operación, construimos el sistema a la medida: arquitectura de software empresarial, desarrollo front y back end, pruebas y puesta en marcha, con la estrategia de negocio y el diseño en el mismo equipo. Trabajamos con corporativos y empresas medianas que ya operan.</p>\n'
        + ul + '\n</div>\n</section>')
s = re.sub(r'<!-- PROPUESTA 22-sep.*?<!-- /PROPUESTA -->', serv, s, count=1, flags=re.S)

# 5) seis retos -> cuatro tipos de proyecto de software
def reto(n, prod, title, tema, dolor, items, caso):
    li = ''.join(f'<li>{i}</li>\n' for i in items)
    return (f'<article class="reto">\n<div class="reto__head">\n<span class="reto__num">{n}</span>\n<h3 class="reto__title">{title}</h3>\n'
            f'<p class="reto__tema">{tema}</p>\n</div>\n<p class="reto__dolor">{dolor}</p>\n<details class="reto__more">\n'
            f'<summary data-track="producto_expand" data-producto="{prod}">Cómo podemos ayudarte</summary>\n<div class="reto__body">\n'
            f'<ul class="reto__si">\n{li}</ul>\n<p class="reto__caso">{caso}</p>\n</div>\n</details>\n</article>\n')
retos = (reto('01', 'software', 'Tu operación necesita software a la medida', 'Desarrollo de software y arquitectura de software empresarial',
              'La información está dispersa y los sistemas no se conectan. Desarrollamos software a la medida, aplicaciones e integraciones que faciliten el trabajo diario, cuando lo que hay en el mercado no se adapta a tu operación.',
              ['Análisis de procesos y oportunidades de automatización', 'Desarrollo de sistemas y aplicaciones a la medida', 'Arquitectura de software empresarial, pruebas y puesta en marcha', 'Información y tableros para dar seguimiento a la operación'],
              'Fanosa · automatización comercial')
         + reto('02', 'apps', 'Necesitas una aplicación para tus clientes o tu equipo', 'Diseño, validación y desarrollo de aplicaciones',
              'Diseñamos, validamos y desarrollamos aplicaciones y productos digitales a partir de las tareas reales de quien las va a usar.',
              ['Investigación con usuarios, prototipos y pruebas antes de construir', 'Diseño de experiencia e interfaces (UX/UI)', 'Desarrollo front y back end y documentación'],
              'Be Grand · herramienta de postventa')
         + reto('03', 'ecommerce', 'Tus clientes empresa todavía dependen de un asesor para comprar', 'Ecommerce B2B y plataformas de venta entre empresas',
              'Rediseñamos y construimos plataformas de ecommerce B2B, tu canal de venta entre empresas, para facilitar la consulta de productos y la gestión de pedidos.',
              ['Diseño de la plataforma a partir de las tareas de tus clientes', 'Desarrollo e integración con los sistemas que ya operas', 'Pruebas y puesta en marcha'],
              'APYMSA · plataforma B2B de autopartes')
         + reto('04', 'integraciones', 'Tus sistemas no se hablan entre sí', 'Integraciones con sistemas existentes y automatización con inteligencia artificial',
              'Buena parte del trabajo es conectar lo que ya opera: integraciones con los sistemas existentes, automatización de procesos y tableros para dar seguimiento.',
              ['Herramientas e integraciones con los sistemas existentes', 'Automatización con inteligencia artificial: agentes y asistentes conectados a tus sistemas y datos', 'Integración con especialistas en APIs y arquitectos de software'],
              'Grupo San Carlos · omnicanalidad integrada a los sistemas core del negocio'))
a = s.index('<section class="section section--navy" id="productos">')
z = s.index('</section>', a)
sec = s[a:z]
i = sec.index('<div class="retos">\n') + len('<div class="retos">\n')
j = sec.rindex('</article>\n') + len('</article>\n')
head = sec[:i]
head = re.sub(r'<p class="eyebrow">[^<]*</p>', '<p class="eyebrow">Qué desarrollamos</p>', head, count=1)
head = re.sub(r'<h2>[^<]*</h2>', '<h2>Cuatro tipos de proyecto de desarrollo de software.</h2>', head, count=1)
head = re.sub(r'<p class="lead">[^<]*</p>', '<p class="lead">Podemos entrar solo en una etapa o ser tu proveedor de software a lo largo del proyecto. En la propuesta definimos qué construye APTO, qué corresponde a tu equipo y de qué dependen los tiempos.</p>', head, count=1)
s = s[:a] + head + retos + sec[j:] + s[z:]
s = s.replace('>Los seis retos<', '>Qué desarrollamos<')

# 6) FAQ: solo las de software, en este orden; JSON-LD igual a lo visible
orden = ['¿Hacen desarrollo de software a la medida?', '¿Ustedes desarrollan el software?', '¿Tienen desarrolladores propios?',
         '¿Desarrollan aplicaciones?', '¿Hacen plataformas de ecommerce o venta B2B?', '¿Pueden integrarse con los sistemas que ya usamos?',
         '¿Hacen proyectos con inteligencia artificial?', '¿Hacen diseño UX y UI e investigación de usuarios?',
         '¿Cuánto cuesta un proyecto?', '¿Cuánto tiempo toma un proyecto?', '¿Trabajan con empresas medianas o solo corporativos?',
         '¿Trabajan con startups?', '¿Dónde están y con quién trabajan?']
items = dict(re.findall(r'<details class="faq-item">\n<summary>(.*?)</summary>\n<div class="faq-item__body">(.*?)</div>\n</details>\n', s, re.S))
for q in orden: assert q in items, q
fm = re.search(r'(<details class="faq-item">.*</details>\n)', s, re.S)
s = s[:fm.start()] + ''.join(f'<details class="faq-item">\n<summary>{q}</summary>\n<div class="faq-item__body">{items[q]}</div>\n</details>\n' for q in orden) + s[fm.end():]
ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
      {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', items[q])}} for q in orden]}
s = re.sub(r'<script type="application/ld\+json">\{"@context":"https://schema.org","@type":"FAQPage".*?</script>',
           '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False, separators=(',', ':')) + '</script>', s, count=1, flags=re.S)

for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S): json.loads(b)
os.makedirs('desarrollo-de-software', exist_ok=True)
open('desarrollo-de-software/index.html', 'w', encoding='utf-8').write(
    '<!-- GENERADO por tools/build_desarrollo.py a partir de index.html: no editar a mano -->\n' + s)
print('ok', len(s))
