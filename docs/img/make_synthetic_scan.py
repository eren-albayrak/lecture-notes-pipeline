"""Generate the synthetic "handwritten scan" used in the README (docs/img/synthetic_scan.jpg).

The content is written for this example; it is not taken from any lecturer's notes.
A handwriting-style font, character jitter, a slight rotation, paper tint and noise make it
look like a scanned page.

Usage:
    python -I docs/img/make_synthetic_scan.py <handwriting_font.ttf> <symbol_font> <out.jpg>
    e.g. on Windows: C:/Windows/Fonts/Inkfree.ttf  C:/Windows/Fonts/cambria.ttc

Mini markup in LINES: ^{...} = superscript, § = integral sign, @ = hand-drawn check mark.

Requires: pillow.
"""

import random
import re
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

LINES = [
    "Ör. 1     y' + 2y = 4",
    "lineer:   p(x) = 2 ,   q(x) = 4",
    "    μ = e^{§ 2 dx} = e^{2x}",
    "    (y e^{2x})' = 4 e^{2x}",
    "    y e^{2x} = 2 e^{2x} + C",
    "     =>  y = 2 + C e^{-2x}",
    "kontrol:  -2Ce^{-2x} + 2(2 + Ce^{-2x}) = 4  @",
    "Ör. 2     y' = x y     (ödev)",
]
BOXED = 5


def main(font_path: str, symbol_path: str, out: str) -> None:
    rng = random.Random(7)
    w, h = 1100, 1400
    paper = Image.effect_noise((w, h), 14).filter(ImageFilter.GaussianBlur(1.2)).point(lambda v: 222 + (v - 128) // 10)
    draw = ImageDraw.Draw(paper)
    for y in range(190, h - 120, 66):
        draw.line([(80, y), (w - 60, y)], fill=200, width=1)
    draw.line([(150, 90), (150, h - 80)], fill=205, width=2)

    font = ImageFont.truetype(font_path, 42)
    sup = ImageFont.truetype(font_path, 28)
    integral = ImageFont.truetype(symbol_path, 30)
    small = ImageFont.truetype(font_path, 26)
    draw.text((760, 110), "Synthetic sample", font=small, fill=115)

    y = 176
    for n, line in enumerate(LINES):
        x = 180
        for token in re.split(r"(\^\{[^}]*\})", line):
            raised = token.startswith("^{")
            text, f, dy0 = (token[2:-1], sup, -16) if raised else (token, font, 0)
            for ch in text:
                ink = rng.randint(25, 60)
                dy = dy0 + rng.uniform(-2.5, 2.5)
                if ch == "§":
                    draw.text((x, y + dy - 2), "\u222b", font=integral, fill=ink)
                    x += 20
                    continue
                if ch == "@":
                    draw.line([(x, y + 26), (x + 10, y + 38), (x + 30, y + 6)], fill=ink, width=4)
                    x += 34
                    continue
                draw.text((x, y + dy), ch, font=f, fill=ink)
                x += draw.textlength(ch, font=f) + rng.uniform(-0.8, 1.2)
        if n == BOXED:
            draw.rounded_rectangle([196, y - 30, x + 30, y + 66], 14, outline=55, width=3)
        y += 132

    page = paper.rotate(-1.0, resample=Image.BICUBIC, fillcolor=222)
    page = page.crop((40, 40, w - 40, h - 40)).filter(ImageFilter.GaussianBlur(0.6))
    page = Image.blend(page, Image.effect_noise(page.size, 22), 0.05)
    page.convert("RGB").resize((780, 1036), Image.LANCZOS).save(out, quality=72, optimize=True)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
