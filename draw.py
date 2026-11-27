#!/usr/bin/env python3
"""Render THE WORLD TODAY front page for Friday, 27 November 2026.

Draws the whole page with Pillow and writes it to entry.png (JPEG bytes,
1024x1024). The page is deterministic: the same script always paints the
same pixels, so two runs produce identical files.
"""
from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
PAPER_RGB = (247, 243, 232)
INK_RGB = (18, 18, 18)
ACCENT_RGB = (178, 34, 34)
MUTED_RGB = (90, 88, 80)

FONTS = {
    "serif_b": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "serif_i": "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    "sans_b": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
}


def load_font(kind, size):
    return ImageFont.truetype(FONTS[kind], size)


def wrap_text(canvas, text, fnt, width):
    """Split text into lines that fit width, measured with fnt."""
    out, current = [], ""
    for word in text.split():
        candidate = (current + " " + word).strip()
        if canvas.textlength(candidate, font=fnt) <= width:
            current = candidate
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def paint_lines(canvas, x, y, lines, fnt, fill=INK_RGB, leading=None,
                centered=False, width=None):
    """Paint lines top to bottom; returns the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.25)
    for line in lines:
        if centered:
            lx = x + (width - canvas.textlength(line, font=fnt)) / 2
        else:
            lx = x
        canvas.text((lx, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fit_font(canvas, text, kind, start, width):
    size = start
    while size > 10:
        fnt = load_font(kind, size)
        if canvas.textlength(text, font=fnt) <= width:
            return fnt
        size -= 2
    return load_font(kind, 10)


def rule(canvas, y, left, right, weight=1):
    canvas.line([(left, y), (right, y)], fill=INK_RGB, width=weight)


def paint_facility_panel(width, height):
    """A refinery at dusk: gradient sky, sun, tanks, columns, one struck
    column in flames, smoke, and a drone silhouette overhead."""
    panel = Image.new("RGB", (width, height), PAPER_RGB)
    p = ImageDraw.Draw(panel)
    top_rgb, bot_rgb = (28, 36, 66), (226, 122, 48)
    for row in range(height):
        t = row / height
        shade = tuple(int(top_rgb[i] + (bot_rgb[i] - top_rgb[i]) * t)
                       for i in range(3))
        p.line([(0, row), (width, row)], fill=shade)
    p.ellipse([60, 16, 118, 74], fill=(255, 214, 120))
    dark = (24, 22, 26)
    ground_y = height - 30
    for tx, tw in [(30, 120), (170, 140), (640, 130)]:
        p.rectangle([tx, ground_y - 56, tx + tw, ground_y], fill=dark)
        p.ellipse([tx, ground_y - 66, tx + tw, ground_y - 46], fill=dark)
    for tx, th, tw in [(360, 100, 42), (420, 112, 34), (800, 95, 38)]:
        p.rectangle([tx, ground_y - th, tx + tw, ground_y], fill=dark)
        p.ellipse([tx, ground_y - th - 10, tx + tw, ground_y - th + 10],
                  fill=dark)
    fx = 420
    p.polygon([(fx - 6, ground_y - 112), (fx + 40, ground_y - 112),
               (fx + 17, ground_y - 136)], fill=(255, 140, 20))
    p.polygon([(fx + 4, ground_y - 112), (fx + 30, ground_y - 112),
               (fx + 17, ground_y - 128)], fill=(255, 215, 80))
    for cx, cy, r in [(494, 28, 17), (520, 16, 13), (820, 34, 18),
                      (846, 22, 16)]:
        p.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 146, 140))
    dx, dy = 690, 48
    p.ellipse([dx - 34, dy - 8, dx + 34, dy + 8], fill=dark)
    p.ellipse([dx - 6, dy - 22, dx + 6, dy - 10], fill=dark)
    p.line([(dx - 52, dy - 16), (dx - 16, dy - 10)], fill=dark, width=4)
    p.line([(dx + 16, dy - 10), (dx + 52, dy - 16)], fill=dark, width=4)
    p.ellipse([dx - 58, dy - 22, dx - 34, dy - 12], fill=(200, 200, 200))
    p.ellipse([dx + 34, dy - 22, dx + 58, dy - 12], fill=(200, 200, 200))
    p.rectangle([0, ground_y, width, height], fill=(16, 20, 30))
    p.line([(16, ground_y + 20), (width - 16, ground_y + 20)],
           fill=(90, 110, 140), width=2)
    return panel


def paint_column(canvas, x, y, width, kicker, headline, body):
    """One column story: red kicker, bold headline, body text."""
    kicker_font = load_font("sans_b", 20)
    canvas.text((x, y), kicker, font=kicker_font, fill=ACCENT_RGB)
    y += 26
    head_font = load_font("serif_b", 26)
    y = paint_lines(canvas, x, y,
                    wrap_text(canvas, headline, head_font, width),
                    head_font, leading=31)
    y += 4
    body_font = load_font("serif", 17)
    y = paint_lines(canvas, x, y,
                    wrap_text(canvas, body, body_font, width),
                    body_font, leading=22)
    return y


def main():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER_RGB)
    d = ImageDraw.Draw(page)
    d.rectangle([12, 12, PAGE_W - 13, PAGE_H - 13], outline=INK_RGB, width=2)
    margin = 48
    content_w = PAGE_W - 2 * margin
    right = PAGE_W - margin

    # Masthead
    y = 22
    masthead = fit_font(d, "THE WORLD TODAY", "serif_b", 70, content_w)
    y = paint_lines(d, margin, y, ["THE WORLD TODAY"], masthead,
                    centered=True, width=content_w)
    y += 4
    rule(d, y, margin, right, 3)
    y += 6
    rule(d, y, margin, right, 1)
    y += 10
    date_font = load_font("sans_b", 26)
    y = paint_lines(d, margin, y, ["FRIDAY, 27 NOVEMBER 2026"], date_font,
                    centered=True, width=content_w)
    y += 6
    rule(d, y, margin, right, 1)
    y += 10

    # Lead story: Kuwait drone strike
    kicker_font = load_font("sans_b", 20)
    d.text((margin, y), "MIDDLE EAST", font=kicker_font, fill=ACCENT_RGB)
    y += 28
    lead_font = load_font("serif_b", 42)
    y = paint_lines(d, margin, y,
                    wrap_text(d, "TWO ITALIANS KILLED IN DRONE STRIKE ON "
                                 "KUWAIT FACILITY", lead_font, content_w),
                    lead_font, leading=48)
    y += 6

    # Illustration panel
    panel_w, panel_h = content_w, 170
    panel = paint_facility_panel(panel_w, panel_h)
    page.paste(panel, (margin, y))
    d.rectangle([margin, y, margin + panel_w, y + panel_h],
                outline=INK_RGB, width=2)
    y = y + panel_h + 6
    caption_font = load_font("serif_i", 16)
    y = paint_lines(d, margin, y,
                    ["An Iranian drone strike hit a facility in Kuwait, "
                     "killing two Italians."],
                    caption_font, fill=MUTED_RGB)
    y += 5
    lead_body_font = load_font("serif", 20)
    y = paint_lines(d, margin, y,
                    wrap_text(d, "Two Italians were killed when an Iranian "
                                 "drone struck a facility in Kuwait, in a "
                                 "sharp escalation in the Gulf. Tehran denies "
                                 "responsibility.", lead_body_font, content_w),
                    lead_body_font, leading=25)
    y += 8
    rule(d, y, margin, right, 1)
    y += 10

    # Two columns: Gaza | Thanksgiving storm
    col_w = 452
    col2_x = margin + col_w + 24
    top_y = y
    ends = []
    ends.append(paint_column(
        d, margin, top_y, col_w, "GAZA",
        "HAMAS WEIGHS RESPONSE AFTER ISRAEL KILLS 10 IN GAZA",
        "Hamas is weighing its response after Israeli strikes killed 10 "
        "people in Gaza, in a fresh test of the fragile ceasefire."))
    ends.append(paint_column(
        d, col2_x, top_y, col_w, "UNITED STATES",
        "THANKSGIVING STORM FLOODS CITIES, DELAYS FLIGHTS",
        "A major storm brought flooding and flight delays across the United "
        "States on Thanksgiving, and New York declared a state of "
        "emergency."))
    y = max(ends) + 8
    rule(d, y, margin, right, 1)
    y += 10

    # Full-width story: Bangkok refinery fire
    d.text((margin, y), "THAILAND", font=kicker_font, fill=ACCENT_RGB)
    y += 26
    story_font = load_font("serif_b", 29)
    y = paint_lines(d, margin, y,
                    wrap_text(d, "MASSIVE FIRE AT BANGKOK REFINERY INJURES "
                                 "SEVERAL", story_font, content_w),
                    story_font, leading=34)
    y += 4
    story_body = load_font("serif", 18)
    y = paint_lines(d, margin, y,
                    wrap_text(d, "A huge fire at a Bangkok oil refinery left "
                                 "several people injured. Operator Bangchak "
                                 "shut all units at the plant.",
                              story_body, content_w),
                    story_body, leading=23)
    y += 8
    rule(d, y, margin, right, 1)
    y += 4

    # Briefs
    brief_font = load_font("sans", 16)
    briefs = [
        "CHESS — Gukesh and Sindarov play out a marathon draw in Game 3 "
        "of the World Chess Championship.",
        "BRITAIN — Net migration falls to its lowest level since 1997.",
    ]
    for brief in briefs:
        d.text((margin + 14, y), "•", font=brief_font, fill=ACCENT_RGB)
        y = paint_lines(d, margin + 34, y,
                        wrap_text(d, brief, brief_font, content_w - 30),
                        brief_font, leading=20)
        y += 2
    y += 2
    rule(d, y, margin, right, 1)
    y += 6
    foot_font = load_font("sans", 15)
    paint_lines(d, margin, y,
                ["THE WORLD TODAY  •  27 NOVEMBER 2026  •  All stories as "
                 "reported on the day."],
                foot_font, fill=MUTED_RGB, centered=True, width=content_w)

    page.save("entry.png", "JPEG", quality=88, optimize=True)
    print("saved entry.png", page.size, "final y:", y)


main()
