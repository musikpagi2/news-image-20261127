#!/usr/bin/env python3
"""Draw the front page for THE WORLD TODAY - Friday, 27 November 2026.

Fresh build, drawn in this session from news first reported on 27 Nov 2026.
Output: entry.png, 1024x1024 JPEG.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (178, 34, 34)
GREY = (90, 88, 80)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=None, align="left", max_w=None):
    if leading is None:
        leading = int(fnt.size * 1.25)
    for line in lines:
        lx = x + (max_w - draw.textlength(line, font=fnt)) / 2 if align == "center" else x
        draw.text((lx, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fit_font(draw, text, path, start, max_w):
    size = start
    while size > 10:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return font(path, 10)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

d.rectangle([12, 12, W - 13, H - 13], outline=INK, width=2)
MX = 48
CW = W - 2 * MX  # 928

# ---- Masthead ----
y = 22
mast = fit_font(d, "THE WORLD TODAY", SERIF_B, 70, CW)
y = text_block(d, MX, y, ["THE WORLD TODAY"], mast, align="center", max_w=CW)
y += 4
d.line([(MX, y), (W - MX, y)], fill=INK, width=3)
y += 6
d.line([(MX, y), (W - MX, y)], fill=INK, width=1)
y += 10
date_f = font(SANS_B, 26)
y = text_block(d, MX, y, ["FRIDAY, 27 NOVEMBER 2026"], date_f, align="center", max_w=CW)
y += 6
d.line([(MX, y), (W - MX, y)], fill=INK, width=1)
y += 10

# ---- Lead story: Kuwait drone strike ----
kick = font(SANS_B, 20)
d.text((MX, y), "MIDDLE EAST", font=kick, fill=RED)
y += 28
lead_h = font(SERIF_B, 42)
y = text_block(d, MX, y, wrap(d, "TWO ITALIANS KILLED IN DRONE STRIKE ON KUWAIT FACILITY",
                              lead_h, CW), lead_h, leading=48)
y += 6

# ---- Illustration: drone over an industrial facility at dusk ----
IX, IY, IW, IH = MX, y, CW, 170
panel = Image.new("RGB", (IW, IH), PAPER)
p = ImageDraw.Draw(panel)
sky_top, sky_bot = (28, 36, 66), (226, 122, 48)
for i in range(IH):
    t = i / IH
    r = int(sky_top[0] + (sky_bot[0] - sky_top[0]) * t)
    g = int(sky_top[1] + (sky_bot[1] - sky_top[1]) * t)
    b = int(sky_top[2] + (sky_bot[2] - sky_top[2]) * t)
    p.line([(0, i), (IW, i)], fill=(r, g, b))
# Sun, upper left
p.ellipse([60, 16, 118, 74], fill=(255, 214, 120))
sil = (24, 22, 26)
base = IH - 30
# storage tanks
for tx, tw in [(30, 120), (170, 140), (640, 130)]:
    p.rectangle([tx, base - 56, tx + tw, base], fill=sil)
    p.ellipse([tx, base - 66, tx + tw, base - 46], fill=sil)
# columns
for tx, th, tw in [(360, 100, 42), (420, 112, 34), (800, 95, 38)]:
    p.rectangle([tx, base - th, tx + tw, base], fill=sil)
    p.ellipse([tx, base - th - 10, tx + tw, base - th + 10], fill=sil)
# flames from the struck column (top at base-112, flame rises 24 above it)
fx = 420
p.polygon([(fx - 6, base - 112), (fx + 40, base - 112), (fx + 17, base - 136)],
          fill=(255, 140, 20))
p.polygon([(fx + 4, base - 112), (fx + 30, base - 112), (fx + 17, base - 128)],
          fill=(255, 215, 80))
# smoke plumes, kept inside the panel and clear of the flame
for cx, cy, r in [(494, 28, 17), (520, 16, 13), (820, 34, 18), (846, 22, 16)]:
    p.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 146, 140))
# drone silhouette, upper right
dx, dy = 690, 48
p.ellipse([dx - 34, dy - 8, dx + 34, dy + 8], fill=sil)
p.ellipse([dx - 6, dy - 22, dx + 6, dy - 10], fill=sil)
p.line([(dx - 52, dy - 16), (dx - 16, dy - 10)], fill=sil, width=4)
p.line([(dx + 16, dy - 10), (dx + 52, dy - 16)], fill=sil, width=4)
p.ellipse([dx - 58, dy - 22, dx - 34, dy - 12], fill=(200, 200, 200))
p.ellipse([dx + 34, dy - 22, dx + 58, dy - 12], fill=(200, 200, 200))
# ground
p.rectangle([0, base, IW, IH], fill=(16, 20, 30))
p.line([(16, base + 20), (IW - 16, base + 20)], fill=(90, 110, 140), width=2)
img.paste(panel, (IX, IY))
d.rectangle([IX, IY, IX + IW, IY + IH], outline=INK, width=2)
y = IY + IH + 6
cap_f = font(SERIF_I, 16)
y = text_block(d, MX, y,
               ["An Iranian drone strike hit a facility in Kuwait, killing two Italians."],
               cap_f, fill=GREY)
y += 5
lead_b = font(SERIF, 20)
y = text_block(d, MX, y, wrap(d, "Two Italians were killed when an Iranian drone struck a "
                                  "facility in Kuwait, in a sharp escalation in the Gulf. "
                                  "Tehran denies responsibility.", lead_b, CW), lead_b, leading=25)
y += 8
d.line([(MX, y), (W - MX, y)], fill=INK, width=1)
y += 10

# ---- Two columns: Gaza | Thanksgiving storm ----
col_w = 452
col2_x = MX + col_w + 24
y0 = y
bottoms = []
for cx, kicker, head, body in [
    (MX, "GAZA", "HAMAS WEIGHS RESPONSE AFTER ISRAEL KILLS 10 IN GAZA",
     "Hamas is weighing its response after Israeli strikes killed 10 people in Gaza, "
     "in a fresh test of the fragile ceasefire."),
    (col2_x, "UNITED STATES", "THANKSGIVING STORM FLOODS CITIES, DELAYS FLIGHTS",
     "A major storm brought flooding and flight delays across the United States on "
     "Thanksgiving, and New York declared a state of emergency."),
]:
    cy = y0
    d.text((cx, cy), kicker, font=kick, fill=RED)
    cy += 26
    hf = font(SERIF_B, 26)
    cy = text_block(d, cx, cy, wrap(d, head, hf, col_w), hf, leading=31)
    cy += 4
    bf = font(SERIF, 17)
    cy = text_block(d, cx, cy, wrap(d, body, bf, col_w), bf, leading=22)
    bottoms.append(cy)
y = max(bottoms) + 8
d.line([(MX, y), (W - MX, y)], fill=INK, width=1)
y += 10

# ---- Full-width story: Bangkok refinery fire ----
d.text((MX, y), "THAILAND", font=kick, fill=RED)
y += 26
hf = font(SERIF_B, 29)
y = text_block(d, MX, y, wrap(d, "MASSIVE FIRE AT BANGKOK REFINERY INJURES SEVERAL",
                              hf, CW), hf, leading=34)
y += 4
bf = font(SERIF, 18)
y = text_block(d, MX, y, wrap(d, "A huge fire at a Bangkok oil refinery left several people "
                                  "injured. Operator Bangchak shut all units at the plant.",
                              bf, CW), bf, leading=23)
y += 8
d.line([(MX, y), (W - MX, y)], fill=INK, width=1)
y += 4

# ---- Briefs ----
brief_f = font(SANS, 16)
briefs = [
    "CHESS — Gukesh and Sindarov play out a marathon draw in Game 3 of the World Chess Championship.",
    "BRITAIN — Net migration falls to its lowest level since 1997.",
]
for b in briefs:
    d.text((MX + 14, y), "•", font=brief_f, fill=RED)
    y = text_block(d, MX + 34, y, wrap(d, b, brief_f, CW - 30), brief_f, leading=20)
    y += 2
y += 2
d.line([(MX, y), (W - MX, y)], fill=INK, width=1)
y += 6
foot_f = font(SANS, 15)
text_block(d, MX, y, ["THE WORLD TODAY  •  27 NOVEMBER 2026  •  All stories as reported on the day."],
           foot_f, fill=GREY, align="center", max_w=CW)

img.save("entry.png", "JPEG", quality=88, optimize=True)
print("saved entry.png", img.size, "final y:", y)
