"""Botanical engraving-style line art (SVG) for the bergamot poster."""
import math
import random

_uid = [0]


def _id(p):
    _uid[0] += 1
    return f'{p}{_uid[0]}'


def leaf(x, y, length, angle, c, w=2.2, veins=7, width=0.36):
    """Leaf from base (x,y) pointing at angle (deg), with midrib and veins."""
    a = math.radians(angle)
    ux, uy = math.cos(a), math.sin(a)
    nx, ny = -uy, ux
    L, W = length, length * width
    tip = (x + ux * L, y + uy * L)
    c1 = (x + ux * L * .35 + nx * W, y + uy * L * .35 + ny * W)
    c2 = (x + ux * L * .35 - nx * W, y + uy * L * .35 - ny * W)
    c1b = (x + ux * L * .8 + nx * W * .55, y + uy * L * .8 + ny * W * .55)
    c2b = (x + ux * L * .8 - nx * W * .55, y + uy * L * .8 - ny * W * .55)
    o = [f'<path d="M{x:.1f} {y:.1f} C{c1[0]:.1f} {c1[1]:.1f} {c1b[0]:.1f} {c1b[1]:.1f} {tip[0]:.1f} {tip[1]:.1f} '
         f'C{c2b[0]:.1f} {c2b[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {x:.1f} {y:.1f}Z" fill="none" stroke="{c}" stroke-width="{w}"/>']
    o.append(f'<path d="M{x:.1f} {y:.1f} L{tip[0]:.1f} {tip[1]:.1f}" stroke="{c}" stroke-width="{w * .7:.1f}"/>')
    for i in range(1, veins + 1):
        t = i / (veins + 1)
        bx, by = x + ux * L * t, y + uy * L * t
        half = W * .78 * math.sin(math.pi * min(.95, t * 1.05)) * (1 - t * .35)
        for s in (1, -1):
            ex = bx + ux * L * .09 + nx * half * s
            ey = by + uy * L * .09 + ny * half * s
            o.append(f'<path d="M{bx:.1f} {by:.1f} Q{bx + nx * half * s * .5 + ux * 4:.1f} {by + ny * half * s * .5 + uy * 4:.1f} '
                     f'{ex:.1f} {ey:.1f}" fill="none" stroke="{c}" stroke-width="{w * .45:.2f}" opacity=".8"/>')
    return '\n'.join(o)


def fruit(cx, cy, r, c, w=2.4, seed=1, light=(-0.45, -0.5)):
    rnd = random.Random(seed)
    cid = _id('fc')
    o = [f'<clipPath id="{cid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>']
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c}" stroke-width="{w}"/>')
    # hatching: curved lines on the shadow side
    g = [f'<g clip-path="url(#{cid})" stroke="{c}" fill="none" stroke-width="{w * .4:.2f}" opacity=".75">']
    for i in range(-14, 15):
        off = i * r / 11
        # shadow crescent: lines offset toward lower-right, arc following circle
        sx, sy = cx + r * .2 + off * .7, cy - r
        g.append(f'<path d="M{sx:.1f} {sy:.1f} Q{sx + r * .55:.1f} {cy:.1f} {sx:.1f} {cy + r:.1f}"/>')
    g.append('</g>')
    # mask hatching to shadow side using a second clip (offset circle cut-out)
    mid = _id('fm')
    o.append(f'<mask id="{mid}"><rect x="{cx - r - 5}" y="{cy - r - 5}" width="{2 * r + 10}" height="{2 * r + 10}" fill="#fff"/>'
             f'<circle cx="{cx + light[0] * r * .55:.1f}" cy="{cy + light[1] * r * .55:.1f}" r="{r * .92:.1f}" fill="#000"/></mask>')
    o.append(f'<g mask="url(#{mid})">' + ''.join(g) + '</g>')
    # stipple (peel pores)
    dots = []
    for _ in range(int(r * 1.1)):
        a = rnd.uniform(0, 2 * math.pi)
        d = r * math.sqrt(rnd.uniform(0, .9))
        dots.append(f'<circle cx="{cx + d * math.cos(a):.1f}" cy="{cy + d * math.sin(a):.1f}" r="{rnd.uniform(.9, 1.8):.1f}"/>')
    o.append(f'<g fill="{c}" opacity=".55">' + ''.join(dots) + '</g>')
    # navel / stem
    o.append(f'<circle cx="{cx}" cy="{cy - r}" r="{r * .07:.1f}" fill="none" stroke="{c}" stroke-width="{w * .8:.1f}"/>')
    return '\n'.join(o)


def slice_(cx, cy, r, c, w=2.2, segs=10, rot=0):
    o = [f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c}" stroke-width="{w}"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r * .86:.1f}" fill="none" stroke="{c}" stroke-width="{w * .6:.1f}"/>']
    ri = r * .78
    for i in range(segs):
        a0 = math.radians(rot + i * 360 / segs + 3)
        a1 = math.radians(rot + (i + 1) * 360 / segs - 3)
        p0 = (cx + r * .1 * math.cos((a0 + a1) / 2), cy + r * .1 * math.sin((a0 + a1) / 2))
        e0 = (cx + ri * math.cos(a0), cy + ri * math.sin(a0))
        e1 = (cx + ri * math.cos(a1), cy + ri * math.sin(a1))
        o.append(f'<path d="M{p0[0]:.1f} {p0[1]:.1f} L{e0[0]:.1f} {e0[1]:.1f} A{ri:.1f} {ri:.1f} 0 0 1 {e1[0]:.1f} {e1[1]:.1f} Z" '
                 f'fill="none" stroke="{c}" stroke-width="{w * .6:.2f}" stroke-linejoin="round"/>')
        # juice vesicle lines
        am = (a0 + a1) / 2
        for k in (0.35, 0.55, 0.72):
            px, py = cx + ri * k * math.cos(am), cy + ri * k * math.sin(am)
            o.append(f'<path d="M{px - 3 * math.cos(am):.1f} {py - 3 * math.sin(am):.1f} l{6 * math.cos(am):.1f} {6 * math.sin(am):.1f}" '
                     f'stroke="{c}" stroke-width="{w * .45:.2f}" opacity=".7"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r * .06:.1f}" fill="none" stroke="{c}" stroke-width="{w * .6:.1f}"/>')
    return '\n'.join(o)


def blossom(cx, cy, r, c, w=1.8, rot=0):
    o = []
    for i in range(5):
        a = rot + i * 72
        o.append(f'<ellipse cx="{cx}" cy="{cy - r * .55:.1f}" rx="{r * .32:.1f}" ry="{r * .55:.1f}" '
                 f'transform="rotate({a} {cx} {cy})" fill="none" stroke="{c}" stroke-width="{w}"/>')
    for i in range(8):
        a = math.radians(i * 45 + rot)
        o.append(f'<path d="M{cx} {cy} L{cx + r * .38 * math.cos(a):.1f} {cy + r * .38 * math.sin(a):.1f}" stroke="{c}" stroke-width="{w * .6:.1f}"/>'
                 f'<circle cx="{cx + r * .4 * math.cos(a):.1f}" cy="{cy + r * .4 * math.sin(a):.1f}" r="{w * 1.1:.1f}" fill="{c}"/>')
    return '\n'.join(o)


def branch_header(c='#d9a940'):
    """Large composition for the header (viewBox 0 0 760 500)."""
    o = ['<svg viewBox="0 0 760 500" width="760" height="500" stroke-linecap="round" stroke-linejoin="round">']
    # main stem
    o.append(f'<path d="M20 470 C 160 400, 300 330, 430 250 C 520 195, 610 150, 740 120" fill="none" stroke="{c}" stroke-width="5"/>')
    o.append(f'<path d="M300 330 C 300 290, 320 250, 350 222" fill="none" stroke="{c}" stroke-width="3.5"/>')
    o.append(f'<path d="M560 168 C 580 140, 590 105, 585 70" fill="none" stroke="{c}" stroke-width="3"/>')
    for (x, y, L, ang) in [(90, 432, 150, -120), (170, 392, 160, 205), (250, 352, 150, -95), (400, 268, 170, 200),
                           (470, 225, 150, -70), (640, 140, 140, -125), (690, 128, 130, 165), (585, 72, 110, -60)]:
        o.append(leaf(x, y, L, ang, c, w=3.2))
    o.append(fruit(350, 300, 95, c, w=3.4, seed=3))
    o.append(fruit(560, 250, 72, c, w=3.2, seed=7))
    o.append(slice_(150, 230, 78, c, w=3, rot=8))
    o.append(blossom(700, 60, 34, c, w=2.4, rot=15))
    o.append(blossom(640, 330, 22, c, rot=40))
    o.append('</svg>')
    return '\n'.join(o)


def sprig(c, w=260, flip=False, seed=2):
    """Small corner sprig (viewBox 0 0 260 200)."""
    tr = ' transform="translate(260 0) scale(-1 1)"' if flip else ''
    o = [f'<svg viewBox="0 0 260 200" width="{w}" height="{w * 200 / 260:.0f}" stroke-linecap="round" stroke-linejoin="round"><g{tr}>']
    o.append(f'<path d="M10 190 C 70 150, 130 120, 220 60" fill="none" stroke="{c}" stroke-width="3"/>')
    for (x, y, L, ang) in [(50, 165, 80, -110), (95, 138, 85, 195), (140, 112, 80, -95), (185, 85, 75, 200)]:
        o.append(leaf(x, y, L, ang, c, w=1.8, veins=5))
    o.append(fruit(222, 72, 30, c, w=1.8, seed=seed))
    o.append('</g></svg>')
    return '\n'.join(o)


def fruit_plate(c, size=300):
    """Fruit + slice study for the 'Why bergamot' box (viewBox 0 0 300 260)."""
    o = [f'<svg viewBox="0 0 300 260" width="{size}" height="{size * 260 / 300:.0f}" stroke-linecap="round" stroke-linejoin="round">']
    o.append(leaf(150, 70, 110, -40, c, w=1.8, veins=6))
    o.append(f'<path d="M118 92 C 130 80, 140 74, 150 70" fill="none" stroke="{c}" stroke-width="2.4"/>')
    o.append(fruit(110, 160, 82, c, w=2, seed=11))
    o.append(slice_(232, 190, 58, c, w=1.8, rot=12))
    o.append('</svg>')
    return '\n'.join(o)


ICONS = {
    'pulse': '<path d="M3 17h7l3-7 5 14 4-9 3 2h8"/>',
    'leaf': '<path d="M6 28C6 14 16 6 30 6c0 14-8 24-22 22z"/><path d="M6 28L22 12"/>',
    'cog': '<circle cx="18" cy="18" r="5"/><path d="M18 3v5M18 28v5M3 18h5M28 18h5M7.4 7.4l3.5 3.5M25.1 25.1l3.5 3.5M7.4 28.6l3.5-3.5M25.1 10.9l3.5-3.5"/>',
    'scale': '<path d="M18 4v26M8 30h20M6 10h24M6 10l-4 9h8zM30 10l-4 9h8z"/>',
    'chart': '<path d="M4 4v28h28"/><path d="M8 26l7-8 6 4 10-12"/>',
    'people': '<circle cx="12" cy="11" r="5"/><circle cx="25" cy="13" r="4"/><path d="M3 31c0-6 4-10 9-10s9 4 9 10M21 31c0-5 2-8 5-8s6 3 6 8"/>',
    'search': '<circle cx="15" cy="15" r="9"/><path d="M22 22l10 10"/>',
    'bars': '<path d="M4 32h28"/><path d="M8 32V18h5v14M16 32V10h5v22M24 32V22h5v10"/>',
    'steps': '<path d="M4 30h8v-8h8v-8h8V6h4"/>',
    'flask': '<path d="M13 4h10M15 4v10L6 30a2 2 0 0 0 2 3h20a2 2 0 0 0 2-3L21 14V4"/><path d="M10 24h16"/>',
    'check': '<circle cx="18" cy="18" r="14"/><path d="M11 18l5 5 9-10"/>',
}


def icon(name, c='#d9a940', size=36):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 36 36" fill="none" stroke="{c}" stroke-width="2.4" '
            f'stroke-linecap="round" stroke-linejoin="round" style="flex:none">{ICONS[name]}</svg>')


def ornament(c, width=520):
    """Divider: line – leaf – fruit – leaf – line (viewBox 0 0 520 40)."""
    return (f'<svg viewBox="0 0 520 40" width="{width}" height="{width * 40 / 520:.0f}" stroke-linecap="round">'
            f'<path d="M10 20H200M320 20H510" stroke="{c}" stroke-width="2"/>'
            + leaf(232, 20, 30, 180, c, w=1.6, veins=3) + leaf(288, 20, 30, 0, c, w=1.6, veins=3)
            + f'<circle cx="260" cy="20" r="11" fill="none" stroke="{c}" stroke-width="2"/>'
            f'<circle cx="260" cy="9" r="1.5" fill="{c}"/></svg>')
