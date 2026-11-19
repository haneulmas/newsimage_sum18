"""Small editorial scenes built only from flat geometric primitives."""

from math import cos, pi, sin


class _Scene:
    def __init__(self, page, box, accent, background):
        left, top, right, bottom = box
        if right <= left or bottom <= top:
            raise ValueError("A pictogram needs a positive drawing area")
        self.page = page
        self.scale = min(right - left, bottom - top) / 100
        self.x = left + (right - left - 100 * self.scale) / 2
        self.y = top + (bottom - top - 100 * self.scale) / 2
        self.accent = accent
        self.background = background

    def point(self, x, y):
        return self.x + x * self.scale, self.y + y * self.scale

    def bounds(self, box):
        return (*self.point(*box[:2]), *self.point(*box[2:]))

    def rect(self, box, color="ink"):
        self.page.rect(self.bounds(box), color)

    def ellipse(self, box, color="ink", width=None):
        self.page.ellipse(self.bounds(box), color,
                          None if width is None else width * self.scale)

    def polygon(self, points, color="ink"):
        self.page.polygon([self.point(x, y) for x, y in points], color)

    def line(self, points, color="ink", width=3):
        self.page.line([self.point(x, y) for x, y in points], color,
                       width * self.scale)

    def person(self, x, y, size=1):
        self.ellipse((x - 4 * size, y, x + 4 * size, y + 8 * size))
        self.polygon([(x - 6 * size, y + 11 * size),
                      (x + 6 * size, y + 11 * size),
                      (x + 8 * size, y + 29 * size),
                      (x - 8 * size, y + 29 * size)])
        self.line([(x - 3 * size, y + 27 * size),
                   (x - 4 * size, y + 40 * size)], width=4 * size)
        self.line([(x + 3 * size, y + 27 * size),
                   (x + 4 * size, y + 40 * size)], width=4 * size)

    def globe(self, box):
        self.ellipse(box, self.accent, 3)
        left, top, right, bottom = box
        w, h = right - left, bottom - top
        self.ellipse((left + .28 * w, top, right - .28 * w, bottom),
                     self.accent, 2)
        self.line([(left + 2, top + h / 2), (right - 2, top + h / 2)],
                  self.accent, 2)
        for fraction in (.27, .73):
            self.line([(left + .1 * w, top + fraction * h),
                       (right - .1 * w, top + fraction * h)], self.accent, 2)

    def drone(self, x, y, size=1):
        self.line([(x - 13 * size, y - 8 * size),
                   (x + 13 * size, y + 8 * size)], width=3 * size)
        self.line([(x - 13 * size, y + 8 * size),
                   (x + 13 * size, y - 8 * size)], width=3 * size)
        for dx, dy in ((-13, -8), (-13, 8), (13, -8), (13, 8)):
            self.ellipse((x + (dx - 6) * size, y + (dy - 3) * size,
                          x + (dx + 6) * size, y + (dy + 3) * size),
                         self.accent, 2 * size)
        self.rect((x - 5 * size, y - 4 * size,
                   x + 5 * size, y + 4 * size))


def _diplomacy(s):
    s.polygon([(7, 26), (34, 26), (48, 8), (56, 8), (49, 26),
               (81, 26), (90, 33), (81, 37), (49, 37), (56, 50),
               (49, 50), (34, 37), (12, 37), (3, 19), (10, 19)], s.accent)
    s.line([(16, 53), (84, 53)], width=2)
    s.person(32, 55, .92)
    s.person(68, 55, .92)
    s.line([(36, 69), (46, 77), (53, 75)], width=5)
    s.line([(64, 69), (54, 77), (47, 75)], width=5)
    s.line([(20, 95), (80, 95)], s.accent, 3)


def _gulf(s):
    s.drone(34, 22, 1.35)
    s.polygon([(10, 65), (52, 40), (95, 65), (88, 74),
               (87, 94), (19, 94), (18, 74)])
    s.polygon([(27, 69), (52, 54), (79, 69), (79, 87),
               (27, 87)], s.accent)
    s.ellipse((47, 62, 59, 74), s.background)
    s.polygon([(45, 77), (61, 77), (64, 87), (42, 87)], s.background)
    s.line([(77, 26), (77, 10)], s.accent, 5)
    s.line([(66, 32), (59, 24)], s.accent, 4)
    s.line([(88, 32), (95, 24)], s.accent, 4)


def _voyager(s):
    s.ellipse((4, 7, 25, 28), s.accent)
    s.polygon([(7, 11), (14, 10), (17, 16), (14, 20), (9, 18)],
              s.background)
    s.polygon([(18, 21), (23, 19), (23, 25), (19, 27)], s.background)
    for start, end in ((30, 36), (40, 46), (50, 56)):
        s.line([(start, 28), (end, 32)], s.accent, 2)
    s.line([(62, 57), (94, 7)], width=2.5)
    s.line([(62, 57), (93, 93)], width=2.5)
    s.line([(62, 57), (17, 92)], width=3)
    s.rect((56, 51, 68, 66), s.accent)
    s.ellipse((41, 25, 81, 55))
    s.ellipse((45, 28, 77, 50), s.background)
    s.line([(61, 40), (70, 16)], width=3)
    s.ellipse((66, 12, 73, 18), s.accent)
    s.line([(60, 52), (49, 43)], width=3)
    for x, y in ((37, 72), (30, 78), (23, 84)):
        s.polygon([(x - 5, y - 5), (x + 3, y - 11),
                   (x + 10, y - 3), (x + 2, y + 3)], s.accent)


def _fed(s):
    s.polygon([(6, 32), (38, 12), (70, 32)], s.accent)
    s.rect((7, 35, 69, 41))
    for x in (14, 34, 54):
        s.rect((x, 43, x + 8, 80))
    s.rect((7, 82, 70, 89))
    s.rect((3, 91, 74, 95), s.accent)
    s.line([(82, 80), (82, 30)], s.accent, 7)
    s.polygon([(69, 42), (82, 24), (95, 42)], s.accent)


def _loan(s):
    s.polygon([(12, 5), (66, 5), (86, 25), (86, 95), (12, 95)])
    s.polygon([(18, 11), (62, 11), (62, 31), (80, 31),
               (80, 89), (18, 89)], s.background)
    s.polygon([(67, 13), (77, 25), (67, 25)], s.accent)
    s.line([(26, 75), (68, 75)], width=3)
    s.line([(26, 82), (57, 82)], width=3)
    # Euro sign as strokes, independent of fonts or character rendering.
    s.line([(64, 40), (57, 35), (45, 35), (35, 44), (35, 55),
            (44, 64), (57, 64), (64, 59)], s.accent, 5)
    s.line([(29, 46), (55, 46)], s.accent, 4)
    s.line([(29, 54), (53, 54)], s.accent, 4)


def _refinery(s):
    s.rect((10, 27, 25, 85))
    s.ellipse((10, 22, 25, 32))
    s.rect((48, 12, 64, 85))
    s.ellipse((48, 7, 64, 17))
    for y in (28, 47, 66):
        s.rect((44, y, 68, y + 5), s.accent)
    s.line([(25, 51), (35, 51), (35, 75), (49, 75)], width=5)
    s.rect((73, 62, 94, 85), s.accent)
    s.ellipse((73, 57, 94, 68), s.accent)
    s.line([(4, 90), (96, 90)], width=5)


def _climate(s):
    s.globe((7, 7, 66, 66))
    s.polygon([(53, 58), (95, 58), (89, 91), (59, 91)])
    s.rect((50, 54, 97, 61), s.accent)
    s.line([(73, 54), (73, 42), (79, 37)], width=3)
    s.ellipse((77, 33, 84, 40))
    s.line([(53, 95), (94, 95)], s.accent, 3)


def _business(s):
    s.rect((7, 31, 93, 90))
    s.rect((14, 39, 86, 82), s.accent)
    s.rect((33, 13, 67, 34))
    s.rect((40, 20, 60, 31), s.background)
    s.line([(14, 57), (86, 57)], s.background, 3)
    s.rect((44, 51, 56, 65))
    s.rect((48, 54, 52, 61), s.background)


def _cyclone(s):
    for phase in (0, pi):
        points = []
        for step in range(65):
            angle = .7 + step * .075
            radius = 8 + step * .51
            points.append((50 + radius * cos(angle + phase),
                           50 + radius * sin(angle + phase)))
        s.line(points, s.accent, 9)
    s.ellipse((42, 42, 58, 58))
    s.ellipse((46, 46, 54, 54), s.background)


def _sudan(s):
    s.drone(53, 22, 1.2)
    for x, y, w in ((5, 66, 27), (38, 58, 30), (73, 70, 22)):
        s.polygon([(x, y), (x + w / 2, y - 13),
                   (x + w, y), (x + w, 92), (x, 92)], s.accent)
        s.rect((x + w * .38, y + 8, x + w * .64, 92))
    s.line([(3, 95), (97, 95)], width=3)


def _ipo(s):
    s.rect((9, 9, 91, 91))
    s.rect((15, 15, 85, 85), s.background)
    s.line([(24, 29), (60, 29)], s.accent, 4)
    s.line([(24, 38), (48, 38)], width=3)
    s.line([(24, 49), (74, 49)], width=3)
    s.line([(24, 59), (63, 59)], width=3)
    s.polygon([(20, 70), (43, 70), (51, 78), (43, 86),
               (20, 86)], s.accent)
    s.ellipse((40, 75, 46, 81), s.background)
    s.ellipse((61, 69, 78, 86), s.accent)
    s.polygon([(64, 82), (63, 98), (70, 93), (76, 98), (75, 82)])


_DRAWINGS = {
    "diplomacy": _diplomacy,
    "gulf": _gulf,
    "voyager": _voyager,
    "fed": _fed,
    "loan": _loan,
    "refinery": _refinery,
    "climate": _climate,
    "business": _business,
    "cyclone": _cyclone,
    "sudan": _sudan,
    "ipo": _ipo,
}


def draw_pictogram(page, name, box, accent, background="paper"):
    """Fit an editorial symbol inside a logical-coordinate box, without stretching."""
    try:
        drawing = _DRAWINGS[name]
    except KeyError as error:
        raise ValueError(f"Unknown pictogram: {name}") from error
    drawing(_Scene(page, box, accent, background))
