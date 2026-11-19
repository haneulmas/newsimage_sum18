"""Build the fixed edition offline; the contest entrypoint only copies its bytes."""

from pathlib import Path
import struct
import zlib

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SIZE = 1024
SCALE = 2
COLORS = {
    "paper": "#F3EEE2", "ink": "#14202E", "grey": "#5B6470",
    "rule": "#B9B2A2", "amber": "#A8741A", "red": "#A33A32",
    "teal": "#2F6F6A",
}
FONTS = {
    "headline": "LibreCaslonText-Bold.ttf",
    "label": "Inter-Bold.ttf",
    "body": "Inter-Regular.ttf",
}
BRIEFS = (
    ("ASIA–PACIFIC", ("APEC leaders", "gather in", "Shenzhen"),
     "Xi chairs, 18–19 Nov", "skyline", "amber"),
    ("MARKETS", ("Wall Street falls", "for a fifth day"),
     "Brent $91.95 (−1.3%)", "markets", "red"),
    ("RUSSIA–UKRAINE", ("Drone strikes", "curb Russian", "refining"),
     "Sources: 15/35 disrupted in Nov", "refinery", "red"),
    ("CLIMATE", ("COP31 talks", "enter final days", "in Antalya"),
     "18 Nov: second draft due", "globe", "teal"),
)


class Page:
    def __init__(self):
        self.image = Image.new("RGB", (SIZE * SCALE, SIZE * SCALE), COLORS["paper"])
        self.draw = ImageDraw.Draw(self.image)
        self.fonts = {}

    def font(self, face, size):
        key = (face, size)
        if key not in self.fonts:
            self.fonts[key] = ImageFont.truetype(
                str(ROOT / "assets" / "fonts" / FONTS[face]), round(size * SCALE),
                layout_engine=ImageFont.Layout.BASIC,
            )
        return self.fonts[key]

    def text(self, value, x, baseline, size, face="body", color="ink", width=None):
        font = self.font(face, size)
        point = (round(x * SCALE), round(baseline * SCALE))
        bounds = self.draw.textbbox(point, value, font=font, anchor="ls")
        if min(bounds[:2]) < 0 or max(bounds[2:]) > SIZE * SCALE:
            raise ValueError(f"Text outside canvas: {value}")
        if width is not None and bounds[2] > (x + width) * SCALE:
            raise ValueError(f"Text exceeds column: {value}")
        self.draw.text(point, value, font=font, anchor="ls", fill=COLORS[color])

    def rect(self, bounds, color):
        self.draw.rectangle(tuple(round(v * SCALE) for v in bounds), fill=COLORS[color])

    def line(self, points, color="rule", width=1):
        self.draw.line([(round(x * SCALE), round(y * SCALE)) for x, y in points],
                       fill=COLORS[color], width=max(1, round(width * SCALE)), joint="curve")

    def polygon(self, points, color="ink"):
        self.draw.polygon([(round(x * SCALE), round(y * SCALE)) for x, y in points],
                          fill=COLORS[color])

    def ellipse(self, bounds, color, width=None):
        box = tuple(round(v * SCALE) for v in bounds)
        if width is None:
            self.draw.ellipse(box, fill=COLORS[color])
        else:
            self.draw.ellipse(box, outline=COLORS[color], width=round(width * SCALE))


def tanker(page, x, y):
    # Maritime context, not a claim that a vessel burned on the edition date.
    page.polygon([(x, y + 69), (x + 169, y + 69), (x + 147, y + 103), (x + 24, y + 103)])
    page.rect((x + 11, y + 43, x + 133, y + 62), "ink")
    page.rect((x + 112, y + 18, x + 144, y + 62), "ink")
    page.rect((x + 117, y + 25, x + 137, y + 34), "paper")
    page.line([(x + 130, y + 18), (x + 130, y + 4)], "ink", 3)
    page.line([(x + 14, y + 116), (x + 155, y + 116)], "teal", 4)
    page.line([(x + 35, y + 128), (x + 135, y + 128)], "teal", 3)


def motif(page, name, x, y, accent):
    if name == "skyline":
        page.rect((x + 1, y + 51, x + 22, y + 94), "ink")
        page.rect((x + 61, y + 35, x + 83, y + 94), "ink")
        page.polygon([(x + 31, y + 94), (x + 31, y + 29), (x + 44, y + 1),
                      (x + 54, y + 29), (x + 54, y + 94)])
        page.line([(x + 44, y + 15), (x + 44, y + 81)], accent, 3)
        page.line([(x - 3, y + 97), (x + 88, y + 97)], "ink", 3)
    elif name == "markets":
        # A direction symbol, with no invented price points, dates or axis values.
        page.line([(x + 3, y + 6), (x + 3, y + 93), (x + 86, y + 93)], "ink", 3)
        page.line([(x + 14, y + 19), (x + 38, y + 43), (x + 54, y + 36),
                   (x + 80, y + 73)], accent, 6)
        page.line([(x + 61, y + 72), (x + 80, y + 73), (x + 80, y + 54)], accent, 6)
    elif name == "refinery":
        page.rect((x + 8, y + 21, x + 26, y + 91), "ink")
        page.rect((x + 48, y + 3, x + 68, y + 91), "ink")
        for offset in (19, 43, 67):
            page.rect((x + 44, y + offset, x + 72, y + offset + 5), accent)
        page.line([(x + 26, y + 51), (x + 37, y + 51), (x + 37, y + 77),
                   (x + 48, y + 77)], "ink", 5)
        page.line([(x, y + 95), (x + 85, y + 95)], "ink", 4)
    elif name == "globe":
        page.ellipse((x, y + 7, x + 88, y + 95), accent, 4)
        page.ellipse((x + 22, y + 7, x + 66, y + 95), accent, 3)
        page.line([(x + 3, y + 51), (x + 85, y + 51)], accent, 3)
        page.line([(x + 10, y + 28), (x + 78, y + 28)], accent, 3)
        page.line([(x + 10, y + 74), (x + 78, y + 74)], accent, 3)
    else:
        raise ValueError(f"Unknown story motif: {name}")


def compose():
    page = Page()
    page.text("The Global Ledger", 34, 43, 32, "headline")
    page.text("WORLD NEWS", 809, 40, 24, "label", "grey", 181)
    page.rect((0, 64, 1024, 275), "ink")
    page.text("WEDNESDAY", 34, 135, 64, "label", "paper")
    page.text("18 NOVEMBER 2026", 34, 215, 74, "headline", "paper", 956)
    page.text("World news of 18 Nov 2026", 36, 258, 30, "body", "paper")

    page.text("GULF / STRAIT OF HORMUZ", 34, 310, 30, "label", "grey")
    page.text("Iran widens attacks to", 34, 372, 54, "headline", width=750)
    page.text("Kuwait and Bahrain", 34, 434, 54, "headline", width=750)
    page.text("Kuwait reports intercepted drones; Bahrain issues two alerts.",
              34, 488, 30, width=956)
    tanker(page, 810, 319)
    page.line([(34, 515), (990, 515)], width=1.5)

    page.line([(512, 538), (512, 981)])
    page.line([(34, 756), (990, 756)])
    for i, (category, headline, support, symbol, accent) in enumerate(BRIEFS):
        x = 34 if i % 2 == 0 else 546
        label_y = 548 if i < 2 else 790
        page.text(category, x, label_y, 24, "label", "grey")
        motif(page, symbol, x, label_y + 29, accent)
        for row, line in enumerate(headline):
            page.text(line, x + 108, label_y + 50 + row * 44, 40, "headline", width=336)
        page.text(support, x, label_y + 182, 30, width=456)

    page.line([(34, 994), (990, 994)])
    page.text("Sources: AP, Reuters, ANTARA, Khaleej Times, Report.az, UNFCCC",
              34, 1017, 16, color="grey", width=956)
    return page.image.resize((SIZE, SIZE), Image.Resampling.LANCZOS)


def rgb(hex_color):
    return tuple(bytes.fromhex(hex_color[1:]))


def indexed(image):
    paper = rgb(COLORS["paper"])
    palette = [paper]
    for name in ("ink", "grey", "rule", "amber", "red", "teal"):
        foreground = rgb(COLORS[name])
        for step in range(1, 33):
            palette.append(tuple((back * (32 - step) + front * step + 16) // 32
                                 for back, front in zip(paper, foreground)))
    palette.extend([paper] * (256 - len(palette)))
    reference = Image.new("P", (1, 1))
    flat = bytes(channel for color in palette for channel in color)
    reference.putpalette(flat)
    result = image.quantize(palette=reference, dither=Image.Dither.NONE)
    return result.tobytes(), flat


def chunk(kind, data):
    payload = kind + data
    return struct.pack(">I", len(data)) + payload + struct.pack(">I", zlib.crc32(payload) & 0xFFFFFFFF)


def encode_png(pixels, palette):
    rows = b"".join(b"\x00" + pixels[y * SIZE:(y + 1) * SIZE] for y in range(SIZE))
    header = struct.pack(">IIBBBBB", SIZE, SIZE, 8, 3, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"PLTE", palette)
            + chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b""))


def main():
    pixels, palette = indexed(compose())
    png = encode_png(pixels, palette)
    if len(png) >= 200_000:
        raise ValueError("Palette PNG must remain below the 200 KB development target")
    (ROOT / "assets" / "entry.png").write_bytes(png)


if __name__ == "__main__":
    main()
