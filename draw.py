#!/usr/bin/env python3
"""Draw the front page of 24 November 2026 as a single 1024x1024 PNG.

Stories (researched 24 Nov 2026, sources in news-research-20261124.md):
  1. Jensen Huang returns as Nvidia CEO; Nvidia +31%, Nasdaq +6.5%.
  2. US sanctions hit Iran's shadow banking ("Operation Economic Outcast").
  3. Russian ship Sparta II hit by drones in the Baltic; corvette sunk off Libya.
  4. COP31 collapses in Antalya with no deal.
  5. Banten candy factory fire: 24 dead, ~30 missing.
  Sport ribbon: Verstappen wins Las Vegas GP; Alcaraz wins ATP Finals.

Deterministic: fixed palette, fixed geometry, no randomness, no network.
Run: python3 draw.py  ->  writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text(draw, xy, s, fnt, fill, anchor="la", stroke=0, stroke_fill=None):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor,
              stroke_width=stroke, stroke_fill=stroke_fill)


def fit(draw, s, fnt_path, size, max_w, bold=True):
    """Largest font size <= size that fits s in max_w."""
    while size > 10:
        f = font(fnt_path, size)
        if draw.textlength(s, font=f) <= max_w:
            return f
        size -= 2
    return font(fnt_path, size)


def wrap(draw, s, fnt, max_w):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def vgrad(base, top, bottom, h):
    img = Image.new("RGB", (1, h))
    px = img.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        px[0, y] = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
    return img.resize((W, h))


def rrect(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


# ---------------------------------------------------------------- palette
NAVY = (13, 27, 46)
NAVY2 = (18, 38, 62)
PAPER = (245, 239, 224)
INK = (20, 24, 30)
GOLD = (212, 175, 55)
GREEN = (34, 229, 132)
GREEN_D = (6, 43, 26)
GREEN_M = (14, 122, 61)
SEA = (16, 27, 42)
GREYSEA = (58, 74, 92)
ORANGE = (255, 122, 26)
FIRE = (255, 176, 32)
RED = (226, 54, 54)
WHITE = (255, 255, 255)
MIST = (214, 222, 230)
SMOKE = (44, 44, 48)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")

# ================================================================ masthead
d.rectangle([0, 0, W, 104], fill=NAVY)
d.rectangle([0, 104, W, 108], fill=GOLD)
text(d, (28, 52), "THE WORLD", font(SERIF_B, 62), WHITE, anchor="lm")
text(d, (996, 40), "TUESDAY", font(SANS_B, 26), GOLD, anchor="ra")
text(d, (996, 72), "24 NOVEMBER 2026", font(SANS_B, 26), WHITE, anchor="ra")

# ================================================================ lead: Nvidia
lead = Image.new("RGB", (W, 326), GREEN_D)
ld = ImageDraw.Draw(lead, "RGBA")
# rising chart with glow
pts = [(0, 262), (90, 238), (180, 250), (280, 205), (380, 220),
       (480, 168), (580, 182), (680, 122), (790, 135), (900, 78), (1024, 36)]
area = pts + [(1024, 326), (0, 326)]
ld.polygon(area, fill=(16, 122, 61, 90))
for wdt, col in ((14, (34, 229, 132, 60)), (8, (34, 229, 132, 140)),
                 (4, (120, 255, 180, 255))):
    ld.line(pts, fill=col, width=wdt, joint="curve")
for (x, y) in pts[::2]:
    ld.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(120, 255, 180, 255))
img.paste(lead, (0, 108))
d = ImageDraw.Draw(img, "RGBA")
# chip motif top-right of lead
cx, cy = 930, 165
d.rectangle([cx - 34, cy - 34, cx + 34, cy + 34], fill=(10, 60, 36),
            outline=GREEN, width=3)
d.rectangle([cx - 16, cy - 16, cx + 16, cy + 16], outline=GREEN, width=2)
for dx in (-46, -23, 0, 23, 46):
    d.line([cx + dx, cy - 46, cx + dx, cy - 34], fill=GREEN, width=3)
    d.line([cx + dx, cy + 34, cx + dx, cy + 46], fill=GREEN, width=3)
    d.line([cx - 46, cy + dx, cx - 34, cy + dx], fill=GREEN, width=3)
    d.line([cx + 34, cy + dx, cx + 46, cy + dx], fill=GREEN, width=3)
text(d, (28, 138), "+31%", font(SANS_B, 148), GREEN, stroke=2,
     stroke_fill=(0, 0, 0))
text(d, (30, 300), "HUANG'S BACK", font(SANS_B, 58), WHITE)
text(d, (30, 362), "Nvidia soars as Wall Street has its wildest day",
     font(SANS, 27), (220, 235, 220))
text(d, (30, 402), "Huang returns as CEO, 11 days after quitting · Nasdaq +6.5% · S&P +4.7% · Dow +3%",
     font(SANS, 21), (170, 200, 180))

# ================================================================ middle row
MY0, MY1 = 446, 700
# ---- left: Iran / Hormuz
d.rectangle([12, MY0, 500, MY1], fill=SEA)
# sea + tankers along the bottom strip
for x0, hull_w in ((40, 150), (220, 150)):
    d.rectangle([x0, 640, x0 + hull_w, 668], fill=(8, 14, 24))
    d.rectangle([x0 + 10, 618, x0 + hull_w - 10, 640], fill=(24, 38, 56))
# burning tanker, right corner: hull, flame, smoke (visual zone x 400-500)
d.rectangle([400, 640, 488, 668], fill=(8, 14, 24))
d.rectangle([410, 618, 478, 640], fill=(24, 38, 56))
d.polygon([(412, 640), (444, 608), (476, 640)], fill=ORANGE)
d.polygon([(426, 640), (444, 620), (462, 640)], fill=FIRE)
for (sx, sy, r) in ((425, 588, 13), (445, 564, 17), (465, 588, 12)):
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(120, 120, 125, 170))
for gx in range(20, 500, 46):
    d.line([gx, 682, gx + 26, 682], fill=(90, 120, 150), width=2)
text(d, (28, 470), "U.S. SQUEEZES IRAN'S", font(SANS_B, 33), WHITE)
text(d, (28, 508), "LAST LIFELINE", font(SANS_B, 33), WHITE)
d.rectangle([28, 546, 200, 551], fill=RED)
text(d, (28, 566), "“Operation Economic Outcast”", font(SANS, 21), MIST)
text(d, (28, 594), "hits $14.7bn of shadow banking", font(SANS, 21), MIST)
text(d, (28, 622), "Brent $114.80 · blockade day 268", font(SANS, 21), MIST)

# ---- right: Baltic war
d.rectangle([524, MY0, 1012, MY1], fill=(38, 52, 68))
# grey sea + burning ship in the bottom band (visual zone y 620-700)
d.rectangle([524, 680, 1012, 700], fill=(28, 40, 54))
d.polygon([(600, 656), (880, 656), (850, 684), (630, 684)], fill=(12, 18, 28))
d.rectangle([640, 634, 700, 656], fill=(20, 28, 40))
d.rectangle([740, 628, 830, 656], fill=(16, 24, 36))
for (fx, fy, r) in ((660, 630, 13), (700, 626, 16), (740, 630, 12),
                    (800, 628, 14)):
    d.polygon([(fx - r, fy + 26), (fx, fy), (fx + r, fy + 26)], fill=ORANGE)
    d.polygon([(fx - r // 2, fy + 26), (fx, fy + 12), (fx + r // 2, fy + 26)],
              fill=FIRE)
# drones, top-right corner clear of the headline
for (dx, dy) in ((935, 465), (970, 505), (992, 462)):
    d.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=WHITE)
    d.line([dx - 12, dy, dx + 12, dy], fill=WHITE, width=2)
    d.line([dx, dy - 12, dx, dy + 12], fill=WHITE, width=2)
text(d, (540, 470), "WAR SPILLS INTO", font(SANS_B, 33), WHITE)
text(d, (540, 508), "THE BALTIC", font(SANS_B, 33), WHITE)
text(d, (540, 548), "Russian ship Sparta II hit", font(SANS, 21), MIST)
text(d, (540, 576), "by drones off Finland · corvette", font(SANS, 21), MIST)
text(d, (540, 604), "sunk off Libya · missiles hit Poland", font(SANS, 21), MIST)

# ================================================================ bottom row
BY0, BY1 = 712, 936
# ---- left: COP31
d.rectangle([12, BY0, 500, BY1], fill=(52, 34, 22))
d.rectangle([12, BY0, 500, BY0 + 118], fill=(96, 58, 30))
# cracked globe, right side clear of the text
gx, gy, gr = 440, 812, 50
d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(40, 90, 70),
          outline=(230, 200, 120), width=3)
d.line([gx - 30, gy - 55, gx - 8, gy - 10, gx - 26, gy + 30], fill=(20, 40, 30),
       width=4)
d.line([gx - 8, gy - 10, gx + 24, gy + 8, gx + 10, gy + 52], fill=(20, 40, 30),
       width=4)
d.line([gx + 24, gy + 8, gx + 48, gy - 12], fill=(20, 40, 30), width=4)
# empty chairs along the bottom, below the text
for cx0 in (48, 118, 188, 258):
    d.rectangle([cx0, 908, cx0 + 52, 920], fill=(30, 20, 14))
    d.rectangle([cx0 + 4, 884, cx0 + 48, 908], fill=(46, 30, 20))
text(d, (28, 736), "COP31 COLLAPSES", font(SANS_B, 33), WHITE)
text(d, (28, 774), "Longest climate summit ever", font(SANS, 21), MIST)
text(d, (28, 802), "ends with no deal in Antalya", font(SANS, 21), MIST)
text(d, (28, 830), "190+ nations fail to agree", font(SANS, 21), MIST)
text(d, (28, 858), "on fossil fuels", font(SANS, 21), MIST)

# ---- right: Banten fire
d.rectangle([524, BY0, 1012, BY1], fill=(26, 24, 30))
# factory, bottom-right corner; smoke rising above it (visual zone x 860+)
d.rectangle([860, 885, 990, 936], fill=(12, 12, 16))
d.rectangle([860, 885, 990, 898], fill=(40, 38, 44))
for wx in range(872, 980, 36):
    d.rectangle([wx, 902, wx + 18, 922], fill=(255, 150, 40, 220))
for (sx, sy, r) in ((890, 862, 18), (920, 832, 24), (950, 862, 16),
                    (905, 802, 14)):
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(60, 60, 64, 200))
text(d, (540, 736), "24 DEAD IN BANTEN", font(SANS_B, 33), WHITE)
text(d, (540, 774), "FACTORY FIRE", font(SANS_B, 33), WHITE)
text(d, (540, 812), "Candy factory blaze in Cikande,", font(SANS, 21), MIST)
text(d, (540, 840), "Serang · ~30 still missing", font(SANS, 21), MIST)
text(d, (540, 868), "Families give DNA samples", font(SANS, 21), MIST)

# ================================================================ footer
d.rectangle([0, 948, W, H], fill=NAVY)
d.rectangle([0, 948, W, 952], fill=GOLD)
# checkered flag on a pole
d.line([40, 962, 40, 998], fill=WHITE, width=2)
for i in range(4):
    for j in range(2):
        if (i + j) % 2 == 0:
            d.rectangle([40 + i * 6, 962 + j * 9, 46 + i * 6, 971 + j * 9],
                        fill=INK)
        else:
            d.rectangle([40 + i * 6, 962 + j * 9, 46 + i * 6, 971 + j * 9],
                        fill=WHITE)
text(d, (74, 980), "SPORT  Verstappen wins Las Vegas GP  ·  Alcaraz wins ATP Finals",
     font(SANS_B, 19), WHITE, anchor="lm")
text(d, (996, 980), "24 NOV 2026", font(SANS_B, 20), GOLD, anchor="rm")

img.save(OUT, format="PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
