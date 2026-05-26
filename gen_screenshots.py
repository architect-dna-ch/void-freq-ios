from PIL import Image, ImageDraw, ImageFont
import math, os

W, H = 1284, 2778
BG = (4, 8, 15)
CYAN = (0, 238, 255)
PURPLE = (119, 85, 255)
WHITE = (240, 244, 255)
DIM = (80, 100, 130)

def font(size):
    for path in [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/System/Library/Fonts/SFNSText.ttf",
    ]:
        try: return ImageFont.truetype(path, size)
        except: pass
    return ImageFont.load_default()

def new_canvas():
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)

def draw_circle(img, d, cx, cy, r, active_ch=None):
    colors = {"focus": CYAN, "rain": (0,180,255), "void": PURPLE,
              "lofi": (255,160,50), "neurons": (180,80,255)}
    col = colors.get(active_ch, CYAN)
    # glow
    for i in range(8, 0, -1):
        a = int(15 - i*1.5)
        ov = Image.new("RGBA", (W, H), (0,0,0,0))
        od = ImageDraw.Draw(ov)
        rr = r + i*6
        od.ellipse([cx-rr,cy-rr,cx+rr,cy+rr], outline=col+(a,), width=2)
        img.paste(Image.alpha_composite(img.convert("RGBA"), ov).convert("RGB"))
    # bars
    bars = 48
    for i in range(bars):
        angle = (i/bars)*math.pi*2
        heights = [0.08,0.18,0.28,0.12,0.22,0.10,0.32,0.15,
                   0.09,0.24,0.20,0.11,0.35,0.14,0.09,0.23,
                   0.30,0.12,0.18,0.26,0.10,0.21,0.16,0.28,
                   0.08,0.18,0.28,0.12,0.22,0.10,0.32,0.15,
                   0.09,0.24,0.20,0.11,0.35,0.14,0.09,0.23,
                   0.30,0.12,0.18,0.26,0.10,0.21,0.16,0.28]
        h = heights[i%len(heights)] * r * 0.9
        ir, or_ = r, r+h
        x1=cx+math.cos(angle)*ir; y1=cy+math.sin(angle)*ir
        x2=cx+math.cos(angle)*or_; y2=cy+math.sin(angle)*or_
        t = i/bars
        rc=int(col[0]*(1-t)+PURPLE[0]*t)
        gc=int(col[1]*(1-t)+PURPLE[1]*t)
        bc=int(col[2]*(1-t)+PURPLE[2]*t)
        d.line([x1,y1,x2,y2], fill=(rc,gc,bc), width=4)
    # inner fill
    d.ellipse([cx-r,cy-r,cx+r,cy+r], fill=BG)
    d.ellipse([cx-r,cy-r,cx+r,cy+r], outline=col, width=3)
    # center dot
    cr=r*0.06; d.ellipse([cx-cr,cy-cr,cx+cr,cy+cr], fill=col)

def centered(d, text, y, f, color=WHITE):
    bb = d.textbbox((0,0), text, font=f)
    x = (W - (bb[2]-bb[0])) // 2
    d.text((x, y), text, fill=color, font=f)

def pill(d, text, x, y, active=False):
    f = font(36)
    bb = d.textbbox((0,0), text, font=f)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    pad_x, pad_y = 40, 20
    bx0,by0 = x, y
    bx1,by1 = x+tw+pad_x*2, y+th+pad_y*2
    col = CYAN if active else (30,40,55)
    tcol = BG if active else DIM
    d.rounded_rectangle([bx0,by0,bx1,by1], radius=20, fill=col)
    d.text((bx0+pad_x, by0+pad_y), text, fill=tcol, font=f)
    return bx1+24

# ── Screenshot 1: Hero ────────────────────────────────────────────────────────
img, d = new_canvas()
cx, cy = W//2, H//2 - 120
draw_circle(img, d, cx, cy, 340, "focus")
d = ImageDraw.Draw(img)
centered(d, "VOID FREQ", 160, font(88), CYAN)
centered(d, "AMBIENT FOCUS STUDIO", 270, font(44), DIM)
centered(d, "FOCUS", cy+380, font(52), CYAN)
centered(d, "Brown noise · 40Hz gamma entrainment", cy+450, font(38), DIM)
img.save("/Users/besonnet.kl2/void-freq-ios/screenshots/01_hero.png")
print("✓ Screenshot 1: Hero")

# ── Screenshot 2: Channels ────────────────────────────────────────────────────
img, d = new_canvas()
centered(d, "FIVE CHANNELS", 220, font(80), WHITE)
centered(d, "for every state of mind", 330, font(44), DIM)
channels = [
    ("FOCUS",   CYAN,          "Brown noise · Gamma entrainment"),
    ("RAIN",    (0,180,255),   "Layered rainfall · Sub-bass rumble"),
    ("VOID",    PURPLE,        "Pure sine oscillators · Isolation"),
    ("LO-FI",   (255,160,50),  "Jazz chords · Vinyl crackle"),
    ("NEURONS", (180,80,255),  "Binaural beats · Alpha 10Hz"),
]
y = 520
for name, col, sub in channels:
    d.rounded_rectangle([80, y, W-80, y+140], radius=24, fill=(10,16,28))
    d.rounded_rectangle([80, y, 16+80, y+140], radius=24, fill=col)
    d.rectangle([80, y, 96, y+140], fill=col)
    d.text((140, y+22), name, fill=col, font=font(52))
    d.text((140, y+84), sub, fill=DIM, font=font(36))
    y += 168
img.save("/Users/besonnet.kl2/void-freq-ios/screenshots/02_channels.png")
print("✓ Screenshot 2: Channels")

# ── Screenshot 3: Visualizer ──────────────────────────────────────────────────
img, d = new_canvas()
cx, cy = W//2, H//2 - 60
draw_circle(img, d, cx, cy, 420, "neurons")
d = ImageDraw.Draw(img)
centered(d, "LIVE VISUALIZER", H-560, font(70), WHITE)
centered(d, "Real-time FFT reacts to every frequency", H-470, font(38), DIM)
centered(d, "NEURONS ACTIVE", cy-500, font(42), (180,80,255))
img.save("/Users/besonnet.kl2/void-freq-ios/screenshots/03_visualizer.png")
print("✓ Screenshot 3: Visualizer")

# ── Screenshot 4: No BS ───────────────────────────────────────────────────────
img, d = new_canvas()
centered(d, "NO SUBSCRIPTIONS", 300, font(80), WHITE)
centered(d, "NO ADS.  NO ACCOUNTS.", 410, font(56), DIM)
centered(d, "NO STREAMING.", 490, font(56), DIM)
facts = [
    ("⚡", "Real-time audio synthesis"),
    ("✈", "Works offline"),
    ("🔋", "Background playback"),
    ("🎧", "Binaural headphone mode"),
]
y = 720
for icon, text in facts:
    d.rounded_rectangle([100, y, W-100, y+120], radius=20, fill=(10,16,28))
    d.text((160, y+30), icon, fill=CYAN, font=font(52))
    d.text((280, y+34), text, fill=WHITE, font=font(48))
    y += 148
centered(d, "PAY ONCE. FOCUS FOREVER.", H-320, font(58), CYAN)
centered(d, "Built by Architect-DNA · Bern", H-230, font(38), DIM)
img.save("/Users/besonnet.kl2/void-freq-ios/screenshots/04_nobs.png")
print("✓ Screenshot 4: No BS")

print("\nAll screenshots done → /Users/besonnet.kl2/void-freq-ios/screenshots/")
