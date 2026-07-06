from PIL import Image, ImageDraw, ImageFont
import os

# ── Beige book / editorial-on-cream palette ──────────────────────────────────
PAPER = (241, 231, 211)      # warm cream
INK   = (33, 28, 20)         # near-black warm ink
RUST  = (168, 64, 42)        # wax-seal rust accent

def serif(size, bold=True):
    path = "/System/Library/Fonts/Supplemental/Didot.ttc" if bold else \
           "/System/Library/Fonts/Supplemental/Georgia.ttf"
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", size)

def make_icon(size):
    img = Image.new("RGB", (size, size), PAPER)
    d = ImageDraw.Draw(img)
    cx = cy = size / 2

    # Outer ink ring — like a medallion / wax seal edge
    ring_r = size * 0.44
    d.ellipse([cx-ring_r, cy-ring_r, cx+ring_r, cy+ring_r],
              outline=INK, width=max(2, round(size*0.014)))

    # Inner rust ring, slightly inset
    ring_r2 = size * 0.385
    d.ellipse([cx-ring_r2, cy-ring_r2, cx+ring_r2, cy+ring_r2],
              outline=RUST, width=max(1, round(size*0.006)))

    # Center serif monogram "V"
    f = serif(round(size * 0.46))
    text = "V"
    bbox = d.textbbox((0, 0), text, font=f)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    d.text((cx - tw/2 - bbox[0], cy - th/2 - bbox[1] - size*0.02), text, fill=INK, font=f)

    # Small rust underline rule beneath the letter
    rule_w = size * 0.16
    rule_y = cy + size * 0.155
    d.line([cx-rule_w/2, rule_y, cx+rule_w/2, rule_y], fill=RUST, width=max(2, round(size*0.012)))

    return img

sizes = [1024, 180, 120, 167, 152, 76, 80, 60, 58, 40, 29, 20]
out_dir = "/Users/besonnet.kl2/void-freq-ios/icons"
os.makedirs(out_dir, exist_ok=True)

for s in sizes:
    img = make_icon(s)
    path = f"{out_dir}/icon_{s}.png"
    img.save(path, "PNG")
    print(f"✓ {s}x{s} → {path}")

print("\nAll icons generated.")
