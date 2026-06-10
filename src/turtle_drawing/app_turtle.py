"""Open the real Turtle window."""

import turtle

from turtle_drawing.drawings import draw_picture


def main():
    screen = turtle.Screen()
    screen.title("Turtle Drawing Project")
    screen.setup(width=900, height=700)
    screen.bgcolor("white")

    t = turtle.Turtle()
    t.shape("turtle")
    t.speed(0)

    draw_picture(t)

    t.hideturtle()
    screen.mainloop()


if __name__ == "__main__":
    main()
