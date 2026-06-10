"""Auto-render output/drawing.png when source files change."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

WATCHED_DIR = Path("src/turtle_drawing")


class RenderOnChange(FileSystemEventHandler):
    def __init__(self):
        self.last_run = 0.0

    def on_modified(self, event):
        if event.is_directory:
            return
        if not event.src_path.endswith(".py"):
            return

        now = time.time()
        if now - self.last_run < 0.3:
            return
        self.last_run = now
        render()


def render():
    print("\nChange detected. Rendering preview...")
    result = subprocess.run(
        [sys.executable, "-m", "turtle_drawing.render"],
        text=True,
        capture_output=True,
    )
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip())
    if result.returncode != 0:
        print("Rendering failed. Fix the error and save again.")


def main():
    render()
    print(f"Watching {WATCHED_DIR}. Press Ctrl+C to stop.")
    observer = Observer()
    observer.schedule(RenderOnChange(), str(WATCHED_DIR), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
