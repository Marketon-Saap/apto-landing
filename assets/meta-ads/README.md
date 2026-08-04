# APTO Meta Ads · Sprint 1 (Ago 2026)

15 creativos (5 conceptos × 3 aspect ratios) para arranque campañas Meta APTO 2026H2.

## Alineación estratégica

**Andromeda 2026 · Diversidad REAL de entities**:
Cada concepto es un ENTITY distinto (no variación cosmética). Andromeda tiene 5 opciones de retrieval distintas.

| # | Concepto | Hook type | Entity signature |
|---|---|---|---|
| 1 | Pattern Interrupt · "Más software ≠ solución" | SHOCK STAT | text-only dark theme |
| 2 | Stat Hero · 10 · 6 · 1 | AUTHORITY BY NUMBERS | number-driven grid |
| 3 | Us vs Them · Big-Four vs APTO | COMPARISON | split-screen contrast |
| 4 | Caso Coppel · Systems Dynamics | PROOF BY CASE | photo diorama + case |
| 5 | Testimonio Álvaro Plasencia | HUMAN TRUST | portrait cinemático b&w |

**Marketon Ads Design · reglas duras respetadas**:
- Max 3 colores activos (navy #0A1A3B + blue #005DE0 + off-white #F5F0E8; amber #F59E0B solo en concepto 1)
- Monumental (Space Grotesk) + Clinica (Inter) dual typography
- Glance (2s) + Linger (5s+) dual mode: cada creativo comunica en 2s con hero + recompensa al 5s con sub/stat
- Diversidad REAL entre conceptos, no variaciones cosméticas
- Safe zones respetadas: top 14% (perfil), bottom 20-35% (Meta CTA)

## Formatos generados

- **9:16** Reels/Stories · 1080×1920
- **4:5** Feed FB+IG · 1080×1350 (highest CTR)
- **1:1** Feed/Carousel · 1080×1080

## Estructura

```
assets/meta-ads/
├── concepts/          # Assets fuente (fotos)
│   ├── coppel-diorama.jpg    (frame slide-2 apto.mx CDN)
│   └── alvaro-portrait.jpg   (YouTube maxres thumb 40gjKGn8qME)
├── html/              # HTML templates parametrizados (para iterar)
├── renders/           # PNG finales listos para subir a Meta
│   ├── 1_pattern_interrupt_[9x16|4x5|1x1].png
│   ├── 2_stat_hero_[9x16|4x5|1x1].png
│   ├── 3_us_vs_them_[9x16|4x5|1x1].png
│   ├── 4_coppel_case_[9x16|4x5|1x1].png
│   ├── 5_alvaro_portrait_[9x16|4x5|1x1].png
│   └── all-5-concepts-4x5-grid.jpg  (composite review)
├── build.py           # Batch generator (HTML → Chrome headless → PNG)
└── README.md          # este archivo
```

## Regenerar / iterar

```bash
cd assets/meta-ads
python3 build.py
```

Cambios de copy o layout: editar función `concept_N_...(w, h, is_vertical, is_square)` en `build.py`, re-run.

## Distribución en campañas Meta

**Campaña Core (ASC $350/día · 70%)**: los 15 renders como asset feed 5×5×5.

**Campaña Sandbox (CBO $100/día · 20%)**: rotación de 3-5 conceptos nuevos cada 14 días.

**Campaña Retargeting Warm (CBO $50/día · 10%)**: conceptos 4 (Coppel case) + 5 (Álvaro portrait) — señales de trust más fuertes para warm audience.

## Value tracking (Andromeda value-based bidding)

Cada Lead se envía a Meta CAPI con `value: 500 MXN`. Lifecycle escala:
- Lead $500 → MQL $2K → SQL $10K → Discovery $25K → Proposal $75K → Negotiation $100K → Purchase (deal amount real)

Meta aprende qué creativos traen leads que llegan más lejos en el funnel, no solo leads baratos.
