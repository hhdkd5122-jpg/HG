"""Office-style (Excel / SmartArt) SVG charts for the AAU bergamot poster."""
import math

F = 'font-family="Carlito, Calibri, Arial, sans-serif"'
BLUE, ORANGE, GRAY, GOLD, GREEN = '#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#70AD47'
DGREEN = '#1d3a1a'
AX, GRID, TXT = '#595959', '#D9D9D9', '#262626'
ARROW = ('<defs><marker id="{id}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" '
         'markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="#404040"/></marker></defs>')


def mechanism():
    W, H = 1040, 360
    o = [f'<svg viewBox="0 0 {W} {H}" width="100%" style="display:block" {F}>', ARROW.format(id='ma')]
    labels = [['Acetyl-CoA'], ['HMG-CoA'], ['Mevalonate'], ['Liver', 'cholesterol ↓'],
              ['LDL', 'receptors ↑'], ['Blood', 'LDL-C ↓']]
    bw, bh, gap = 146, 78, 32
    x0 = (W - (6 * bw + 5 * gap)) / 2
    y = 20
    for i, lines in enumerate(labels):
        x = x0 + i * (bw + gap)
        fill = GREEN if i >= 3 else BLUE
        o.append(f'<rect x="{x:.0f}" y="{y}" width="{bw}" height="{bh}" rx="6" fill="{fill}"/>')
        for k, l in enumerate(lines):
            yy = y + bh / 2 + 8 + (k - (len(lines) - 1) / 2) * 25
            o.append(f'<text x="{x + bw / 2:.0f}" y="{yy:.0f}" text-anchor="middle" font-size="23" '
                     f'font-weight="700" fill="#fff">{l}</text>')
        if i < 5:
            ax = x + bw + 4
            o.append(f'<path d="M{ax:.0f} {y + bh / 2 - 9} h11 v-8 l12 17 l-12 17 v-8 h-11z" fill="{GRAY}"/>')
    ex = x0 + 2 * bw + 1.5 * gap
    o.append(f'<text x="{ex:.0f}" y="{y + bh + 32}" text-anchor="middle" font-size="20" fill="{AX}" '
             f'font-style="italic">HMG-CoA reductase</text>')
    o.append(f'<path d="M{ex - 70:.0f} 196 L{ex - 12:.0f} {y + bh + 44}" stroke="{BLUE}" stroke-width="2.5" marker-end="url(#ma)"/>')
    o.append(f'<path d="M{ex + 80:.0f} 196 L{ex + 14:.0f} {y + bh + 44}" stroke="{ORANGE}" stroke-width="2.5" '
             f'stroke-dasharray="7 5" marker-end="url(#ma)"/>')
    o.append(f'<rect x="{ex - 270:.0f}" y="196" width="220" height="66" fill="#fff" stroke="{BLUE}" stroke-width="2"/>'
             f'<text x="{ex - 160:.0f}" y="223" text-anchor="middle" font-size="22" font-weight="700" fill="{BLUE}">Statins</text>'
             f'<text x="{ex - 160:.0f}" y="249" text-anchor="middle" font-size="19" fill="{AX}">inhibit (proven)</text>')
    o.append(f'<rect x="{ex + 40:.0f}" y="196" width="320" height="66" fill="#fff" stroke="{ORANGE}" stroke-width="2" '
             f'stroke-dasharray="7 5"/><text x="{ex + 200:.0f}" y="223" text-anchor="middle" font-size="22" '
             f'font-weight="700" fill="{ORANGE}">Bergamot flavanones</text><text x="{ex + 200:.0f}" y="249" '
             f'text-anchor="middle" font-size="19" fill="{AX}">brutieridin, melitidin (proposed)</text>')
    o.append(f'<rect x="10" y="286" width="1020" height="32" fill="#E7E6E6"/><text x="22" y="309" font-size="20" '
             f'font-weight="700" fill="{TXT}">Other proposed effects</text>')
    o.append(f'<rect x="10" y="318" width="510" height="38" fill="#fff" stroke="#BFBFBF"/><text x="22" y="344" '
             f'font-size="19" fill="{TXT}"><tspan font-weight="700">Antioxidant:</tspan> ↓ LOX-1 receptor (Gliozzi 2013)</text>')
    o.append(f'<rect x="520" y="318" width="510" height="38" fill="#fff" stroke="#BFBFBF"/><text x="532" y="344" '
             f'font-size="19" fill="{TXT}"><tspan font-weight="700">Liver fat:</tspan> ↑ lipophagy, rat model (Parafati 2015)</text>')
    o.append('</svg>')
    return '\n'.join(o)


def linechart():
    W, H = 1500, 560
    L, R, T, B = 120, 40, 64, 150
    pw, ph = W - L - R, H - T - B
    X = lambda a: L + a / 60 * pw
    Y = lambda v: T + ph - v / 200 * ph
    o = [f'<svg viewBox="0 0 {W} {H}" width="100%" style="display:block" {F}>', ARROW.format(id='la')]
    o.append(f'<text x="{W / 2}" y="36" text-anchor="middle" font-size="30" fill="{AX}">'
             f'Cumulative LDL-C exposure by age (illustrative model)</text>')
    o.append(f'<rect x="{X(15):.0f}" y="{T}" width="{X(19) - X(15):.0f}" height="{ph}" fill="#FFF2CC"/>')
    o.append(f'<text x="{(X(15) + X(19)) / 2:.0f}" y="{T + 26}" text-anchor="middle" font-size="19" fill="#7F6000">Young</text>'
             f'<text x="{(X(15) + X(19)) / 2:.0f}" y="{T + 48}" text-anchor="middle" font-size="19" fill="#7F6000">patients</text>')
    for v in range(0, 201, 40):
        o.append(f'<path d="M{L} {Y(v):.1f} H{L + pw}" stroke="{GRID}" stroke-width="1.5"/>'
                 f'<text x="{L - 12}" y="{Y(v) + 7:.1f}" text-anchor="end" font-size="21" fill="{AX}">{v}</text>')
    for a in range(0, 61, 10):
        o.append(f'<text x="{X(a):.1f}" y="{T + ph + 32}" text-anchor="middle" font-size="21" fill="{AX}">{a}</text>')
    o.append(f'<path d="M{L} {T + ph} H{L + pw}" stroke="#BFBFBF" stroke-width="2"/>')
    o.append(f'<text x="{L + pw / 2}" y="{T + ph + 66}" text-anchor="middle" font-size="23" font-weight="700" fill="{AX}">Age (years)</text>')
    o.append(f'<text transform="translate(36 {T + ph / 2}) rotate(-90)" text-anchor="middle" font-size="23" '
             f'font-weight="700" fill="{AX}">LDL-C × years (mmol/L)</text>')

    def pl(pts, c, w=4.5, dash=''):
        d = 'M' + ' L'.join(f'{X(a):.1f} {Y(v):.1f}' for a, v in pts)
        return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" {dash}/>'
    o.append(pl([(0, 160), (60, 160)], '#C00000', 3, 'stroke-dasharray="10 6"'))
    o.append(pl([(0, 0), (60, 180)], GRAY))
    o.append(pl([(0, 0), (50, 200)], ORANGE))
    o.append(pl([(0, 0), (16, 64), (58.75, 200)], BLUE))
    for a, c in [(40, ORANGE), (46, BLUE)]:
        o.append(f'<circle cx="{X(a):.1f}" cy="{Y(160):.1f}" r="8" fill="{c}" stroke="#fff" stroke-width="2"/>')
    o.append(f'<path d="M{X(40) + 10:.1f} {Y(160) + 26:.1f} H{X(46) - 12:.1f}" stroke="#404040" stroke-width="2.5" marker-end="url(#la)"/>')
    o.append(f'<rect x="{X(40) - 8:.1f}" y="{Y(160) + 40:.1f}" width="176" height="42" fill="#fff" stroke="#404040" stroke-width="1.5"/>'
             f'<text x="{X(40) + 80:.1f}" y="{Y(160) + 69:.1f}" text-anchor="middle" font-size="23" font-weight="700" fill="{TXT}">≈6 years later</text>')
    o.append(f'<text x="{X(0.6):.1f}" y="{Y(160) - 10:.1f}" font-size="20" fill="#C00000">Event threshold (~160)</text>')
    items = [(ORANGE, 'High risk, untreated (LDL-C 4.0)', ''), (BLUE, 'Bergamot started early (−0.8)', ''),
             (GRAY, 'Average (LDL-C 3.0)', ''), ('#C00000', 'Event threshold', 'stroke-dasharray="10 6"')]
    lx, ly = 170, H - 26
    for c, t, d in items:
        o.append(f'<path d="M{lx} {ly - 7} h40" stroke="{c}" stroke-width="4.5" {d}/>'
                 f'<text x="{lx + 50}" y="{ly}" font-size="21" fill="{AX}">{t}</text>')
        lx += 50 + len(t) * 10.6 + 44
    o.append('</svg>')
    return '\n'.join(o)


def donut():
    S = 360
    cx = cy = S / 2
    R, r = 165, 86
    vals = [(3, BLUE, '43%'), (2, ORANGE, '29%'), (1, GRAY, '14%'), (1, GOLD, '14%')]
    tot = 7
    a0 = -90
    o = [f'<svg viewBox="0 0 {S} {S}" width="{S}" height="{S}" {F}>']
    for v, c, lab in vals:
        a1 = a0 + v / tot * 360

        def p(a, rr):
            return cx + rr * math.cos(math.radians(a)), cy + rr * math.sin(math.radians(a))
        large = 1 if a1 - a0 > 180 else 0
        x1, y1 = p(a0, R); x2, y2 = p(a1, R); x3, y3 = p(a1, r); x4, y4 = p(a0, r)
        o.append(f'<path d="M{x1:.1f} {y1:.1f} A{R} {R} 0 {large} 1 {x2:.1f} {y2:.1f} L{x3:.1f} {y3:.1f} '
                 f'A{r} {r} 0 {large} 0 {x4:.1f} {y4:.1f} Z" fill="{c}" stroke="#fff" stroke-width="3"/>')
        mx, my = p((a0 + a1) / 2, (R + r) / 2)
        o.append(f'<text x="{mx:.1f}" y="{my + 9:.1f}" text-anchor="middle" font-size="27" font-weight="700" fill="#fff">{lab}</text>')
        a0 = a1
    o.append(f'<text x="{cx}" y="{cy + 8}" text-anchor="middle" font-size="54" font-weight="700" fill="#C00000">0</text>'
             f'<text x="{cx}" y="{cy + 34}" text-anchor="middle" font-size="19" fill="{AX}">in young</text>'
             f'<text x="{cx}" y="{cy + 54}" text-anchor="middle" font-size="19" fill="{AX}">patients</text>')
    o.append('</svg>')
    return '\n'.join(o)


def ldlbars():
    W, H = 640, 330
    L, T, B = 70, 50, 56
    pw, ph = W - L - 16, H - T - B
    Y = lambda v: T + ph - v / 60 * ph
    o = [f'<svg viewBox="0 0 {W} {H}" width="100%" style="display:block" {F}>']
    o.append(f'<text x="{W / 2}" y="28" text-anchor="middle" font-size="24" fill="{AX}">LDL-C reduction in meta-analyses (mg/dL)</text>')
    for v in range(0, 61, 20):
        o.append(f'<path d="M{L} {Y(v):.1f} H{L + pw}" stroke="{GRID}" stroke-width="1.5"/>'
                 f'<text x="{L - 10}" y="{Y(v) + 7:.1f}" text-anchor="end" font-size="20" fill="{AX}">{v}</text>')
    data = [('Sadeghi 2022', '14 trials', 55), ('Chambari 2026', '9 RCTs', 40), ('Osadnik 2022', 'network MA', 47)]
    bw = 110
    for i, (n, sub, v) in enumerate(data):
        c = L + pw / 6 + i * pw / 3
        o.append(f'<rect x="{c - bw / 2:.1f}" y="{Y(v):.1f}" width="{bw}" height="{Y(0) - Y(v):.1f}" fill="{BLUE}"/>')
        o.append(f'<text x="{c:.1f}" y="{Y(v) - 8:.1f}" text-anchor="middle" font-size="23" font-weight="700" fill="{TXT}">−{v}</text>')
        o.append(f'<text x="{c:.1f}" y="{T + ph + 26}" text-anchor="middle" font-size="20" fill="{TXT}">{n}</text>'
                 f'<text x="{c:.1f}" y="{T + ph + 48}" text-anchor="middle" font-size="17" fill="{AX}">{sub}</text>')
    o.append(f'<path d="M{L} {Y(0):.1f} H{L + pw}" stroke="#BFBFBF" stroke-width="2"/>')
    o.append('</svg>')
    return '\n'.join(o)


def liverbars():
    W, H = 640, 330
    L, T, R = 130, 50, 30
    pw = W - L - R
    X = lambda v: L + v / 60 * pw
    o = [f'<svg viewBox="0 0 {W} {H}" width="100%" style="display:block" {F}>']
    o.append(f'<text x="{W / 2}" y="28" text-anchor="middle" font-size="24" fill="{AX}">Liver fat reduction, 12 weeks (Ferro 2020)</text>')
    for v in range(0, 61, 20):
        o.append(f'<path d="M{X(v):.1f} {T + 10} V{T + 200}" stroke="{GRID}" stroke-width="1.5"/>'
                 f'<text x="{X(v):.1f}" y="{T + 226}" text-anchor="middle" font-size="20" fill="{AX}">{v}</text>')
    for i, (n, v, c) in enumerate([('Bergamot', 48, ORANGE), ('Placebo', 27, GRAY)]):
        y = T + 36 + i * 86
        o.append(f'<text x="{L - 12}" y="{y + 36}" text-anchor="end" font-size="22" fill="{TXT}">{n}</text>'
                 f'<rect x="{L}" y="{y}" width="{X(v) - L:.1f}" height="54" fill="{c}"/>'
                 f'<text x="{X(v) + 8:.1f}" y="{y + 36}" font-size="23" font-weight="700" fill="{TXT}">−{v}</text>')
    o.append(f'<path d="M{L} {T + 10} V{T + 200}" stroke="#BFBFBF" stroke-width="2"/>')
    o.append(f'<text x="{L + pw / 2}" y="{H - 14}" text-anchor="middle" font-size="20" fill="{AX}">CAP score reduction (dB/m), n = 102</text>')
    o.append('</svg>')
    return '\n'.join(o)


def process():
    steps = [('1', 'Recruit', 'Young patients with high cholesterol'),
             ('2', 'Screen', 'Lipids, Lp(a), genetic score, metabolic signs'),
             ('3', 'Sort', 'Monogenic FH → statin care; others enrolled'),
             ('4', 'Randomise', 'Bergamot vs placebo, with lifestyle advice'),
             ('5', 'Follow up', '12 months; adherence, safety, growth'),
             ('6', 'Measure', 'LDL-C, apoB, glucose, BP, liver fat'),
             ('7', 'Long term', 'Time until statin is needed')]
    W, H = 2150, 190
    bw, gap = 268, 46
    o = [f'<svg viewBox="0 0 {W} {H}" width="100%" style="display:block" {F}>']
    for i, (n, t, d) in enumerate(steps):
        x = i * (bw + gap)
        last = i == len(steps) - 1
        o.append(f'<rect x="{x}" y="0" width="{bw}" height="54" fill="{GOLD if last else DGREEN}"/>')
        o.append(f'<text x="{x + 16}" y="37" font-size="27" font-weight="700" fill="{DGREEN if last else "#fff"}">{n}. {t}</text>')
        o.append(f'<rect x="{x}" y="54" width="{bw}" height="128" fill="#fff" stroke="#BFBFBF" stroke-width="1.5"/>')
        words, lines, cur = d.split(' '), [], ''
        for w_ in words:
            if len(cur + ' ' + w_) > 22 and cur:
                lines.append(cur)
                cur = w_
            else:
                cur = (cur + ' ' + w_).strip()
        lines.append(cur)
        for k, l in enumerate(lines):
            o.append(f'<text x="{x + 16}" y="{90 + k * 28}" font-size="22" fill="{TXT}">{l}</text>')
        if not last:
            ax = x + bw + 8
            o.append(f'<path d="M{ax} 106 h12 v-12 l18 22 l-18 22 v-12 h-12z" fill="{GRAY}"/>')
    o.append('</svg>')
    return '\n'.join(o)
