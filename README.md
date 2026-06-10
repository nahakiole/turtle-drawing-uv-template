# Turtle Drawing Template

A small Python project for a 13-year-old programming project: write Turtle-style drawing commands, generate a PNG preview, and auto-refresh it while editing in VS Code.

## Install uv

If `uv` is not installed yet:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On Windows, use PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Start

```bash
uv sync
uv run render
```

This creates:

```text
output/drawing.png
```

Open `output/drawing.png` in VS Code. Then start auto-refresh:

```bash
uv run watch
```

Now edit this file:

```text
src/turtle_drawing/drawings.py
```

Every time you save, the PNG is regenerated.

## Run the real Turtle window

```bash
uv run draw
```

This opens the normal Turtle window. The PNG renderer supports the most important commands, but the Turtle window is useful for checking behaviour visually.

## VS Code workflow

1. Open this folder in VS Code.
2. Open `src/turtle_drawing/drawings.py` on the left.
3. Run the task `Watch Turtle Preview`.
4. Open `output/drawing.png` on the right.
5. Save the Python file and watch the image update.

## Challenge ideas

Try changing `draw_picture(t)` to draw:

- a house
- a robot
- a flower
- a spiral
- a city skyline
- a treasure map
- a monster
- a mandala

## Import a picture

The example file includes:

```python
import_picture(t, "assets/example_picture.png", -280, 100, width=120)
```

This puts an existing image into the PNG preview. Try adding your own image file to the project and changing the path:

```python
import_picture(t, "assets/my_photo.jpg", 0, 0, width=200)
```

## Read a pixel color

The example file also includes:

```python
pixel_color = get_pixel_color(t, -280, 100)
```

This reads the color at Turtle coordinates `(-280, 100)` from the PNG preview and returns an RGB value like:

```python
(135, 206, 235)
```

Pixel reading works with `uv run render` and `uv run watch`, because those commands create the PNG preview. The normal Turtle window does not support reading PNG pixels.

## Supported drawing commands in preview mode

The PNG preview supports these Turtle-like commands:

```python
t.forward(100)
t.backward(50)
t.left(90)
t.right(45)
t.goto(10, 20)
t.setheading(0)
t.penup()
t.pendown()
t.color("red")
t.pencolor("blue")
t.fillcolor("yellow")
t.pensize(5)
t.circle(40)
t.dot(20, "green")
t.begin_fill()
t.end_fill()
t.write("Hello")
t.draw_image("assets/example_picture.png", 0, 0, width=120)
t.pixel_at(0, 0)
```

For more advanced Turtle commands, use `uv run draw` with the real Turtle window.
