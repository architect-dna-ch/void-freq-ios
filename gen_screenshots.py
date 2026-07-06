from PIL import Image, ImageDraw, ImageFont
import math, os

W, H = 1284, 2778
MARGIN = 100

# ── Beige book / editorial-on-cream-stock palette ────────────────────────────
PAPER  = (241, 231, 211)   # warm cream page
INK    = (33, 28, 20)      # near-black warm ink
INK2   = (108, 99, 82)     # muted ink (captions, deks)
INK3   = (168, 159, 139)   # faint ink (footnotes, rules)
RUST   = (168, 64, 42)

ACCENTS = {
    "focus":   RUST,
    "rain":    (46, 74, 99),
    "void":    (91, 59, 87),
    "lofi":    (166, 121, 31),
    "neurons": (75, 90, 46),
}

FONT_DIR = "/System/Library/Fonts/Supplemental/"

def didot(size):
    return ImageFont.truetype(FONT_DIR + "Didot.ttc", size)

def georgia(size, bold=False, italic=False):
    name = "Georgia"
    if bold and italic: name += " Bold Italic"
    elif bold: name += " Bold"
    elif italic: name += " Italic"
    return ImageFont.truetype(FONT_DIR + name + ".ttf", size)

def new_canvas():
    img = Image.new("RGB", (W, H), PAPER)
    return img, ImageDraw.Draw(img)

def tracked_width(d, text, font, tracking):
    w = 0
    for ch in text:
        bb = d.textbbox((0, 0), ch, font=font)
        w += (bb[2] - bb[0]) + tracking
    return w - tracking if text else 0

def draw_tracked(d, xy, text, font, fill, tracking=0, anchor="l"):
    x, y = xy
    total = tracked_width(d, text, font, tracking)
    if anchor == "c":
        x -= total / 2
    elif anchor == "r":
        x -= total
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        bb = d.textbbox((0, 0), ch, font=font)
        x += (bb[2] - bb[0]) + tracking
    return total

def centered(d, text, y, font, fill=INK):
    bb = d.textbbox((0, 0), text, font=font)
    x = (W - (bb[2] - bb[0])) // 2 - bb[0]
    d.text((x, y), text, fill=fill, font=font)
    return bb[3] - bb[1]

def rule(d, y, x0=MARGIN, x1=W - MARGIN, fill=INK3, width=2):
    d.line([x0, y, x1, y], fill=fill, width=width)

def running_head(d, left, right, page_no):
    y = 84
    draw_tracked(d, (MARGIN, y), left, georgia(22, bold=True), INK, tracking=4, anchor="l")
    draw_tracked(d, (W - MARGIN, y), right, georgia(20), INK2, tracking=4, anchor="r")
    rule(d, y + 46)

def footer(d, page_no, total=4):
    y = H - 130
    rule(d, y)
    draw_tracked(d, (MARGIN, y + 26), "ARCHITECT-DNA · BERN", georgia(20), INK2, tracking=3, anchor="l")
    draw_tracked(d, (W - MARGIN, y + 26), f"{page_no:02d} / {total:02d}", georgia(20), INK2, tracking=3, anchor="r")

def draw_dial(d, cx, cy, r, accent=RUST, ticks=48, seed=0):
    # outer ink ring
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=4)
    # inner accent ring
    ir = r * 0.9
    d.ellipse([cx - ir, cy - ir, cx + ir, cy + ir], outline=accent, width=2)
    # radiating engraved ticks
    heights = [0.10, 0.22, 0.14, 0.30, 0.12, 0.24, 0.16, 0.34,
               0.11, 0.26, 0.18, 0.28, 0.13, 0.20, 0.15, 0.32]
    for i in range(ticks):
        angle = (i / ticks) * math.pi * 2
        h = heights[(i + seed) % len(heights)] * r * 0.55
        x1 = cx + math.cos(angle) * r
        y1 = cy + math.sin(angle) * r
        x2 = cx + math.cos(angle) * (r + h)
        y2 = cy + math.sin(angle) * (r + h)
        col = accent if i % 6 == 0 else INK
        w = 3 if i % 6 == 0 else 1
        d.line([x1, y1, x2, y2], fill=col, width=w)
    # center mark
    cr = r * 0.045
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=accent)

OUT = "/Users/besonnet.kl2/void-freq-ios/screenshots"

# ── Screenshot 1: Cover ───────────────────────────────────────────────────────
img, d = new_canvas()
running_head(d, "VOID FREQ", "AMBIENT FOCUS STUDIO", 1)

y = 230
draw_tracked(d, (W // 2, y), "FOCUS STUDIO · VOID CELL", georgia(26, bold=True), RUST, tracking=6, anchor="c")
y += 84
centered(d, "VOID", y, didot(168), INK); y += 168
centered(d, "FREQ", y, didot(168), RUST); y += 196
d.text((MARGIN, y), "Five ambient soundscapes, synthesized live for", font=georgia(36, italic=True), fill=INK2)
y += 50
d.text((MARGIN, y), "deep work — brown noise, rain, lo-fi, binaural.", font=georgia(36, italic=True), fill=INK2)
y += 90
rule(d, y); y += 130

r = 460
cy = y + r
draw_dial(d, W // 2, cy, r, RUST, seed=0)
y2 = cy + r + 90
draw_tracked(d, (W // 2, y2), "FOCUS", georgia(44, bold=True), RUST, tracking=6, anchor="c")
centered(d, "Brown noise · 40Hz gamma entrainment", y2 + 62, georgia(32, italic=True), INK2)
y2 += 150
rule(d, y2)
centered(d, "Synthesized live in your browser or on your phone —", y2 + 50, georgia(30, italic=True), INK2)
centered(d, "no files, no streaming, no buffering.", y2 + 94, georgia(30, italic=True), INK2)

footer(d, 1)
img.save(f"{OUT}/01_hero.png")
print("✓ Screenshot 1: Cover")

# ── Screenshot 2: Contents (channels) ─────────────────────────────────────────
img, d = new_canvas()
running_head(d, "VOID FREQ", "TABLE OF CHANNELS", 2)

y = 230
centered(d, "FIVE CHANNELS", y, didot(110), INK); y += 128
centered(d, "For every state of mind.", y, georgia(36, italic=True), INK2); y += 80
rule(d, y); y += 90

channels = [
    ("I",   "FOCUS",   "focus",   "Brown noise · 40Hz gamma entrainment"),
    ("II",  "RAIN",    "rain",    "Layered rainfall · sub-bass rumble"),
    ("III", "VOID",    "void",    "Pure sine oscillators · isolation"),
    ("IV",  "LO-FI",   "lofi",    "Jazz chords · vinyl crackle"),
    ("V",   "NEURONS", "neurons", "Binaural beats · alpha 10Hz"),
]
row_h = 322
for num, name, key, desc in channels:
    accent = ACCENTS[key]
    draw_tracked(d, (MARGIN, y), num, didot(70), accent, tracking=0, anchor="l")
    tx = MARGIN + 120
    draw_tracked(d, (tx, y + 6), name, georgia(58, bold=True), INK, tracking=3, anchor="l")
    d.text((tx, y + 92), desc, font=georgia(34, italic=True), fill=INK2)
    d.rectangle([W - MARGIN - 16, y + 10, W - MARGIN, y + 10 + 84], fill=accent)
    y += row_h
    rule(d, y - 70, fill=INK3, width=1)

y += 40
d.text((MARGIN, y), "Every channel is synthesized in real time —", font=georgia(32, italic=True), fill=INK2)
d.text((MARGIN, y + 48), "no downloads, no buffering, no files.", font=georgia(32, italic=True), fill=INK2)

footer(d, 2)
img.save(f"{OUT}/02_channels.png")
print("✓ Screenshot 2: Contents")

# ── Screenshot 3: Visualizer ───────────────────────────────────────────────────
img, d = new_canvas()
running_head(d, "VOID FREQ", "LIVE VISUALIZER", 3)

y = 230
centered(d, "LIVE VISUALIZER", y, didot(100), INK); y += 112
centered(d, "Real-time FFT, rendered in ink.", y, georgia(36, italic=True), INK2); y += 80
rule(d, y); y += 90

draw_tracked(d, (W // 2, y), "NEURONS ACTIVE", georgia(32, bold=True), ACCENTS["neurons"], tracking=6, anchor="c")
y += 120
r = 520
cy = y + r
draw_dial(d, W // 2, cy, r, ACCENTS["neurons"], seed=3)

y2 = cy + r + 130
centered(d, "Binaural alpha entrainment at 10Hz —", y2, georgia(36, italic=True), INK2); y2 += 54
centered(d, "left channel 200Hz, right channel 210Hz.", y2, georgia(36, italic=True), INK2); y2 += 100
rule(d, y2); y2 += 60
centered(d, "Wear headphones. Let your brain synchronize.", y2, georgia(34, italic=True), INK2); y2 += 60
centered(d, "The ring pulses with the mix — brighter as intensity rises.", y2, georgia(34, italic=True), INK2)

footer(d, 3)
img.save(f"{OUT}/03_visualizer.png")
print("✓ Screenshot 3: Visualizer")

# ── Screenshot 4: Colophon (no subscriptions) ─────────────────────────────────
img, d = new_canvas()
running_head(d, "VOID FREQ", "COLOPHON", 4)

y = 230
centered(d, "NO SUBSCRIPTIONS", y, didot(100), INK); y += 112
centered(d, "No ads. No accounts. No streaming.", y, georgia(36, italic=True), INK2); y += 80
rule(d, y); y += 100

facts = [
    "Real-time audio synthesis",
    "Works fully offline",
    "Continues in background",
    "Binaural headphone mode",
]
for text in facts:
    d.rectangle([MARGIN, y + 14, MARGIN + 34, y + 48], fill=RUST)
    d.text((MARGIN + 76, y), text, font=georgia(46), fill=INK)
    y += 190
    rule(d, y - 65, fill=INK3, width=1)

y += 200
centered(d, "FREE FOREVER.", y, didot(100), RUST); y += 128
centered(d, "Focus anytime.", y, georgia(46, italic=True), INK2); y += 170
rule(d, y); y += 80
centered(d, "Built by Architect-DNA · Bern, Switzerland", y, georgia(32), INK3); y += 60
centered(d, "systems@architect-dna.ch", y, georgia(28), INK3)

footer(d, 4)
img.save(f"{OUT}/04_nobs.png")
print("✓ Screenshot 4: Colophon")

print(f"\nAll screenshots done → {OUT}/")
