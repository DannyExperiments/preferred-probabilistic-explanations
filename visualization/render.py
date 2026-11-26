"""Build the rotating exact-support illustration and offline explorer ZIP."""

import math
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
W, H = 704, 835
BG, PANEL = "#101b32", "#162640"
TEXT, MUTED = "#f7faff", "#b8c7de"
MINT, AMBER, RED = "#6aead7", "#ffcf83", "#ffb8ae"
NAMES = ("s", "a1", "b1", "a2", "b2")


def label(draw, xy, msg, size, color=TEXT, anchor="lt"):
    draw.text(xy, msg, font=ImageFont.load_default(size=size), fill=color, anchor=anchor)


def survivors(mask):
    return ([0] if mask == 0 else []) + [j + 1 for j in range(4) if not (mask & (1 << j))]


def polygons(x, y):
    top = [(x - 25, y - 49), (x, y - 63), (x + 25, y - 49), (x, y - 35)]
    left = [top[0], top[3], (x, y), (x - 25, y - 14)]
    right = [top[3], top[2], (x + 25, y - 14), (x, y)]
    return left, right, top


def support(draw, angle, mask):
    kept = survivors(mask)
    assert len(kept) == (5 if not mask else 4 - bin(mask).count("1"))
    points = []
    for j in range(5):
        th = angle + j * (2 * math.pi / 5)
        points.append((352 + 205 * math.cos(th), 430 + 99 * math.sin(th), j))
    assert all(abs(x - a) >= 54 or abs(y - b) >= 90
               for j, (x, y, _) in enumerate(points) for a, b, _ in points[:j])
    draw.polygon([(x, y) for x, y, _ in points], fill="#1b3150", outline="#486484", width=2)
    for x, y, j in sorted(points, key=lambda point: point[1]):
        if j in kept:
            colors = ("#349c9a", "#257176", MINT) if j else ("#ae7545", "#785e50", AMBER)
        else:
            colors = ("#334360", "#2b3753", "#647491") if j else ("#53475a", "#433c53", "#9d806e")
        for poly, color in zip(polygons(x, y), colors):
            draw.polygon(poly, fill=color, outline="#16243b")
        label(draw, (x, y + 10), NAMES[j], 23, TEXT if j in kept else MUTED, "mt")


def frame(angle, step):
    cases = (
        (1, "a1 only", "Fails entailment", RED, ("No selector from pair 2.", "A valuation can omit that pair.")),
        (9, "a1 and b2", "Defeats the fallback", MINT, ("One selector from each pair.", "The observation follows.")),
        (7, "a1, b1 and a2", "Ties the fallback", AMBER, ("A doubled pair makes it valid.", "Only one point survives.")),
    )
    mask, term, conclusion, color, notes = cases[step]
    image = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(image)
    label(d, (36, 42), "PROBABILISTIC ABDUCTION", 24, MINT)
    label(d, (34, 85), "Can this term win?", 62)
    label(d, (36, 169), "Five support points, each of mass 1/5.", 28, MUTED)
    d.rounded_rectangle((32, 227, 672, 575), 21, fill=PANEL, outline="#304463", width=2)
    label(d, (55, 256), "BRIGHT POINTS SURVIVE", 22, MUTED)
    support(d, angle, mask)
    d.rounded_rectangle((32, 597, 672, 803), 21, fill=PANEL, outline="#304463", width=2)
    label(d, (56, 619), term, 32)
    label(d, (645, 619), f"{len(survivors(mask))}/5 vs 1/5", 31, color, "rt")
    label(d, (56, 666), conclusion, 33, color)
    label(d, (56, 718), notes[0], 27, MUTED)
    label(d, (56, 754), notes[1], 27, MUTED)
    return image.convert("P", palette=Image.Palette.ADAPTIVE, colors=64)


def main():
    total = 72
    frames = [frame(2 * math.pi * (i / total + .035), i // 24) for i in range(total)]
    frames[0].save(HERE / "support-comparison.gif", save_all=True, append_images=frames[1:],
                   loop=0, duration=170, optimize=True)
    files = {"index.html": (HERE / "index.html").read_bytes(),
             "README.md": (HERE / "README.md").read_bytes()}
    with ZipFile(HERE / "support-comparison-explorer.zip", "w") as archive:
        for name in sorted(files):
            info = ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, files[name], ZIP_DEFLATED, compresslevel=9)


if __name__ == "__main__":
    main()
