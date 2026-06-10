"""
Edit this file!

The goal is to write Turtle-style drawing code inside draw_picture(t).
Then run:

    uv run render

or start auto-refresh with:

    uv run watch
"""


def draw_square(t, size):
    """Draw a square with the current pen colour."""
    for _ in range(4):
        t.forward(size)
        t.right(90)


def draw_triangle(t, size):
    """Draw an equilateral triangle."""
    for _ in range(3):
        t.forward(size)
        t.left(120)


def jump_to(t, x, y):
    """Move without drawing."""
    t.penup()
    t.goto(x, y)
    t.pendown()


def draw_picture(t):
    """
    Main drawing function.

    Change this function to solve different drawing challenges.
    The coordinates work like normal Turtle:
    - (0, 0) is the middle
    - x goes left/right
    - y goes down/up
    """

    # Background demo: a simple house.
    t.pensize(20)

    # Roof
    jump_to(t, -120, 10)
    t.color("firebrick")
    t.fillcolor("tomato")
    t.begin_fill()
    t.forward(240)
    t.right(100)
    t.forward(240)
    t.end_fill()
