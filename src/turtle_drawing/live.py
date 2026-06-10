"""Open an auto-refreshing PNG preview window."""

from __future__ import annotations

import importlib
import os
import sys
import textwrap
import time
import traceback
import tkinter as tk
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageTk

from turtle_drawing.render import PreviewTurtle

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DRAWINGS_PATH = PROJECT_ROOT / "src" / "turtle_drawing" / "drawings.py"
OUTPUT_PATH = PROJECT_ROOT / "output" / "drawing.png"


class LivePreview:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Live Turtle Preview")

        self.status = tk.StringVar(value="Starting live preview...")
        self.image_label = tk.Label(self.root, bg="white")
        self.image_label.pack()

        status_label = tk.Label(self.root, textvariable=self.status, anchor="w", padx=8)
        status_label.pack(fill="x")

        self.photo_image = None
        self.last_mtime = 0.0

    def start(self):
        self.render()
        self.root.after(300, self.check_for_changes)
        self.root.mainloop()

    def check_for_changes(self):
        try:
            mtime = DRAWINGS_PATH.stat().st_mtime
            if mtime != self.last_mtime:
                self.render()
        finally:
            self.root.after(300, self.check_for_changes)

    def render(self):
        try:
            image = self.render_drawing()
            OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
            image.save(OUTPUT_PATH)
            self.show_image(image)
            self.last_mtime = DRAWINGS_PATH.stat().st_mtime
            self.status.set(f"Updated {time.strftime('%H:%M:%S')} - saved {OUTPUT_PATH}")
        except Exception:
            message = traceback.format_exc()
            print(message)
            self.show_image(self.error_image(message))
            self.last_mtime = DRAWINGS_PATH.stat().st_mtime
            self.status.set("Preview failed. Fix the error and save drawings.py again.")

    def render_drawing(self):
        importlib.invalidate_caches()

        module_name = "turtle_drawing.drawings"
        if module_name in sys.modules:
            drawings = importlib.reload(sys.modules[module_name])
        else:
            drawings = importlib.import_module(module_name)

        turtle = PreviewTurtle()
        drawings.draw_picture(turtle)
        return turtle.image

    def show_image(self, image):
        self.photo_image = ImageTk.PhotoImage(image)
        self.image_label.configure(image=self.photo_image)

    def error_image(self, message):
        image = Image.new("RGB", (900, 700), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        draw.text((20, 20), "Could not draw the picture:", fill="firebrick", font=font)
        y = 50
        for line in textwrap.wrap(message, width=110):
            draw.text((20, y), line, fill="black", font=font)
            y += 16
            if y > 670:
                break

        return image


def main():
    os.chdir(PROJECT_ROOT)
    LivePreview().start()


if __name__ == "__main__":
    main()
