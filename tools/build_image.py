"""Render a fixed news atlas offline; main.py copies the resulting PNG bytes."""

from pathlib import Path
import json
import struct
import zlib

from PIL import Image, ImageDraw, ImageFont

from pictograms import draw_pictogram


ROOT = Path(__file__).resolve().parents[1]
SIZE = 1024
SCALE = 2
COLORS = {
    "paper": "#F3EEE2", "ink": "#14202E", "grey": "#505660",
    "rule": "#B8B1A4", "asia": "#63517C", "mideast": "#A1443F",
    "europe": "#365C7E", "americas": "#466848", "space": "#20344B",
    "markets": "#805719", "africa": "#7C583D", "climate": "#31685E",
}
FONTS = {"headline": "Inter-Bold.ttf", "label": "Nunito.ttf", "body": "Inter-Regular.ttf"}
LEADS = (
    ("asia", "ASIA / SHENZHEN / APEC", "diplomacy",
     ("Trump meets", "Xi, Putin"),
     ("Xi greets Trump on the tarmac.", "Trump and Putin shake hands.",
      "Trilateral: scheduled 19 Nov.")),
    ("mideast", "MIDDLE EAST / GULF", "gulf",
     ("Iran widens", "Gulf attacks"),
     ("Kuwait: drones intercepted.", "Bahrain: two shelter alerts.",
      "After US strike on 17 Nov.")),
    ("space", "SPACE / NASA", "voyager",
     ("Voyager 1", "one light-day"),
     ("First human-made object.", "25.9 billion km from Earth.",
      "Radio: 24 hours each way.")),
)
CARDS = (
    ("markets", "US / FED", "fed", ("Fed minutes", "signal more", "rate hikes"),
     "Dow −561; S&P: fifth daily loss"),
    ("europe", "EUROPE / UKRAINE", "loan", ("EU proposes", "€45bn loan", "for Ukraine"),
     "For 2027; approval still needed"),
    ("europe", "RUSSIA / ENERGY", "refinery", ("15 refineries", "disrupted by", "drone strikes"),
     "15 of 35 in November: sources"),
    ("climate", "TÜRKIYE / COP31", "climate", ("COP31 talks", "near their", "deadline"),
     "Antalya; second draft due today"),
    ("asia", "CHINA / APEC BUSINESS", "business", ("Prabowo", "arrives", "for APEC"),
     "Shenzhen CEO Summit: 17–18 Nov"),
    ("asia", "INDIA / BAY OF BENGAL", "cyclone", ("Akvan", "intensifies", "off India"),
     "Landfall forecast for 20 Nov"),
    ("africa", "SUDAN / NEW REPORT", "sudan", ("Amnesty:", "RSF drones", "killed civilians"),
     "El Obeid: earlier civilian deaths"),
    ("markets", "US / TECHNOLOGY", "ipo", ("Anthropic IPO", "priced at", "$83 a share"),
     "Trading scheduled for 19 Nov"),
)

# Every brief has a dated reference in SOURCES.md; cumulative figures stay attributed.
ALSO = (
    ("americas", "US Democrats nominate Jeffries for Speaker"),
    ("mideast", "Witnesses: tanks push into central Gaza"),
    ("americas", "Hegseth meets Venezuela's interim leader"),
    ("americas", "Brazil Senate approves fiscal package"),
    ("europe", "UK reports October inflation at 3.6%"),
    ("asia", "IAEA reports Yongbyon enrichment expansion"),
    ("asia", "Myanmar to review ASEAN relationship"),
    ("africa", "Ethiopia–Eritrea border buildup reported"),
    ("mideast", "UNICEF reports child casualties in Yemen"),
    ("africa", "S. Africa aid groups warn of HIV/TB care gaps"),
    ("europe", "Vatican marks St Peter's 400th anniversary"),
    ("americas", "Ecuador receives NY collapse victim's remains"),
    ("asia", "Trump meets Marcos in Manila"),
    ("climate", "Indonesia unveils blue-carbon revenue rules"),
    ("americas", "Carney meets Trump at APEC"),
    ("mideast", "ADNOC reports 17 Nov vessel attack"),
)


class Page:
    def __init__(self):
        self.image = Image.new("RGB", (SIZE * SCALE, SIZE * SCALE), COLORS["paper"])
        self.draw = ImageDraw.Draw(self.image)
        self.fonts = {}
        self.text_bounds = []

    def color(self, value):
        return COLORS.get(value, value)

    def font(self, face, size):
        key = (face, size)
        if key not in self.fonts:
            font = ImageFont.truetype(str(ROOT / "assets" / "fonts" / FONTS[face]),
                                      round(size * SCALE), layout_engine=ImageFont.Layout.BASIC)
            if face == "label":
                font.set_variation_by_axes([750])
            self.fonts[key] = font
        return self.fonts[key]

    def text(self, value, x, baseline, size, face="body", color="ink", width=None):
        font = self.font(face, size)
        point = (round(x * SCALE), round(baseline * SCALE))
        bounds = self.draw.textbbox(point, value, font=font, anchor="ls")
        if min(bounds[:2]) < 0 or max(bounds[2:]) > SIZE * SCALE:
            raise ValueError(f"Text outside canvas: {value}")
        if width is not None and bounds[2] > (x + width) * SCALE:
            raise ValueError(f"Text exceeds column: {value}")
        self.text_bounds.append((value, tuple(v / SCALE for v in bounds)))
        self.draw.text(point, value, font=font, anchor="ls", fill=self.color(color))

    def rect(self, bounds, color):
        self.draw.rectangle(tuple(round(v * SCALE) for v in bounds), fill=self.color(color))

    def line(self, points, color="rule", width=1):
        self.draw.line([(round(x * SCALE), round(y * SCALE)) for x, y in points],
                       fill=self.color(color), width=max(1, round(width * SCALE)), joint="curve")

    def polygon(self, points, color="ink"):
        self.draw.polygon([(round(x * SCALE), round(y * SCALE)) for x, y in points],
                          fill=self.color(color))

    def ellipse(self, bounds, color, width=None):
        box = tuple(round(v * SCALE) for v in bounds)
        if width is None:
            self.draw.ellipse(box, fill=self.color(color))
        else:
            self.draw.ellipse(box, outline=self.color(color), width=max(1, round(width * SCALE)))

    def check_text_collisions(self):
        for index, (text, a) in enumerate(self.text_bounds):
            for other, b in self.text_bounds[index + 1:]:
                if min(a[2], b[2]) - max(a[0], b[0]) > .5 and min(a[3], b[3]) - max(a[1], b[1]) > .5:
                    raise ValueError(f"Text collision: {text!r} and {other!r}")


def header(page):
    page.rect((0, 0, SIZE, 187), "ink")
    page.text("WEDNESDAY", 20, 80, 84, "headline", "paper", 984)
    page.text("18 NOVEMBER 2026", 20, 170, 84, "headline", "paper", 984)
    page.text("Everything here happened, or was first reported, on 18 Nov 2026",
              20, 213, 25, width=984)
    x = 20
    for name, title in (("asia", "Asia"), ("mideast", "Middle East"), ("europe", "Europe"),
                        ("americas", "Americas"), ("space", "Space"), ("markets", "Markets"),
                        ("africa", "Africa"), ("climate", "Climate / health")):
        page.rect((x, 225, x + 8, 233), name)
        page.text(title, x + 13, 234, 13, "label")
        x += {"asia": 72, "mideast": 118, "europe": 88, "americas": 106,
              "space": 83, "markets": 96, "africa": 80, "climate": 145}[name]


def lead_panels(page):
    for index, (region, tag, icon, headline, support) in enumerate(LEADS):
        x = 20 + index * 332
        page.rect((x, 250, x + 320, 536), region)
        page.text(tag, x + 14, 273, 13.5, "label", "paper", 292)
        page.rect((x + 14, 282, x + 306, 386), "paper")
        draw_pictogram(page, icon, (x + 19, 283, x + 301, 384), region)
        for row, line in enumerate(headline):
            page.text(line, x + 14, 427 + row * 46, 44, "headline", "paper", 292)
        for row, line in enumerate(support):
            page.text(line, x + 14, 498 + row * 16.5, 15.5, color="paper", width=292)


def story_cards(page):
    for index, (region, tag, icon, headline, support) in enumerate(CARDS):
        x = 20 + (index % 4) * 249
        y = 552 + (index // 4) * 128
        page.line([(x, y), (x + 237, y)], region, 4)
        page.text(tag, x, y + 20, 12.5, "label", region, 237)
        draw_pictogram(page, icon, (x, y + 39, x + 50, y + 89), region)
        for row, line in enumerate(headline):
            page.text(line, x + 62, y + 46 + row * 24, 22, "headline", width=175)
        page.text(support, x, y + 111, 12.3, width=237)


def where_map(page):
    x, y, w, h = 775, 850, 229, 106
    page.text("WHERE IT HAPPENED", x, 831, 16, "label", width=w)
    # Equirectangular silhouettes are schematic, not administrative boundaries.
    continents = (
        [(-168, 66), (-130, 72), (-105, 67), (-81, 49), (-60, 48), (-81, 25),
         (-86, 9), (-105, 22), (-125, 44), (-156, 58)],
        [(-81, 12), (-51, 4), (-35, -8), (-51, -30), (-68, -55), (-78, -16)],
        [(-12, 35), (12, 37), (33, 29), (48, 7), (32, -33), (14, -35), (-6, 2)],
        [(-10, 36), (-8, 58), (27, 71), (69, 71), (111, 75), (170, 61),
         (141, 36), (122, 23), (109, -5), (87, 9), (77, 27), (52, 12), (30, 30)],
        [(113, -14), (138, -11), (153, -28), (140, -40), (115, -33)],
        [(-54, 59), (-19, 64), (-26, 81), (-48, 81)],
    )

    def project(lon, lat):
        return x + (lon + 180) / 360 * w, y + (82 - lat) / 140 * h

    for polygon in continents:
        page.polygon([project(lon, lat) for lon, lat in polygon], "#D5CFC2")
    locations = ((114, 23, "asia"), (121, 15, "asia"), (85, 18, "asia"),
                 (48, 29, "mideast"), (50, 26, "mideast"), (35, 39, "climate"),
                 (31, 49, "europe"), (38, 56, "europe"), (30, 13, "africa"),
                 (28, -26, "africa"), (12, 42, "europe"), (107, -6, "climate"),
                 (-77, 39, "americas"), (-122, 38, "markets"), (-67, 10, "americas"),
                 (-48, -16, "americas"), (-78, -1, "americas"))
    for lon, lat, region in locations:
        px, py = project(lon, lat)
        page.ellipse((px - 2.4, py - 2.4, px + 2.4, py + 2.4), region)
    page.text("Schematic locations; space off-map", x, 966, 11, width=w)


def briefs(page):
    page.line([(20, 806), (1004, 806)], "ink", 1.5)
    page.text("ALSO ON 18 NOVEMBER", 20, 831, 18, "headline", width=735)
    for index, (region, value) in enumerate(ALSO):
        x = 20 if index < 8 else 397
        baseline = 853 + (index % 8) * 15.4
        page.rect((x, baseline - 6, x + 4, baseline - 2), region)
        page.text(value, x + 10, baseline, 12.5, width=350)
    where_map(page)
    page.rect((0, 978, SIZE, SIZE), "ink")
    page.text("DATE CHECK", 20, 995, 13, "label", "paper", 107)
    page.text("17 Nov or earlier: Nvidia results; Qeshm strike.",
              136, 995, 12, color="paper", width=868)
    page.text("Not yet on Wednesday: trilateral results (talks 19 Nov); Akvan landfall (forecast 20 Nov).",
              20, 1014, 12, color="paper", width=984)


def compose():
    page = Page()
    header(page)
    lead_panels(page)
    story_cards(page)
    briefs(page)
    page.check_text_collisions()
    return page


def chunk(kind, data):
    payload = kind + data
    return struct.pack(">I", len(data)) + payload + struct.pack(">I", zlib.crc32(payload) & 0xFFFFFFFF)


def encode_png(image):
    palette = [tuple(bytes.fromhex(COLORS["paper"][1:]))]
    paper = palette[0]
    for name in tuple(COLORS)[1:] + ("#D5CFC2",):
        front = tuple(bytes.fromhex(COLORS.get(name, name)[1:]))
        for step in range(1, 20):
            palette.append(tuple((back * (19 - step) + fore * step + 9) // 19
                                 for back, fore in zip(paper, front)))
    palette.extend([paper] * (256 - len(palette)))
    reference = Image.new("P", (1, 1))
    flat = bytes(channel for color in palette for channel in color)
    reference.putpalette(flat)
    reduced = image.resize((SIZE, SIZE), Image.Resampling.LANCZOS).quantize(
        palette=reference, dither=Image.Dither.NONE)
    pixels = reduced.tobytes()
    rows = b"".join(b"\x00" + pixels[y * SIZE:(y + 1) * SIZE] for y in range(SIZE))
    header_bytes = struct.pack(">IIBBBBB", SIZE, SIZE, 8, 3, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header_bytes) + chunk(b"PLTE", flat)
            + chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b""))


def main():
    page = compose()
    png = encode_png(page.image)
    if len(png) >= 400_000:
        raise ValueError("PNG must remain below the 400 KB development target")
    (ROOT / "assets" / "entry.png").write_bytes(png)
    cap = page.font("headline", 84).getbbox("H")
    print(json.dumps({"bytes": len(png), "lead_stories": len(LEADS),
                      "cards": len(CARDS), "briefs": len(ALSO),
                      "date_cap_height_px": (cap[3] - cap[1]) / SCALE,
                      "text_boxes_checked": len(page.text_bounds)}))


if __name__ == "__main__":
    main()
