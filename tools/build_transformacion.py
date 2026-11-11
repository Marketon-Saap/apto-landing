#!/usr/bin/env python3
"""Genera /transformacion-digital/index.html a partir de index.html (11-nov-2026).
Misma capa de diseño, formulario y medición; contenido enfocado en transformación digital para el
grupo "T2 Core · Transformación digital" de la campaña de Adquisición. Texto tomado de lo ya publicado.
Uso: python3 tools/build_transformacion.py  (desde la raíz del repo)"""
import re, json, os

s = open('index.html', encoding='utf-8').read()
URL = 'https://landing.apto.mx/transformacion-digital/'

s = re.sub(r'(\s(?:href|src|action|poster|data-src)=")(?!https?:|/|#|mailto:|tel:|data:|javascript:)([^"]+)"', r'\1/\2"', s)
s = re.sub(r'srcset="([^"]+)"', lambda m: 'srcset="' + ', '.join(('/' + p.strip()) if not p.strip().startswith(('/', 'http')) else p.strip() for p in m.group(1).split(',')) + '"', s)

TITLE = 'Consultoría de transformación digital para empresas · APTO'
DESC = 'Transformación digital para corporativos y empresas medianas: integramos estrategia, diseño y tecnología para transformar ecosistemas, crear nuevos canales y optimizar operaciones.'
s = re.sub(r'<title>.*?</title>', f'<title>{TITLE}</title>', s, count=1, flags=re.S)
s = re.sub(r'(<meta name="description" content=")[^"]*"', rf'\g<1>{DESC}"', s, count=1)
s = re.sub(r'(<meta name="twitter:description" content=")[^"]*"', rf'\g<1>{DESC}"', s)
s = re.sub(r'(<meta content=")[^"]*(" property="og:description")', rf'\g<1>{DESC}\2', s)
s = re.sub(r'(<meta property="og:description" content=")[^"]*"', rf'\g<1>{DESC}"', s)
s = re.sub(r'(<meta content=")[^"]*(" property="og:title")', rf'\g<1>{TITLE}\2', s)
s = re.sub(r'(<meta property="og:title" content=")[^"]*"', rf'\g<1>{TITLE}"', s)
s = s.replace('<link rel="canonical" href="https://landing.apto.mx/">', f'<link rel="canonical" href="{URL}">')
s = s.replace('<meta property="og:url" content="https://landing.apto.mx/">', f'<meta property="og:url" content="{URL}">')

s = re.sub(r'<h1>[^<]*</h1>', '<h1>Transformación digital para tu empresa.</h1>', s, count=1)
s = re.sub(r'(<p class="hero-sub">)[^<]*(</p>)', r'\1Integramos estrategia, diseño y tecnología para transformar ecosistemas, crear nuevos canales, optimizar operaciones y habilitar un crecimiento sostenible.\2', s, count=1)

chips = ['Transformación digital', 'Consultoría de transformación digital', 'Diseño de servicios y experiencias omnicanales',
         'Experiencia del cliente', 'Digitalización de la operación', 'Automatización e inteligencia artificial aplicada al negocio',
         'Software a la medida', 'Integraciones con sistemas existentes', 'Estrategia de negocio', 'Equipos de innovación y diseño']
ul = '<ul class="servicios__list">' + ''.join(f'<li><a href="#productos" data-track="servicio_chip_click" data-item="{c}">{c}</a></li>' for c in chips) + '</ul>'
serv = ('<section class="servicios" id="servicios" aria-labelledby="servicios-title">\n<div class="container">\n'
        '<p class="eyebrow">Transformación digital</p>\n'
        '<h2 id="servicios-title" class="servicios__title">Consultoría de transformación digital: estrategia de negocio, diseño de servicios, digitalización de la operación y desarrollo de software en el mismo equipo.</h2>\n'
        '<p class="lead">Las empresas necesitan conectar productos, servicios, procesos y tecnología para entregar valor de forma consistente en cada punto de contacto. Trabajamos con corporativos y empresas medianas que ya operan, en proyectos que se definen, se construyen y se ponen en marcha.</p>\n'
        + ul + '\n</div>\n</section>')
s = re.sub(r'<!-- PROPUESTA 22-sep.*?<!-- /PROPUESTA -->', serv, s, count=1, flags=re.S)

# retos: el de transformación digital (06) primero, renumerados
a = s.index('<section class="section section--navy" id="productos">'); z = s.index('</section>', a); sec = s[a:z]
i = sec.index('<div class="retos">\n') + len('<div class="retos">\n'); j = sec.rindex('</article>\n') + len('</article>\n')
arts = re.findall(r'<article class="reto">.*?</article>\n', sec[i:j], re.S)
assert len(arts) == 6
orden = [arts[5], arts[2], arts[0], arts[1], arts[3], arts[4]]
orden = [re.sub(r'<span class="reto__num">\d+</span>', f'<span class="reto__num">{k+1:02d}</span>', x) for k, x in enumerate(orden)]
head = sec[:i]
head = re.sub(r'<p class="eyebrow">[^<]*</p>', '<p class="eyebrow">Por dónde empieza</p>', head, count=1)
head = re.sub(r'<h2>[^<]*</h2>', '<h2>Seis puntos de partida para la transformación digital.</h2>', head, count=1)
s = s[:a] + head + ''.join(orden) + sec[j:] + s[z:]

# FAQ: transformación digital primero
items = re.findall(r'<details class="faq-item">\n<summary>(.*?)</summary>\n<div class="faq-item__body">(.*?)</div>\n</details>\n', s, re.S)
q0 = '¿Hacen consultoría de transformación digital?'
assert any(q == q0 for q, _ in items)
items = [x for x in items if x[0] == q0] + [x for x in items if x[0] != q0]
fm = re.search(r'(<details class="faq-item">.*</details>\n)', s, re.S)
s = s[:fm.start()] + ''.join(f'<details class="faq-item">\n<summary>{q}</summary>\n<div class="faq-item__body">{b}</div>\n</details>\n' for q, b in items) + s[fm.end():]
ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
      {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'<[^>]+>', '', b)}} for q, b in items]}
s = re.sub(r'<script type="application/ld\+json">\{"@context":"https://schema.org","@type":"FAQPage".*?</script>',
           '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False, separators=(',', ':')) + '</script>', s, count=1, flags=re.S)
for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S): json.loads(b)
os.makedirs('transformacion-digital', exist_ok=True)
open('transformacion-digital/index.html', 'w', encoding='utf-8').write(
    '<!-- GENERADO por tools/build_transformacion.py a partir de index.html: no editar a mano -->\n' + s)
print('ok', len(s))
