#!/usr/bin/env python3
"""og.png 1200x630 — Bluebonnet Books & Wine (2x supersample, auto-fit text).
Deep-wine reading room, brass glow, stacked books + wine glass + bluebonnet sprigs,
jewel-rug band. Shop identity only — zero builder tokens."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
S = 2
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "og.png")

WINE = (59, 31, 48); WINE2 = (42, 21, 34); BRASS = (185, 138, 47); BRASSL = (217, 180, 95)
CREAM = (248, 239, 227); ROSE = (185, 85, 111); BB = (91, 116, 184); BBL = (143, 167, 216)
WINE3 = (107, 52, 83); INKD = (43, 29, 39); SOFT = (238, 221, 222)

def font(paths, size):
    bases = ["/System/Library/Fonts/Supplemental/", "/System/Library/Fonts/"]
    for b in bases:
        for n in paths:
            p = b + n
            if os.path.exists(p):
                try: return ImageFont.truetype(p, size * S)
                except Exception: pass
    return ImageFont.load_default()

def fit(paths, size, text, maxw):
    while size > 10:
        f = font(paths, size)
        if f.getlength(text) <= maxw * S: return f, size
        size -= 2
    return font(paths, size), size

def P(x, y): return (x * S, y * S)

Georgia = lambda s: ["Georgia Bold.ttf", "Georgia.ttf"]
Menlo   = lambda s: ["Menlo.ttc", "Courier New Bold.ttf"]
Sans    = lambda s: ["Avenir Next Medium.ttf", "HelveticaNeue.ttc"]

img = Image.new("RGB", (W * S, H * S), WINE)
d = ImageDraw.Draw(img, "RGBA")

# gradient: wine -> deeper wine
for y in range(H * S):
    t = y / (H * S)
    r = int(WINE[0] + (WINE2[0] - WINE[0]) * t * .95)
    g = int(WINE[1] + (WINE2[1] - WINE[1]) * t * .95)
    b = int(WINE[2] + (WINE2[2] - WINE[2]) * t * .95)
    d.line([(0, y), (W * S, y)], fill=(r, g, b))
glow = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([990 * S - 300, 150 * S - 240, 990 * S + 300, 150 * S + 240], fill=(185, 138, 47, 52))
glow = glow.filter(__import__("PIL.ImageFilter", fromlist=["GaussianBlur"]).GaussianBlur(120 * S // 2))
img.paste(glow, (0, 0), glow)

L = 78
CX = 762  # art column starts here; all left text must end left of CX

# rug band across the bottom
ry0, ry1 = 566, 608
x = 0
band = [WINE3, BRASS, BB, WINE3, (52, 27, 42)]
while x < W:
    d.rectangle([x * S, ry0 * S, (x + 17) * S, ry1 * S], fill=band[0])
    d.rectangle([(x + 17) * S, ry0 * S, (x + 25) * S, ry1 * S], fill=band[1])
    d.rectangle([(x + 25) * S, ry0 * S, (x + 37) * S, ry1 * S], fill=band[2])
    d.rectangle([(x + 37) * S, ry0 * S, (x + 54) * S, ry1 * S], fill=band[3])
    d.rectangle([(x + 54) * S, ry0 * S, (x + 62) * S, ry1 * S], fill=band[4])
    x += 62

# ---- left text block ----
k, ks = fit(Menlo(None), 24, "OPENED SEPT. 10, 2026  ·  FORT WORTH, TX", CX - L - 20)
d.text((L * S, 86 * S), "OPENED SEPT. 10, 2026  ·  FORT WORTH, TX", font=k, fill=BRASSL)

t1, s1 = fit(Georgia(None), 92, "BLUEBONNET", CX - L - 10)
t2, s2 = fit(Georgia(None), 92, "BOOKS & WINE", CX - L - 10)
smin = min(s1, s2)
tf, _ = fit(Georgia(None), smin, "BOOKS & WINE", CX - L - 10)
d.text((L * S, 128 * S), "BLUEBONNET", font=tf, fill=(255, 249, 239))
d.text((L * S, (128 + smin * 1.12) * S), "BOOKS & WINE", font=tf, fill=BRASSL)

sf, ss = fit(Sans(None), 29, "Used books at $5 · $10 · $20 — antiques, gifts, book clubs.", CX - L - 10)
d.text((L * S, 342 * S), "Used books at $5 · $10 · $20 — antiques, gifts, book clubs.", font=sf, fill=SOFT)
sf2, ss2 = fit(Sans(None), 24, "Wed–Sat 10am–6pm · 3464 Blue Bonnet Cir #120 · near TCU", CX - L - 10)
d.text((L * S, 384 * S), "Wed–Sat 10am–6pm · 3464 Blue Bonnet Cir #120 · near TCU", font=sf2, fill=(203, 177, 162))
af, asz = fit(Sans(None), 21, "(817) 948-8436 · Fort Worth, TX 76109", CX - L - 10)
d.text((L * S, 424 * S), "(817) 948-8436 · Fort Worth, TX 76109", font=af, fill=(169, 139, 128))

# ---- right art: book stack, wine glass, bluebonnets ----
# stacked books (flat, front spines facing)
books = [
    (812, 352, 1116, 388, ROSE),
    (798, 314, 1100, 350, (127, 168, 127)),
    (824, 276, 1124, 312, BB),
    (806, 238, 1096, 274, BRASS),
]
for (x0, y0, x1, y1, col) in books:
    d.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], fill=col, outline=(42, 21, 34))
    # page edge
    d.rectangle([(x1 - 14) * S, (y0 + 4) * S, (x1 - 4) * S, (y1 - 4) * S], fill=CREAM)
    # title band on spine face
    d.rectangle([(x0 + 16) * S, (y0 + (y1 - y0) // 2 - 4) * S, (x0 + 130) * S, (y0 + (y1 - y0) // 2 + 4) * S], fill=(42, 21, 34, 140))

# wine glass above the stack
gx, gyr = 1008, 44
d.ellipse([(gx - gyr) * S, 118 * S, (gx + gyr) * S, (118 + 12) * S], outline=CREAM, width=3 * S)
d.polygon([P(gx - gyr + 6, 124), P(gx + gyr - 6, 124), P(gx, 196)], fill=(150, 60, 88, 190))
d.line([P(gx - gyr + 2, 120), P(gx, 202), P(gx + gyr - 2, 120)], fill=CREAM, width=3 * S, joint="curve")
d.line([P(gx, 202), P(gx, 224)], fill=CREAM, width=3 * S)
d.line([P(gx - 26, 226), P(gx + 26, 226)], fill=CREAM, width=3 * S)

# bluebonnet sprigs right edge
def sprig(bx, by):
    d.line([P(bx, by + 44), P(bx - 2, by + 18), P(bx + 1, by)], fill=(127, 168, 127), width=2 * S)
    for (ox, oy, r, col) in [(-9, 6, 7, BBL), (9, 10, 7, BB), (0, 0, 8, BBL), (-7, 22, 6, BB), (8, 26, 6, BBL), (0, 15, 5, (174, 195, 232))]:
        d.ellipse([(bx + ox - r) * S, (by + oy - r) * S, (bx + ox + r) * S, (by + oy + r) * S], fill=col)

sprig(1148, 250)
sprig(1108, 430)
sprig(1172, 430)

# thin brass rule under the title
d.rectangle([L * S, 322 * S, (L + 240) * S, (322 + 3) * S], fill=BRASS)

img = img.resize((W, H), Image.LANCZOS)
img.save(OUT, "PNG", optimize=True)
print("og.png", img.size, os.path.getsize(OUT), "bytes")
