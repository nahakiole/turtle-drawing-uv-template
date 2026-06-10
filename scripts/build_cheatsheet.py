"""Build a printable Turtle drawing command cheatsheet PDF."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "turtle-drawing-cheatsheet.pdf"


PALETTE = {
    "ink": colors.HexColor("#1f2937"),
    "muted": colors.HexColor("#4b5563"),
    "rule": colors.HexColor("#d1d5db"),
    "soft": colors.HexColor("#f3f4f6"),
    "blue": colors.HexColor("#2563eb"),
    "blue_soft": colors.HexColor("#eff6ff"),
    "green": colors.HexColor("#047857"),
    "green_soft": colors.HexColor("#ecfdf5"),
}


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "CheatsheetTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=25,
            textColor=PALETTE["ink"],
            spaceAfter=4,
        ),
        "subtitle": ParagraphStyle(
            "CheatsheetSubtitle",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=12,
            textColor=PALETTE["muted"],
            spaceAfter=10,
        ),
        "section": ParagraphStyle(
            "CheatsheetSection",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=13,
            textColor=PALETTE["blue"],
            spaceBefore=0,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "CheatsheetBody",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.4,
            leading=10.4,
            textColor=PALETTE["ink"],
        ),
        "code": ParagraphStyle(
            "CheatsheetCode",
            parent=base["Code"],
            fontName="Courier",
            fontSize=7.7,
            leading=9.4,
            textColor=PALETTE["ink"],
            leftIndent=0,
            rightIndent=0,
        ),
        "tiny": ParagraphStyle(
            "CheatsheetTiny",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.4,
            leading=9,
            textColor=PALETTE["muted"],
        ),
    }


def p(text: str, style: ParagraphStyle) -> Paragraph:
    text = text.replace("\n", "<br/>")
    return Paragraph(text, style)


def code(text: str, style: ParagraphStyle) -> Paragraph:
    escaped = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )
    return Paragraph(escaped, style)


def box(title: str, lines: list[str], sheet: dict[str, ParagraphStyle], accent=None):
    accent = accent or PALETTE["blue_soft"]
    content = [p(title, sheet["section"])]
    content.extend(code(line, sheet["code"]) for line in lines)
    table = Table([[content]], colWidths=[3.45 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), accent),
                ("BOX", (0, 0), (-1, -1), 0.65, PALETTE["rule"]),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return table


def note(title: str, body: str, sheet: dict[str, ParagraphStyle]):
    content = [p(f"<b>{title}</b>", sheet["body"]), p(body, sheet["tiny"])]
    table = Table([[content]], colWidths=[7.1 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), PALETTE["soft"]),
                ("BOX", (0, 0), (-1, -1), 0.65, PALETTE["rule"]),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def command_table(rows: list[tuple[str, str]], sheet: dict[str, ParagraphStyle]):
    table_rows = [[code(cmd, sheet["code"]), p(desc, sheet["body"])] for cmd, desc in rows]
    table = Table(table_rows, colWidths=[2.85 * inch, 4.2 * inch], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.35, PALETTE["rule"]),
                ("BACKGROUND", (0, 0), (0, -1), PALETTE["soft"]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def two_column(left, right):
    table = Table([[left, right]], colWidths=[3.55 * inch, 3.55 * inch])
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return table


def build_pdf():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    sheet = styles()
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        leftMargin=0.45 * inch,
        rightMargin=0.45 * inch,
        topMargin=0.42 * inch,
        bottomMargin=0.42 * inch,
        title="Turtle Drawing Cheatsheet",
        author="Turtle Drawing Template",
    )

    story = [
        p("Turtle Drawing Cheatsheet", sheet["title"]),
        p(
            "Quick commands for the turtle drawing template. Edit "
            "<b>src/turtle_drawing/drawings.py</b>, then run "
            "<b>uv run interactive</b>, <b>uv run live</b>, or <b>uv run render</b>.",
            sheet["subtitle"],
        ),
        command_table(
            [
                ("uv sync", "Install the project dependencies."),
                ("uv run interactive", "Open the real-time Turtle window. Reloads when you save."),
                ("uv run live", "Open the auto-refresh PNG preview window."),
                ("uv run render", "Create output/drawing.png once."),
                ("uv run watch", "Regenerate output/drawing.png whenever code changes."),
            ],
            sheet,
        ),
        Spacer(1, 8),
    ]

    left_boxes = [
        box(
            "Move",
            [
                "t.forward(100)",
                "t.backward(50)",
                "t.left(90)",
                "t.right(45)",
                "t.goto(10, 20)",
                "t.setheading(0)",
                "t.home()",
            ],
            sheet,
        ),
        Spacer(1, 7),
        box(
            "Pen",
            [
                "t.penup()",
                "t.pendown()",
                "t.pensize(5)",
                't.color("red")',
                't.pencolor("blue")',
                "current = t.pencolor()",
            ],
            sheet,
            PALETTE["green_soft"],
        ),
        Spacer(1, 7),
        box(
            "Shapes",
            [
                "draw_square(t, 80)",
                "draw_rectangle(t, 120, 60)",
                "draw_triangle(t, 90)",
                "draw_circle(t, 35)",
                "draw_star(t, 70)",
                "draw_flower(t, x, y)",
            ],
            sheet,
        ),
    ]

    right_boxes = [
        box(
            "Fill",
            [
                't.fillcolor("yellow")',
                "t.begin_fill()",
                "draw_square(t, 80)",
                "t.end_fill()",
                "",
                'draw_filled_circle(t, 25, "red", "pink")',
            ],
            sheet,
            PALETTE["green_soft"],
        ),
        Spacer(1, 7),
        box(
            "Text, Dots, Images",
            [
                't.write("Hello")',
                't.dot(20, "green")',
                'import_picture(t, "assets/example_picture.png", 0, 0, width=120)',
                "pixel = get_pixel_color(t, 0, 0)",
            ],
            sheet,
        ),
        Spacer(1, 7),
        box(
            "Jump Without Drawing",
            [
                "jump_to(t, -100, 50)",
                "",
                "def jump_to(t, x, y):",
                "    t.penup()",
                "    t.goto(x, y)",
                "    t.pendown()",
            ],
            sheet,
            PALETTE["green_soft"],
        ),
    ]

    story.extend([two_column(left_boxes, right_boxes), Spacer(1, 8)])

    story.extend(
        [
            KeepTogether(
                [
                    p("Interactive Mode", sheet["section"]),
                    command_table(
                        [
                            ("def on_click(t, x, y):", "Runs when the user clicks the Turtle window."),
                            ("def on_key(t, key):", "Runs when the user presses a supported key."),
                            ("r / g / b", "Change the current pen color in the example."),
                            ("arrow keys", "Move the turtle and draw in the example."),
                            ("space", "Draw a star in the example."),
                            ("t.clear()", "Clear the window."),
                            ("draw_picture(t)", "Draw the starting picture again."),
                            ("t.hideturtle()", "Hide the turtle cursor while drawing."),
                            ("t.speed(1)", "Slow drawing down. Use 0 for fastest."),
                        ],
                        sheet,
                    ),
                ]
            ),
            Spacer(1, 7),
            note(
                "Turtle coordinates",
                "(0, 0) is the center. x goes left/right. y goes down/up. "
                "Use jump_to(t, x, y) when you want to move without drawing a line.",
                sheet,
            ),
        ]
    )

    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()
