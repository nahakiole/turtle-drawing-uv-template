"""Open a real-time Turtle window that reloads drawings.py on save."""

from __future__ import annotations

import importlib
import os
import sys
import time
import traceback
import turtle
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DRAWINGS_PATH = PROJECT_ROOT / "src" / "turtle_drawing" / "drawings.py"

KEYS = [
    "Up",
    "Down",
    "Left",
    "Right",
    "space",
    "c",
    "r",
    "g",
    "b",
]


class InteractivePreview:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Interactive Turtle Preview")
        self.screen.setup(width=900, height=700)
        self.screen.bgcolor("white")

        self.artist = turtle.Turtle()
        self.artist.shape("turtle")
        self.artist.speed(6)

        self.message = turtle.Turtle(visible=False)
        self.message.penup()

        self.drawings = None
        self.last_mtime = 0.0

    def start(self):
        self.reload_and_draw()
        self.screen.ontimer(self.check_for_changes, 300)
        self.screen.mainloop()

    def check_for_changes(self):
        try:
            mtime = DRAWINGS_PATH.stat().st_mtime
            if mtime != self.last_mtime:
                self.reload_and_draw()
        finally:
            self.screen.ontimer(self.check_for_changes, 300)

    def reload_and_draw(self):
        try:
            self.drawings = self.load_drawings()
            self.reset_artist()
            self.drawings.draw_picture(self.artist)
            self.bind_interaction()
            self.last_mtime = DRAWINGS_PATH.stat().st_mtime
            self.show_message(f"Updated {time.strftime('%H:%M:%S')}")
        except Exception:
            self.last_mtime = DRAWINGS_PATH.stat().st_mtime
            self.show_error(traceback.format_exc())

    def load_drawings(self):
        importlib.invalidate_caches()

        module_name = "turtle_drawing.drawings"
        if module_name in sys.modules:
            return importlib.reload(sys.modules[module_name])

        return importlib.import_module(module_name)

    def reset_artist(self):
        self.artist.reset()
        self.artist.hideturtle()
        self.artist.speed(6)
        self.artist.pensize(2)
        self.artist.color("black")
        self.message.clear()

    def bind_interaction(self):
        self.screen.onclick(None)
        for key in KEYS:
            self.screen.onkeypress(None, key)

        if hasattr(self.drawings, "on_click"):
            self.screen.onclick(
                lambda x, y: self.drawings.on_click(self.artist, x, y)
            )

        if hasattr(self.drawings, "on_key"):
            for key in KEYS:
                self.screen.onkeypress(
                    lambda key=key: self.drawings.on_key(self.artist, key),
                    key,
                )

        if hasattr(self.drawings, "setup_interaction"):
            self.drawings.setup_interaction(self.artist, self.screen)

        self.screen.listen()

    def show_message(self, text):
        self.message.clear()
        self.message.goto(-430, 315)
        self.message.color("gray25")
        self.message.write(text, font=("Arial", 12, "normal"))

    def show_error(self, message):
        print(message)
        self.artist.clear()
        self.message.clear()
        self.message.goto(-430, 315)
        self.message.color("firebrick")
        self.message.write(
            "Could not draw the picture. Fix the error and save drawings.py again.",
            font=("Arial", 12, "normal"),
        )


def main():
    os.chdir(PROJECT_ROOT)
    InteractivePreview().start()


if __name__ == "__main__":
    main()
