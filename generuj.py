#!/usr/bin/env python3
"""Makes profile/assets/studio-dark.svg and studio-light.svg, the animation of the studio's profile. Words and colors are here."""
import html
import math
from pathlib import Path

W, H = 900, 560
MONO = "'JetBrains Mono','Cascadia Code','SF Mono',Consolas,'DejaVu Sans Mono',monospace"
SANS = "'Inter','Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"

THEMES = {
    "dark": dict(bg="#070a14", tile="#0e1424", line="#1f2a44", txt="#e8edf8", dim="#8794b4", acc="#7aa2ff", acc2="#c08bff", chip="#16203a"),
    "light": dict(bg="#eef2fb", tile="#ffffff", line="#d3dcf0", txt="#141a2c", dim="#5b6785", acc="#2f5fe0", acc2="#8a3fe0", chip="#eaf0fd"),
}
TERM = [  # (command, answer)
    ("whoami", "Deadzone Studio"),
    ("ls projects", "pairlume  ricepick  CSSimulator"),
    ("cat about.txt", "Open source for Linux and Android."),
]
CARD = ("Pairlume", "stage 3: calls", ["Your phone and your Hyprland", "desktop as one: texts, calls", "and their voice."])
STACK = [  # (what, made with)
    ("Desktop", ["Rust", "QML", "Python", "GTK"]),
    ("Phone", ["Kotlin"]),
    ("Web", ["HTML", "CSS", "JavaScript"]),
    ("Tools", ["Bash", "Docker", "Git"]),
    ("Made on", ["Linux", "Hyprland"]),
]
e = html.escape

# logos from Simple Icons (assets/icons, CC0): file and brand color
ICONS = {
    "HTML": ("html5", "E34F26"), "CSS": ("css", "1572B6"), "JavaScript": ("javascript", "F7DF1E"), "QML": ("qt", "41CD52"),
    "Python": ("python", "3776AB"), "Node.js": ("nodedotjs", "5FA04E"), "Rust": ("rust", "000000"), "Kotlin": ("kotlin", "7F52FF"),
    "TypeScript": ("typescript", "3178C6"), "React": ("react", "61DAFB"), "C++": ("cplusplus", "00599C"), "C#": ("csharp", "512BD4"),
    "Java": ("java", "ED8B00"), "Lua": ("lua", "2C2D72"), "GTK": ("gtk", "7FE719"),
    "Linux": ("linux", "FCC624"), "Hyprland": ("hyprland", "58E1FF"), "Bash": ("gnubash", "4EAA25"), "Docker": ("docker", "2496ED"), "Git": ("git", "F05032"),
}


def lum(h):
    c = [int(h.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def icon(name, x, y, size, chip, txt):
    """the logo in its brand color; a color that would vanish on the chip (black Rust on dark) takes the text's"""
    if name not in ICONS:
        return ""
    f, hexc = ICONS[name]
    import re
    d = re.search(r' d="([^"]+)"', (Path(__file__).parent / "profile" / "assets" / "icons" / f"{f}.svg").read_text()).group(1)
    a, b = lum("#" + hexc), lum(chip)
    fill = "#" + hexc if (max(a, b) + .05) / (min(a, b) + .05) >= 2.2 else txt
    return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 24 24"><path fill="{fill}" d="{d}"/></svg>'


def mono(x, y, s, fill, size=15, cls="", extra=""):
    w = round(len(s) * size * 0.6, 1)  # stala szerokosc znaku, zeby pisanie trafialo na kazdym systemie
    return f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" fill="{fill}" textLength="{w}" lengthAdjust="spacingAndGlyphs" xml:space="preserve" class="{cls}" {extra}>{e(s)}</text>', w


def sans(x, y, s, fill, size=14, weight=400, anchor="start"):
    return f'<text x="{x}" y="{y}" font-family="{SANS}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{e(s)}</text>'


def tile(x, y, w, h, c, delay, inner):
    return (f'<g class="tile" style="animation-delay:{delay}s"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{c["tile"]}" '
            f'stroke="{c["line"]}"/>{inner}</g>')


def build(c):
    o, defs = [], []
    # ---- pasek ----
    bar = ""
    for i in range(5):
        bar += f'<circle cx="{38 + i * 20}" cy="30" r="4" fill="{c["line"]}"/>'
    bar += f'<rect x="33" y="26" width="18" height="8" rx="4" fill="{c["acc"]}" class="ws"/>'
    bar += f'<rect x="370" y="17" width="160" height="26" rx="13" fill="{c["chip"]}"/>' + sans(450, 35, "Deadzone Studio", c["txt"], 14, 700, "middle")
    bar += sans(838, 35, "open source", c["dim"], 13, 500, "end") + f'<circle cx="858" cy="30" r="4" fill="{c["acc2"]}" class="pulse"/>'
    o.append(tile(12, 12, 876, 36, c, 0.05, bar))
    # ---- terminal ----
    t, y, at = "", 104, 0.9
    for n, (cmd, ans) in enumerate(TERM):
        a, _ = mono(36, y, "$", c["acc2"], cls="show", extra=f'style="animation-delay:{at:.2f}s"')
        b, w = mono(54, y, cmd, c["txt"])
        dur = max(0.4, len(cmd) * 0.07)
        defs.append(f'<clipPath id="k{n}"><rect x="54" y="{y - 18}" width="{w}" height="26" class="type" style="animation-duration:{dur:.2f}s;animation-delay:{at + .15:.2f}s;animation-timing-function:steps({len(cmd)})"/></clipPath>')
        t += a + f'<g clip-path="url(#k{n})">{b}</g>'
        at += dur + 0.35
        r, _ = mono(36, y + 27, ans, c["acc"] if n == 0 else c["dim"], cls="show", extra=f'style="animation-delay:{at:.2f}s"')
        t += r
        at += 0.45
        y += 64
    a, _ = mono(36, y, "$", c["acc2"], cls="show", extra=f'style="animation-delay:{at:.2f}s"')
    t += a + f'<g class="show" style="animation-delay:{at:.2f}s"><rect x="54" y="{y - 14}" width="9" height="18" fill="{c["txt"]}" class="blink"/></g>'
    o.append(tile(12, 60, 520, 262, c, 0.2, t))
    # ---- the studio's mark, and the circles of pairing going out from it ----
    cx, cy = 716, 191
    rings = ""
    for k in range(4):
        rings += (f'<circle cx="{cx}" cy="{cy}" r="34" fill="none" stroke="{c["acc"] if k % 2 == 0 else c["acc2"]}" stroke-width="2" '
                  f'class="ring" style="animation-delay:{k * 0.9:.1f}s"/>')
    defs.append(f'<linearGradient id="gm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["acc2"]}"/><stop offset="1" stop-color="{c["acc"]}"/></linearGradient>')
    mark = (f'<g transform="translate({cx - 40} {cy - 40}) scale(1.25)"><rect width="64" height="64" rx="15" fill="{c["bg"]}"/>'
            f'<circle cx="32" cy="32" r="18" fill="none" stroke="url(#gm)" stroke-width="6" stroke-linecap="round" stroke-dasharray="86 27.1" '
            f'transform="rotate(-62 32 32)" class="arc"/><circle cx="32" cy="32" r="5.5" fill="{c["txt"]}"/></g>')
    o.append(tile(544, 60, 344, 262, c, 0.35, f'<g clip-path="url(#ct)">{rings}</g>{mark}'))
    defs.append('<clipPath id="ct"><rect x="545" y="61" width="342" height="260" rx="13"/></clipPath>')
    # ---- projekt ----
    name, lang, lines = CARD
    s = sans(34, 370, name, c["txt"], 19, 700)
    for j, l in enumerate(lines):
        s += sans(34, 402 + j * 23, l, c["dim"], 14)
    s += f'<circle cx="39" cy="523" r="5" fill="{c["acc"]}"/>' + sans(52, 528, lang, c["txt"], 13, 500)
    o.append(tile(12, 334, 284, 214, c, 0.5, s))
    # ---- czego uzywam ----
    s, i = "", 0
    for r, (cat, items) in enumerate(STACK):
        y = 348 + r * 38
        s += sans(330, y + 20, cat, c["dim"], 14, 600)
        x = 420
        for k in items:
            logo = k in ICONS
            w = len(k) * 7.0 + 20 + (18 if logo else 0)
            s += (f'<g class="pop" style="animation-delay:{1.0 + i * .08:.2f}s"><rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="30" rx="15" fill="{c["chip"]}"/>'
                  f'{icon(k, round(x + 10, 1), y + 8.5, 13, c["chip"], c["txt"])}{sans(round(x + w / 2 + (9 if logo else 0), 1), y + 20, k, c["txt"], 12.5, 500, "middle")}</g>')
            x += w + 8
            i += 1
    o.append(tile(308, 334, 580, 214, c, 0.65, s))
    css = """
.tile{opacity:0;transform-box:fill-box;transform-origin:center;animation:tile .6s cubic-bezier(.2,.9,.25,1.08) forwards}
@keyframes tile{from{opacity:0;transform:scale(.94)}to{opacity:1;transform:none}}
.show{opacity:0;animation:show .01s linear forwards}
@keyframes show{to{opacity:1}}
.type{transform-box:fill-box;transform-origin:left;transform:scaleX(0);animation-name:type;animation-fill-mode:forwards}
@keyframes type{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.pop{opacity:0;transform-box:fill-box;transform-origin:center;animation:pop .4s cubic-bezier(.2,.9,.3,1.3) forwards}
@keyframes pop{from{opacity:0;transform:scale(.7)}to{opacity:1;transform:none}}
.blink{animation:bl 1.1s steps(1) infinite}
@keyframes bl{0%,55%{opacity:1}56%,100%{opacity:0}}
.pulse{animation:pu 2.2s ease-in-out infinite}
@keyframes pu{0%,100%{opacity:.3}50%{opacity:1}}
.ring{transform-box:fill-box;transform-origin:center;opacity:0;animation:ring 3.6s cubic-bezier(.16,1,.3,1) infinite}
@keyframes ring{0%{opacity:0;transform:scale(1)}15%{opacity:.9}100%{opacity:0;transform:scale(4.2)}}
.arc{stroke-dashoffset:113;animation:draw 1.2s cubic-bezier(.16,1,.3,1) .5s forwards}
@keyframes draw{to{stroke-dashoffset:0}}
.eq{transform-box:fill-box;transform-origin:bottom;animation:eq0 1.6s ease-in-out infinite alternate}
.k1{animation-name:eq1}.k2{animation-name:eq2}.k3{animation-name:eq3}
@keyframes eq0{0%{transform:scaleY(.2)}35%{transform:scaleY(.7)}60%{transform:scaleY(.4)}100%{transform:scaleY(1)}}
@keyframes eq1{0%{transform:scaleY(.85)}30%{transform:scaleY(.3)}70%{transform:scaleY(.65)}100%{transform:scaleY(.15)}}
@keyframes eq2{0%{transform:scaleY(.4)}25%{transform:scaleY(1)}55%{transform:scaleY(.25)}100%{transform:scaleY(.75)}}
@keyframes eq3{0%{transform:scaleY(.6)}40%{transform:scaleY(.2)}75%{transform:scaleY(.95)}100%{transform:scaleY(.35)}}
.ws{animation:ws 12s cubic-bezier(.3,1,.4,1) infinite}
@keyframes ws{0%,18%{transform:translateX(0)}22%,42%{transform:translateX(20px)}46%,66%{transform:translateX(60px)}70%,90%{transform:translateX(40px)}94%,100%{transform:translateX(0)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;opacity:1!important}.arc{stroke-dashoffset:0}.ring{opacity:.3!important}.ring:nth-of-type(1){transform:scale(1.7)!important}.ring:nth-of-type(2){transform:scale(2.4)!important}.ring:nth-of-type(3){transform:scale(3.1)!important}.ring:nth-of-type(4){transform:scale(3.8)!important}.type,.tile,.pop{transform:none!important}}
"""
    label = "Deadzone Studio. " + " ".join(a for _, a in TERM[1:]) + f" {CARD[0]}: {' '.join(CARD[2])} " + " ".join(f"{k}: {', '.join(v)}." for k, v in STACK)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{e(label)}">'
            f'<style>{css}</style><defs>{"".join(defs)}</defs><rect width="{W}" height="{H}" rx="18" fill="{c["bg"]}"/>{"".join(o)}</svg>\n')


root = Path(__file__).parent
for name, c in THEMES.items():
    (root / "profile" / "assets" / f"studio-{name}.svg").write_text(build(c), encoding="utf-8")
