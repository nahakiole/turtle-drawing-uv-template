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
    t.pensize(4)

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
    draw_flower(t, -260, -175)
    draw_flower(t, -210, -185)
    draw_flower(t, 245, -180)

    # Star
    jump_to(t, -300, 190)
    t.setheading(0)
    t.color("darkorange")
    t.pensize(3)
    draw_star(t, 65)
