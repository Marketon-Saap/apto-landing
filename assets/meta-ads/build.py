#!/usr/bin/env python3
"""
APTO Meta Ads S1 · Batch Generator
5 conceptos × 3 aspect ratios = 15 renders

Alineado a:
- Andromeda 2026 · 5 entities distintos (diversidad REAL no cosmética)
- Marketon Ads Design · max 3 colores · monumental+clinica typography · glance+linger
- Paleta APTO · navy #0A1A3B · electric blue #005DE0 · off-white #F5F0E8

Formatos:
- 9:16 (Reels/Stories) 1080×1920 · safe zone y=280 a y=1200
- 4:5 (Feed) 1080×1350
- 1:1 (Feed/Carousel) 1080×1080
"""
import subprocess
from pathlib import Path

OUT_DIR = Path(__file__).parent
RENDERS = OUT_DIR / 'renders'
HTML_DIR = OUT_DIR / 'html'
CONCEPTS = OUT_DIR / 'concepts'
RENDERS.mkdir(exist_ok=True)
HTML_DIR.mkdir(exist_ok=True)

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

# Paleta APTO oficial
NAVY = '#0A1A3B'
NAVY_DEEP = '#050E24'
BLUE = '#005DE0'
BLUE_LIGHT = '#3A86FF'
OFFWHITE = '#F5F0E8'
GRAY_MUTED = '#4A5568'
ACCENT_AMBER = '#F59E0B'

FORMATS = [
    {'key': '9x16', 'w': 1080, 'h': 1920},
    {'key': '4x5',  'w': 1080, 'h': 1350},
    {'key': '1x1',  'w': 1080, 'h': 1080},
]

BASE_CSS = f"""
  @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:100%; height:100%; overflow:hidden; -webkit-font-smoothing:antialiased; }}
  body {{ font-family:'Inter', -apple-system, sans-serif; color:{OFFWHITE}; }}
  .canvas {{
    width:100%; height:100vh;
    display:flex; flex-direction:column;
    position:relative; overflow:hidden;
  }}
  .heading {{ font-family:'Space Grotesk', sans-serif; font-weight:600; line-height:0.92; letter-spacing:-0.02em; }}
  .body-text {{ font-family:'Inter', sans-serif; font-weight:400; line-height:1.4; }}
  .eyebrow {{
    font-family:'Space Grotesk', sans-serif; font-weight:600;
    font-size:14px; text-transform:uppercase; letter-spacing:0.16em;
    color:{BLUE_LIGHT};
  }}
  .cta {{
    display:inline-flex; align-items:center; gap:8px;
    background:{BLUE}; color:{OFFWHITE};
    padding:16px 28px; border-radius:100px;
    font-family:'Space Grotesk', sans-serif; font-weight:600;
    font-size:15px; letter-spacing:0.02em;
  }}
  .cta .arrow {{ font-size:18px; line-height:1; }}
  .logo-footer {{
    font-family:'Space Grotesk', sans-serif; font-weight:700;
    font-size:16px; letter-spacing:0.24em; color:{OFFWHITE};
  }}
  .logo-footer .dot {{ color:{BLUE_LIGHT}; }}
  .divider {{ height:1px; background:rgba(255,255,255,.12); }}
"""

# ============================================================
# CONCEPTO 1 · PATTERN INTERRUPT · "Más software ≠ solución"
# Hook type: SHOCK STAT · Andromeda entity: text-driven dark theme
# ============================================================
def concept_1_pattern_interrupt(w, h, is_vertical, is_square):
    hero_size = 'clamp(120px, 18vw, 200px)' if is_vertical else ('clamp(140px, 16vw, 180px)' if is_square else 'clamp(100px, 12vw, 150px)')
    return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
    .canvas {{ background:{NAVY_DEEP}; padding:{80 if is_vertical else 60}px; justify-content:space-between; }}
    .grain {{
      position:absolute; inset:0; opacity:.04; pointer-events:none;
      background-image:radial-gradient(circle at 20% 30%, {BLUE_LIGHT} 1px, transparent 1px);
      background-size:20px 20px;
    }}
    .header {{ z-index:2; }}
    .hero {{
      z-index:2; text-align:left;
      font-size:{hero_size}; line-height:0.88; letter-spacing:-0.035em;
    }}
    .hero .neq {{ color:{ACCENT_AMBER}; font-weight:700; }}
    .sub {{
      z-index:2; max-width:{700 if is_vertical else 800}px;
      font-size:{'22px' if is_vertical else '20px'};
      color:rgba(245,240,232,.72); font-weight:400; line-height:1.5;
    }}
    .footer {{ z-index:2; display:flex; justify-content:space-between; align-items:center; }}
  </style></head><body>
    <div class="canvas">
      <div class="grain"></div>
      <div class="header">
        <div class="eyebrow">Consultoría de innovación</div>
      </div>
      <h1 class="heading hero">Más software<br><span class="neq">≠</span> solución.</h1>
      <p class="body-text sub">Estrategia, diseño y tecnología resueltas por el mismo equipo. Nos quedamos hasta que el sistema opera — no entregamos un deck y desaparecemos.</p>
      <div class="footer">
        <div class="cta">Agenda tu sesión <span class="arrow">→</span></div>
        <div class="logo-footer">APTO<span class="dot">.</span></div>
      </div>
    </div>
  </body></html>"""

# ============================================================
# CONCEPTO 2 · STAT HERO · 10 años · 6 disciplinas · 1 equipo
# Hook type: AUTHORITY BY NUMBERS · Andromeda entity: number-driven
# ============================================================
def concept_2_stat_hero(w, h, is_vertical, is_square):
    stat_size = 'clamp(180px, 26vw, 320px)' if is_vertical else ('clamp(160px, 22vw, 240px)' if is_square else 'clamp(180px, 22vw, 260px)')
    # Column stack en todos los formatos · 3 números apilados vertical se leen mejor que row squeeze
    layout_dir = 'column'
    return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
    .canvas {{
      background:linear-gradient(135deg, {NAVY} 0%, {NAVY_DEEP} 100%);
      padding:{80 if is_vertical else 60}px; justify-content:space-between;
    }}
    .grid-bg {{
      position:absolute; inset:0; opacity:.06; pointer-events:none;
      background-image:linear-gradient({OFFWHITE} 1px, transparent 1px), linear-gradient(90deg, {OFFWHITE} 1px, transparent 1px);
      background-size:80px 80px;
    }}
    .header {{ z-index:2; }}
    .stats {{
      z-index:2; display:flex; flex-direction:{layout_dir};
      gap:{40 if is_vertical else 30}px; flex:1; align-items:flex-start; justify-content:center;
      {'padding: 40px 0;' if is_vertical else ''}
    }}
    .stat {{ display:flex; flex-direction:column; gap:8px; align-items:flex-start; flex:1; }}
    .stat-number {{
      font-family:'Space Grotesk', sans-serif; font-weight:700;
      font-size:{stat_size}; line-height:0.85; letter-spacing:-0.05em;
      color:{OFFWHITE};
    }}
    .stat-number .accent {{ color:{BLUE_LIGHT}; }}
    .stat-label {{
      font-size:{'18px' if is_vertical else '16px'};
      color:rgba(245,240,232,.72); font-weight:500; line-height:1.35;
      max-width:{280 if is_vertical else 220}px;
    }}
    .footer {{ z-index:2; display:flex; justify-content:space-between; align-items:center; }}
  </style></head><body>
    <div class="canvas">
      <div class="grid-bg"></div>
      <div class="header">
        <div class="eyebrow">10 años acompañando líderes de innovación</div>
      </div>
      <div class="stats">
        <div class="stat">
          <div class="stat-number">10<span class="accent">.</span></div>
          <div class="stat-label">años acompañando líderes de innovación en México</div>
        </div>
        <div class="stat">
          <div class="stat-number">6<span class="accent">.</span></div>
          <div class="stat-label">disciplinas bajo el mismo techo</div>
        </div>
        <div class="stat">
          <div class="stat-number">1<span class="accent">.</span></div>
          <div class="stat-label">equipo diseña + construye · no fábrica externa</div>
        </div>
      </div>
      <div class="footer">
        <div class="cta">Agenda tu sesión <span class="arrow">→</span></div>
        <div class="logo-footer">APTO<span class="dot">.</span></div>
      </div>
    </div>
  </body></html>"""

# ============================================================
# CONCEPTO 3 · US VS THEM · Big-Four vs APTO
# Hook type: COMPARISON · Andromeda entity: split-screen contrast
# ============================================================
def concept_3_us_vs_them(w, h, is_vertical, is_square):
    header_size = 'clamp(38px, 5vw, 60px)' if is_vertical else ('clamp(40px, 5vw, 56px)' if is_square else 'clamp(28px, 3.5vw, 42px)')
    layout_dir = 'column' if is_vertical else 'row'
    return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
    .canvas {{ background:{NAVY_DEEP}; padding:{60 if is_vertical else 50}px; gap:{30 if is_vertical else 24}px; }}
    .header {{ z-index:2; text-align:{'center' if is_vertical else 'left'}; }}
    .header h1 {{
      font-size:{header_size}; letter-spacing:-0.025em; line-height:1.05;
      max-width:{800 if not is_vertical else 900}px;
    }}
    .header h1 .accent {{ color:{BLUE_LIGHT}; }}
    .compare {{
      z-index:2; display:flex; flex-direction:{layout_dir};
      gap:{20 if is_vertical else 24}px; flex:1;
    }}
    .side {{
      flex:1; border-radius:24px; padding:{40 if is_vertical else 44}px;
      display:flex; flex-direction:column; gap:20px;
    }}
    .side-them {{ background:rgba(74,85,104,.15); border:1px solid rgba(74,85,104,.3); }}
    .side-us {{ background:{BLUE}; }}
    .side-label {{
      font-family:'Space Grotesk', sans-serif; font-weight:600;
      font-size:12px; letter-spacing:0.18em; text-transform:uppercase;
    }}
    .side-them .side-label {{ color:{GRAY_MUTED}; }}
    .side-us .side-label {{ color:rgba(245,240,232,.7); }}
    .side-title {{
      font-family:'Space Grotesk', sans-serif; font-weight:700;
      font-size:{'32px' if is_vertical else '28px'}; letter-spacing:-0.02em; line-height:1.1;
    }}
    .side-them .side-title {{ color:rgba(245,240,232,.55); }}
    .side-us .side-title {{ color:{OFFWHITE}; }}
    .side-list {{ list-style:none; display:flex; flex-direction:column; gap:12px; margin-top:8px; }}
    .side-list li {{
      font-size:{'17px' if is_vertical else '15px'}; line-height:1.4;
      padding-left:24px; position:relative;
    }}
    .side-them .side-list li {{ color:rgba(245,240,232,.5); }}
    .side-them .side-list li::before {{ content:'✕'; position:absolute; left:0; color:rgba(245,240,232,.4); }}
    .side-us .side-list li {{ color:{OFFWHITE}; }}
    .side-us .side-list li::before {{ content:'→'; position:absolute; left:0; color:{OFFWHITE}; font-weight:700; }}
    .footer {{ z-index:2; display:flex; justify-content:space-between; align-items:center; margin-top:auto; }}
  </style></head><body>
    <div class="canvas">
      <div class="header">
        <div class="eyebrow" style="margin-bottom:14px">El nuevo estándar</div>
        <h1 class="heading">Rigor consultora estratégica <span class="accent">sin el sobreprecio.</span></h1>
      </div>
      <div class="compare">
        <div class="side side-them">
          <div class="side-label">Consultora tradicional</div>
          <div class="side-title">120 slides. 3 años. Nunca aterriza.</div>
          <ul class="side-list">
            <li>8 semanas solo de análisis</li>
            <li>Tarifas Big-Four</li>
            <li>Ejecución tercerizada</li>
          </ul>
        </div>
        <div class="side side-us">
          <div class="side-label">APTO</div>
          <div class="side-title">Sistema construido y operando.</div>
          <ul class="side-list">
            <li>Mismo equipo diseña y construye</li>
            <li>Precio accesible medianas + corporativos</li>
            <li>Nos quedamos hasta que opera</li>
          </ul>
        </div>
      </div>
      <div class="footer">
        <div class="cta" style="background:{OFFWHITE};color:{NAVY}">Agenda tu sesión <span class="arrow">→</span></div>
        <div class="logo-footer">APTO<span class="dot">.</span></div>
      </div>
    </div>
  </body></html>"""

# ============================================================
# CONCEPTO 4 · CASO COPPEL · Systems Dynamics · photo overlay
# Hook type: PROOF BY CASE · Andromeda entity: image + case study
# ============================================================
def concept_4_coppel_case(w, h, is_vertical, is_square):
    title_size = 'clamp(42px, 6vw, 68px)' if is_vertical else ('clamp(38px, 5vw, 58px)' if is_square else 'clamp(30px, 4vw, 46px)')
    # Gradient inverso: foto visible arriba 55%, oscuro abajo donde va el texto
    return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
    .canvas {{
      background:{NAVY_DEEP};
      background-image:linear-gradient(180deg, rgba(5,14,36,.05) 0%, rgba(5,14,36,.15) 40%, rgba(5,14,36,.85) 65%, rgba(5,14,36,.98) 82%, rgba(5,14,36,1) 100%),
                       url('../concepts/coppel-diorama.jpg');
      background-size:cover; background-position:center 45%;
      padding:{80 if is_vertical else 60}px; justify-content:flex-end;
    }}
    .top {{ z-index:2; {'display:none;' if is_vertical else ''} }}
    .content {{
      z-index:2; display:flex; flex-direction:column; gap:{28 if is_vertical else 22}px;
      max-width:{900 if is_vertical else 900}px;
    }}
    .caso-cliente {{
      font-family:'Space Grotesk', sans-serif; font-weight:600;
      font-size:{'16px' if is_vertical else '14px'}; letter-spacing:0.15em;
      text-transform:uppercase; color:{BLUE_LIGHT};
    }}
    .caso-title {{
      font-size:{title_size}; letter-spacing:-0.028em; line-height:1.04;
    }}
    .stat-callout {{
      display:inline-flex; align-items:center; gap:16px;
      background:{BLUE}; color:{OFFWHITE};
      padding:{'18px 24px' if is_vertical else '16px 22px'};
      border-radius:16px; align-self:flex-start;
      font-family:'Space Grotesk', sans-serif; font-weight:600;
      font-size:{'20px' if is_vertical else '17px'};
    }}
    .stat-callout .num {{
      font-size:{'32px' if is_vertical else '28px'}; font-weight:700; line-height:1;
    }}
    .footer {{
      z-index:2; display:flex; justify-content:space-between; align-items:center;
      margin-top:{40 if is_vertical else 24}px;
    }}
  </style></head><body>
    <div class="canvas">
      <div class="top"><div class="eyebrow">Caso · Flagship</div></div>
      <div class="content">
        <div class="caso-cliente">Coppel · Systems Dynamics</div>
        <h1 class="heading caso-title">Un mapa no-lineal para un ecosistema de miles de puntos de contacto.</h1>
        <div class="stat-callout">
          <span class="num">+25%</span>
          <span>eficiencia en definición de nuevos servicios</span>
        </div>
      </div>
      <div class="footer">
        <div class="cta">Ver más casos <span class="arrow">→</span></div>
        <div class="logo-footer">APTO<span class="dot">.</span></div>
      </div>
    </div>
  </body></html>"""

# ============================================================
# CONCEPTO 5 · TESTIMONIO ÁLVARO · portrait cinemático
# Hook type: HUMAN TRUST · Andromeda entity: face + text overlay
# ============================================================
def concept_5_alvaro_portrait(w, h, is_vertical, is_square):
    title_size = 'clamp(38px, 5.5vw, 60px)' if is_vertical else ('clamp(36px, 5vw, 52px)' if is_square else 'clamp(28px, 4vw, 42px)')
    bg_pos = 'center 25%' if is_vertical else 'center center'
    return f"""<!DOCTYPE html><html><head><style>{BASE_CSS}
    .canvas {{
      background:{NAVY_DEEP};
      background-image:linear-gradient(180deg, rgba(5,14,36,.15) 0%, rgba(5,14,36,.55) 55%, rgba(5,14,36,.95) 90%),
                       url('../concepts/alvaro-portrait.jpg');
      background-size:cover; background-position:{bg_pos};
      padding:{80 if is_vertical else 60}px; justify-content:{'flex-end' if is_vertical else 'space-between'};
    }}
    .top-badge {{
      z-index:2; align-self:flex-start;
      display:inline-flex; align-items:center; gap:10px;
      background:rgba(0,93,224,.9); color:{OFFWHITE};
      padding:10px 18px; border-radius:100px;
      font-family:'Space Grotesk', sans-serif; font-weight:600;
      font-size:13px; letter-spacing:0.08em; text-transform:uppercase;
      {'display:none;' if is_vertical else ''}
    }}
    .content {{
      z-index:2; display:flex; flex-direction:column; gap:{20 if is_vertical else 18}px;
      max-width:{800 if is_vertical else 800}px;
    }}
    .name-line {{
      font-family:'Space Grotesk', sans-serif; font-weight:600;
      font-size:{'16px' if is_vertical else '14px'}; letter-spacing:0.15em;
      text-transform:uppercase; color:{BLUE_LIGHT};
    }}
    .quote {{
      font-size:{title_size}; letter-spacing:-0.025em; line-height:1.08;
    }}
    .sub {{
      font-size:{'18px' if is_vertical else '16px'};
      color:rgba(245,240,232,.7); line-height:1.4;
      max-width:{600 if is_vertical else 700}px;
    }}
    .footer {{
      z-index:2; display:flex; justify-content:space-between; align-items:center;
      margin-top:{40 if is_vertical else 24}px;
    }}
  </style></head><body>
    <div class="canvas">
      <div class="top-badge">▶ 1 min · Manifesto APTO</div>
      <div class="content">
        <div class="name-line">Álvaro Plasencia · Socio senior</div>
        <h1 class="heading quote">Antes de agendar, conoce quién te va a atender.</h1>
        <p class="body-text sub">Uno de los socios toma la primera llamada. Sin filtros de agencia, sin BDRs, sin discovery calls con juniors.</p>
      </div>
      <div class="footer">
        <div class="cta">Agenda tu sesión <span class="arrow">→</span></div>
        <div class="logo-footer">APTO<span class="dot">.</span></div>
      </div>
    </div>
  </body></html>"""

CONCEPTS_LIST = [
    {'id': '1_pattern_interrupt', 'name': 'Pattern Interrupt · Más software ≠ solución', 'fn': concept_1_pattern_interrupt},
    {'id': '2_stat_hero',         'name': 'Stat Hero · 10 · 6 · 1',                     'fn': concept_2_stat_hero},
    {'id': '3_us_vs_them',        'name': 'Us vs Them · Big-Four vs APTO',              'fn': concept_3_us_vs_them},
    {'id': '4_coppel_case',       'name': 'Caso Coppel · Systems Dynamics',             'fn': concept_4_coppel_case},
    {'id': '5_alvaro_portrait',   'name': 'Testimonio Álvaro Plasencia',                'fn': concept_5_alvaro_portrait},
]

def build_all():
    total = len(CONCEPTS_LIST) * len(FORMATS)
    idx = 0
    for c in CONCEPTS_LIST:
        for fmt in FORMATS:
            idx += 1
            w, h = fmt['w'], fmt['h']
            is_vertical = (h > w * 1.5)
            is_square = (w == h)
            fname = f"{c['id']}_{fmt['key']}"
            html_path = HTML_DIR / f"{fname}.html"
            png_path = RENDERS / f"{fname}.png"
            html_path.write_text(c['fn'](w, h, is_vertical, is_square))
            subprocess.run([
                CHROME, '--headless=new', '--disable-gpu',
                f'--window-size={w},{h}', '--hide-scrollbars',
                '--virtual-time-budget=8000',
                '--run-all-compositor-stages-before-draw',
                f'--screenshot={png_path}',
                f'file://{html_path.resolve()}'
            ], capture_output=True, timeout=30)
            size = png_path.stat().st_size if png_path.exists() else 0
            print(f'  [{idx:2}/{total}] {fname:35} · {size//1024}KB')
    print(f'\nDONE · {total} renders en {RENDERS}')

if __name__ == '__main__':
    build_all()
