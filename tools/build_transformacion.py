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
DESC = 'Transformación digital para empresas: integramos estrategia, diseño y tecnología para crear nuevos canales, optimizar operaciones y crecer.'
s = re.sub(r'<title>.*?</title>', f'<title>{TITLE}</title>', s, count=1, flags=re.S)
s = re.sub(r'(<meta name="description" content=")[^"]*"', rf'\g<1>{DESC}"', s, count=1)
s = re.sub(r'(<meta name="twitter:description" content=")[^"]*"', rf'\g<1>{DESC}"', s)
s = re.sub(r'(<meta content=")[^"]*(" property="og:description")', rf'\g<1>{DESC}\2', s)
s = re.sub(r'(<meta property="og:description" content=")[^"]*"', rf'\g<1>{DESC}"', s)
s = re.sub(r'(<meta content=")[^"]*(" property="og:title")', rf'\g<1>{TITLE}\2', s)
s = re.sub(r'(<meta property="og:title" content=")[^"]*"', rf'\g<1>{TITLE}"', s)
s = s.replace('<link rel="canonical" href="https://landing.apto.mx/">', f'<link rel="canonical" href="{URL}">')
# hreflang: cada página se declara a sí misma (antes apuntaba a la portada y contradecía la canónica)
s = s.replace('<link rel="alternate" hreflang="es-MX" href="https://landing.apto.mx/">', f'<link rel="alternate" hreflang="es-MX" href="{URL}">')
s = s.replace('<link rel="alternate" hreflang="x-default" href="https://landing.apto.mx/">', f'<link rel="alternate" hreflang="x-default" href="{URL}">')
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

# retos -> cinco frentes de la transformación digital, con los textos de apto.mx/servicios (11-nov-2026)
def reto(n, prod, title, tema, dolor, items, caso):
    li = ''.join(f'<li>{i}</li>\n' for i in items)
    return (f'<article class="reto">\n<div class="reto__head">\n<span class="reto__num">{n}</span>\n<h3 class="reto__title">{title}</h3>\n'
            f'<p class="reto__tema">{tema}</p>\n</div>\n<p class="reto__dolor">{dolor}</p>\n<details class="reto__more">\n'
            f'<summary data-track="producto_expand" data-producto="{prod}">Qué logramos</summary>\n<div class="reto__body">\n'
            f'<ul class="reto__si">\n{li}</ul>\n<p class="reto__caso">{caso}</p>\n</div>\n</details>\n</article>\n')
frentes = (reto('01', 'omnicanal', 'Tus canales funcionan por separado', 'Diseño de servicios y experiencias omnicanales',
                'La experiencia de servicio es crítica para el desempeño comercial. La fidelidad del cliente no existe ante un servicio complicado o que falla, mantener la excelencia cuesta en la operación y la integración omnicanal para atender a los usuarios se vuelve cada vez más compleja.',
                ['Comprendemos las oportunidades del negocio y la relación con tus clientes', 'Identificamos las necesidades del usuario en cada etapa del servicio', 'Co-diseñamos los flujos entre canales remotos y presenciales, con una visión de sistema', 'Validamos los conceptos con prototipos y definimos las capacidades del servicio y un plan de acción', 'Desarrollamos la tecnología e implementamos procesos y equipos para operar el Mínimo Servicio Viable'],
                'Grupo San Carlos · omnicanalidad integrada a los sistemas core del negocio')
         + reto('02', 'productos', 'Tus activos digitales no están a la altura', 'Diseño y desarrollo de productos y ecosistemas digitales',
                'La calidad de los activos digitales influye tanto en las decisiones de compra de tus clientes como en la eficiencia de la operación. Mejorar su funcionalidad y su experiencia aumenta las ventas y optimiza los procesos internos.',
                ['Diseñamos, validamos y desarrollamos productos digitales centrados en el cliente o en la eficiencia operativa', 'Creamos nuevos canales y herramientas para fortalecer las relaciones comerciales', 'Desarrollamos software que se integra con los sistemas centrales del negocio'],
                'APYMSA · plataforma B2B de autopartes')
         + reto('03', 'operacion', 'Tu operación depende de tareas manuales', 'Digitalización de la operación y automatización',
                'Optimizamos procesos con tecnología: sistemas ágiles, seguros y escalables que potencian cada etapa de la cadena de valor, desde los procesos industriales hasta la relación con los clientes.',
                ['Análisis de procesos y oportunidades de automatización', 'Automatización con inteligencia artificial: agentes y asistentes conectados a tus sistemas y datos', 'Desarrollo de sistemas y aplicaciones a la medida', 'Herramientas e integraciones con los sistemas existentes'],
                'Fanosa · automatización comercial')
         + reto('04', 'estrategia', 'Tu estrategia no parte de lo que necesita tu cliente', 'Estrategia con enfoque centrado en el usuario',
                'Se habla mucho de orientar los esfuerzos hacia el usuario, pero en la práctica los análisis suelen quedarse en la superficie. Las organizaciones que alinean sus capacidades con las necesidades reales de sus usuarios mantienen su relevancia y su competitividad.',
                ['Análisis de la organización, sus líneas de ingreso y sus retos de crecimiento', 'Investigación cualitativa y cuantitativa con tus segmentos de usuarios', 'Portafolio de iniciativas evaluadas por viabilidad, deseabilidad y factibilidad tecnológica'],
                'BayWa r.e. · recorrido de instaladores')
         + reto('05', 'equipos', 'Tus iniciativas de innovación no logran avanzar', 'Equipos de innovación y diseño para empresas',
                'Muchas organizaciones tardan en llevar productos al mercado porque el proceso carece de consistencia o el equipo a cargo no cuenta con las herramientas, el liderazgo o las competencias técnicas para resolver retos complejos.',
                ['Construimos y fortalecemos equipos multidisciplinarios dentro de tu empresa', 'Los habilitamos para diseñar y transformar productos, servicios y flujos de valor', 'Capacitación en metodologías de diseño centradas en el usuario, con APTO Education'],
                'Coppel Club de Protección · producto de seguros'))
a_ = s.index('<section class="section section--navy" id="productos">'); z = s.index('</section>', a_); sec = s[a_:z]
i = sec.index('<div class="retos">\n') + len('<div class="retos">\n'); j = sec.rindex('</article>\n') + len('</article>\n')
head = sec[:i]
head = re.sub(r'<p class="eyebrow">[^<]*</p>', '<p class="eyebrow">Qué transformamos</p>', head, count=1)
head = re.sub(r'<h2>[^<]*</h2>', '<h2>Cinco frentes de la transformación digital.</h2>', head, count=1)
head = re.sub(r'<p class="lead">[^<]*</p>', '<p class="lead">La transformación digital no es un proyecto de tecnología aislado: conecta el servicio, los productos digitales, la operación, la estrategia y los equipos. Podemos empezar por un frente y sumar los demás según el alcance.</p>', head, count=1)
s = s[:a_] + head + frentes + sec[j:] + s[z:]
s = s.replace('>Los seis retos<', '>Cinco frentes<')

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
