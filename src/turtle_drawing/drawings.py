"""Edit this file to make your own Turtle drawing."""

import math


def draw_square(t, size):
    """Draw a square with the current pen color."""
    for _ in range(4):
        t.forward(size)
        t.right(90)


def draw_rectangle(t, width, height):
    """Draw a rectangle with the current pen color."""
    for _ in range(2):
        t.forward(width)
        t.right(90)
        t.forward(height)
        t.right(90)


def draw_triangle(t, size):
    """Draw an equilateral triangle."""
    for _ in range(3):
        t.forward(size)
        t.left(120)


def draw_circle(t, radius):
    """Draw a circle above the turtle."""
    t.circle(radius)


def draw_star(t, size):
    """Draw a five-point star."""
    for _ in range(5):
        t.forward(size)
        t.right(144)


def draw_filled_square(t, size, outline_color, fill_color):
    """Draw a square with an outline and fill color."""
    t.color(outline_color)
    t.fillcolor(fill_color)
    t.begin_fill()
    draw_square(t, size)
    t.end_fill()


def draw_filled_rectangle(t, width, height, outline_color, fill_color):
    """Draw a rectangle with an outline and fill color."""
    t.color(outline_color)
    t.fillcolor(fill_color)
    t.begin_fill()
    draw_rectangle(t, width, height)
    t.end_fill()


def draw_filled_triangle(t, size, outline_color, fill_color):
    """Draw a triangle with an outline and fill color."""
    t.color(outline_color)
    t.fillcolor(fill_color)
    t.begin_fill()
    draw_triangle(t, size)
    t.end_fill()


def draw_filled_circle(t, radius, outline_color, fill_color):
    """Draw a circle with an outline and fill color."""
    t.color(outline_color)
    t.fillcolor(fill_color)
    t.begin_fill()
    draw_circle(t, radius)
    t.end_fill()


def jump_to(t, x, y):
    """Move without drawing."""
    t.penup()
    t.goto(x, y)
    t.pendown()


def import_picture(t, path, x, y, width=None, height=None):
    """Add an existing picture to the PNG preview, centered at x, y."""
    if hasattr(t, "draw_image"):
        t.draw_image(path, x, y, width=width, height=height)
        return

    jump_to(t, x, y)


def get_pixel_color(t, x, y):
    """Get the RGB color at x, y in the PNG preview."""
    if hasattr(t, "pixel_at"):
        return t.pixel_at(x, y)

    return None


def draw_color_swatch(t, x, y, color):
    """Draw a little square showing an RGB color."""
    if color is None:
        return

    jump_to(t, x, y)
    t.setheading(0)
    draw_filled_square(t, 28, "black", color)


def draw_flower(t, x, y):
    """Draw a small flower centered near x, y."""
    petal_radius = 18

    for angle in range(0, 360, 60):
        petal_x = x + math.cos(math.radians(angle)) * 22
        petal_y = y + math.sin(math.radians(angle)) * 22
        jump_to(t, petal_x, petal_y - petal_radius)
        draw_filled_circle(t, petal_radius, "hotpink", "pink")

    jump_to(t, x, y - 10)
    draw_filled_circle(t, 10, "goldenrod", "yellow")


def draw_picture(t):
    """
    Main drawing function.

    Change this function to solve different drawing challenges.
    The coordinates work like normal Turtle:
    - (0, 0) is the middle
    - x goes left/right
    - y goes down/up
    """

    t.speed(0)
    t.pensize(5)

    # Import an existing picture.
    # Try replacing this with your own PNG or JPG file.
    import_picture(t, "assets/example_picture.png", -280, 100, width=120)

    # Read one pixel from the finished drawing so far.
    # The result is an RGB color like (135, 206, 235).
    pixel_color = get_pixel_color(t, -280, 100)
    jump_to(t, -340, 35)
    t.color("black")
    draw_color_swatch(t, -340, 20, pixel_color)

    # Sun
    jump_to(t, 260, 180)
    draw_filled_circle(t, 55, "orange", "gold")

    # A simple house body.
    jump_to(t, -140, -40)
    t.setheading(0)
    draw_filled_square(t, 180, "saddlebrown", "burlywood")

    # Roof
    jump_to(t, -165, -40)
    t.setheading(0)
    draw_filled_triangle(t, 230, "firebrick", "tomato")

    # Door
    jump_to(t, -75, -125)
    t.setheading(0)
    draw_filled_rectangle(t, 45, 95, "saddlebrown", "peru")

    # Windows
    jump_to(t, -125, -75)
    t.setheading(0)
    draw_filled_square(t, 35, "steelblue", "lightblue")

    jump_to(t, -25, -75)
    t.setheading(0)
    draw_filled_square(t, 35, "steelblue", "lightblue")

    # Tree trunk
    jump_to(t, 120, -80)
    t.setheading(0)
    draw_filled_rectangle(t, 35, 120, "sienna", "peru")

    # Tree leaves
    jump_to(t, 108, 15)
    draw_filled_circle(t, 45, "forestgreen", "limegreen")

    jump_to(t, 145, 30)
    draw_filled_circle(t, 45, "forestgreen", "limegreen")

    jump_to(t, 180, 15)
    draw_filled_circle(t, 45, "forestgreen", "limegreen")

    # Flowers
    draw_flower(t, -290, -175)
    draw_flower(t, -200, -185)
    draw_flower(t, 245, -180)

    # Star
    jump_to(t, -300, 190)
    t.setheading(0)
    t.color("darkorange")
    t.pensize(3)
    draw_star(t, 65)


def on_click(t, x, y):
    """Interactive mode: draw a purple circle wherever you click."""
    t.pensize(3)
    jump_to(t, x, y - 20)
    draw_filled_circle(t, 20, "purple", "plum")
    jump_to(t, x, y)


def on_key(t, key):
    """Interactive mode: use arrow keys, space, c, r, g, and b."""
    if key == "c":
        t.clear()
        draw_picture(t)
        return

    if key == "r":
        t.color("red")
        return

    if key == "g":
        t.color("green")
        return

    if key == "b":
        t.color("blue")
        return

    if key == "space":
        draw_star(t, 50)
        return

    directions = {
        "Up": 90,
        "Down": 270,
        "Left": 180,
        "Right": 0,
    }

    if key in directions:
        t.setheading(directions[key])
        t.forward(30)
