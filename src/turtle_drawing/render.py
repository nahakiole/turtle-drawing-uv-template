"""Render Turtle-style drawing commands to a PNG image.

This renderer intentionally supports a beginner-friendly subset of turtle.
For full turtle behaviour, run `uv run draw`.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import List, Tuple

from PIL import Image, ImageDraw, ImageFont

Point = Tuple[float, float]


class PreviewTurtle:
    def __init__(self, width: int = 900, height: int = 700, background: str = "white"):
        self.width = width
        self.height = height
        self.image = Image.new("RGB", (width, height), background)
        self.draw = ImageDraw.Draw(self.image)

        self.x = 0.0
        self.y = 0.0
        self.heading = 0.0
        self.is_down = True
        self.pen_colour = "black"
        self.fill_colour = "black"
        self.pen_width = 1
        self._fill_points: List[Point] | None = None

    def _screen(self, x: float, y: float) -> tuple[int, int]:
        return int(round(self.width / 2 + x)), int(round(self.height / 2 - y))

    def _line(self, x1: float, y1: float, x2: float, y2: float):
        if self.is_down:
            self.draw.line(
                [self._screen(x1, y1), self._screen(x2, y2)],
                fill=self.pen_colour,
                width=self.pen_width,
            )
        if self._fill_points is not None:
            self._fill_points.append((x2, y2))

    def forward(self, distance: float):
        radians = math.radians(self.heading)
        new_x = self.x + math.cos(radians) * distance
        new_y = self.y + math.sin(radians) * distance
        self._line(self.x, self.y, new_x, new_y)
        self.x = new_x
        self.y = new_y

    def backward(self, distance: float):
        self.forward(-distance)

    def right(self, angle: float):
        self.heading -= angle

    def left(self, angle: float):
        self.heading += angle

    def setheading(self, angle: float):
        self.heading = angle

    def goto(self, x: float, y: float):
        self._line(self.x, self.y, x, y)
        self.x = float(x)
        self.y = float(y)

    def home(self):
        self.goto(0, 0)
        self.setheading(0)

    def penup(self):
        self.is_down = False

    def pendown(self):
        self.is_down = True

    def pensize(self, size: int):
        self.pen_width = max(1, int(size))

    def width(self, size: int):
        self.pensize(size)

    def pencolor(self, colour: str):
        self.pen_colour = colour

    def fillcolor(self, colour: str):
        self.fill_colour = colour

    def color(self, *args: str):
        if len(args) == 1:
            self.pen_colour = args[0]
            self.fill_colour = args[0]
        elif len(args) >= 2:
            self.pen_colour = args[0]
            self.fill_colour = args[1]

    def begin_fill(self):
        self._fill_points = [(self.x, self.y)]

    def end_fill(self):
        if self._fill_points and len(self._fill_points) >= 3:
            points = [self._screen(x, y) for x, y in self._fill_points]
            self.draw.polygon(points, fill=self.fill_colour, outline=self.pen_colour)
        self._fill_points = None

    def circle(self, radius: float, extent: float | None = None, steps: int | None = None):
        # Simple preview: draw a full circle centred above the turtle, similar enough for beginner tasks.
        # The real Turtle window gives exact turtle circle behaviour.
        if extent is not None and abs(extent) < 360:
            steps = steps or max(8, int(abs(extent) / 8))
            step_angle = extent / steps
            step_length = 2 * math.pi * abs(radius) * abs(extent) / 360 / steps
            for _ in range(steps):
                self.forward(step_length)
                self.left(step_angle)
            return

        cx = self.x
        cy = self.y + radius
        bbox = [
            self._screen(cx - radius, cy + radius),
            self._screen(cx + radius, cy - radius),
        ]
        flat_bbox = [bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1]]
        if self.is_down:
            self.draw.ellipse(flat_bbox, outline=self.pen_colour, width=self.pen_width)
        if self._fill_points is not None:
            samples = steps or 48
            for i in range(samples + 1):
                a = 2 * math.pi * i / samples
                self._fill_points.append((cx + math.cos(a) * radius, cy + math.sin(a) * radius))

    def dot(self, size: int = 10, colour: str | None = None):
        colour = colour or self.pen_colour
        r = size / 2
        bbox = [
            self._screen(self.x - r, self.y + r),
            self._screen(self.x + r, self.y - r),
        ]
        self.draw.ellipse([bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1]], fill=colour)

    def draw_image(
        self,
        path: str,
        x: float,
        y: float,
        width: int | None = None,
        height: int | None = None,
    ):
        """Paste an image into the PNG preview, centered at Turtle coordinates x, y."""
        picture = Image.open(path).convert("RGBA")

        if width is not None or height is not None:
            original_width, original_height = picture.size
            if width is None:
                width = round(original_width * height / original_height)
            if height is None:
                height = round(original_height * width / original_width)
            picture = picture.resize((int(width), int(height)))

        screen_x, screen_y = self._screen(x, y)
        left = screen_x - picture.width // 2
        top = screen_y - picture.height // 2
        self.image.paste(picture, (left, top), picture)
        self.draw = ImageDraw.Draw(self.image)

    def pixel_at(self, x: float, y: float) -> tuple[int, int, int] | None:
        """Return the RGB color at Turtle coordinates x, y."""
        screen_x, screen_y = self._screen(x, y)
        if not (0 <= screen_x < self.width and 0 <= screen_y < self.height):
            return None

        red, green, blue = self.image.getpixel((screen_x, screen_y))
        return red, green, blue

    def write(self, text: str, font=None, align: str = "left"):
        try:
            size = font[1] if font and len(font) > 1 else 16
            pil_font = ImageFont.truetype("DejaVuSans.ttf", size)
        except Exception:
            pil_font = ImageFont.load_default()
        sx, sy = self._screen(self.x, self.y)
        self.draw.text((sx, sy), str(text), fill=self.pen_colour, font=pil_font, anchor=None)

    def speed(self, *_args, **_kwargs):
        pass

    def shape(self, *_args, **_kwargs):
        pass

    def hideturtle(self):
        pass

    def save(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.image.save(path)


def main():
    from turtle_drawing.drawings import draw_picture

    output = Path("output/drawing.png")
    t = PreviewTurtle()
    draw_picture(t)
    t.save(output)
    print(f"Rendered {output}")


if __name__ == "__main__":
    main()
