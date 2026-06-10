"""Build a printable Turtle drawing command cheatsheet PDF."""

from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
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
    "amber": colors.HexColor("#92400e"),
    "amber_soft": colors.HexColor("#fffbeb"),
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
        "page_title": ParagraphStyle(
            "CheatsheetPageTitle",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=20,
            textColor=PALETTE["ink"],
            spaceAfter=8,
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


def note(title: str, body: str, sheet: dict[str, ParagraphStyle], accent=None):
    accent = accent or PALETTE["soft"]
    content = [p(f"<b>{title}</b>", sheet["body"]), p(body, sheet["tiny"])]
    table = Table([[content]], colWidths=[7.1 * inch])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), accent),
                ("BOX", (0, 0), (-1, -1), 0.65, PALETTE["rule"]),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def command_table(
    rows: list[tuple[str, str]],
    sheet: dict[str, ParagraphStyle],
    col_widths=None,
):
    col_widths = col_widths or [2.85 * inch, 4.2 * inch]
    table_rows = [[code(cmd, sheet["code"]), p(desc, sheet["body"])] for cmd, desc in rows]
    table = Table(table_rows, colWidths=col_widths, hAlign="LEFT")
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


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(PALETTE["muted"])
    canvas.drawString(0.45 * inch, 0.25 * inch, "Turtle Drawing Template")
    canvas.drawRightString(7.95 * inch, 0.25 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build_intro_page(sheet):
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
                't.fillcolor("yellow")',
                "current = t.pencolor()",
            ],
            sheet,
            PALETTE["green_soft"],
        ),
        Spacer(1, 7),
        box(
            "Coordinates",
            [
                "(0, 0) is the center",
                "x: left / right",
                "y: down / up",
                "jump_to(t, x, y)",
            ],
            sheet,
            PALETTE["amber_soft"],
        ),
    ]

    right_boxes = [
        box(
            "Draw",
            [
                "t.circle(40)",
                't.dot(20, "green")',
                't.write("Hello")',
                "t.clear()",
                "t.hideturtle()",
                "t.speed(1)   # slow",
                "t.speed(0)   # fastest",
            ],
            sheet,
        ),
        Spacer(1, 7),
        box(
            "Fill",
            [
                't.fillcolor("gold")',
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
            "Run It",
            [
                "uv sync",
                "uv run interactive",
                "uv run live",
                "uv run render",
                "uv run watch",
                "uv run draw",
            ],
            sheet,
            PALETTE["amber_soft"],
        ),
    ]

    return [
        p("Turtle Drawing Cheatsheet", sheet["title"]),
        p(
            "A printable reference for the turtle drawing template. Edit "
            "<b>src/turtle_drawing/drawings.py</b>, save, and use "
            "<b>uv run interactive</b> for real-time drawing.",
            sheet["subtitle"],
        ),
        command_table(
            [
                ("uv run interactive", "Real Turtle window. Reloads quickly when you save."),
                ("uv run live", "Auto-refresh PNG preview window."),
                ("uv run render", "Generate output/drawing.png once."),
                ("uv run watch", "Regenerate output/drawing.png whenever code changes."),
            ],
            sheet,
        ),
        Spacer(1, 8),
        two_column(left_boxes, right_boxes),
        Spacer(1, 8),
        note(
            "Most important idea",
            "The turtle remembers where it is pointing. Movement commands draw from the current position. "
            "Use t.penup() or jump_to(t, x, y) when you want to move without drawing.",
            sheet,
        ),
    ]


def build_recipe_page(sheet):
    shape_helpers = command_table(
        [
            ("draw_square(t, 80)", "Square using the current pen color."),
            ("draw_rectangle(t, 120, 60)", "Rectangle with width and height."),
            ("draw_triangle(t, 90)", "Equilateral triangle."),
            ("draw_circle(t, 35)", "Circle above the turtle."),
            ("draw_star(t, 70)", "Five-point star."),
            ("draw_flower(t, x, y)", "Flower centered near x, y."),
        ],
        sheet,
    )
    fill_helpers = command_table(
        [
            ('draw_filled_square(t, 80, "black", "gold")', "Filled square."),
            ('draw_filled_rectangle(t, 120, 60, "brown", "tan")', "Filled rectangle."),
            ('draw_filled_triangle(t, 100, "red", "tomato")', "Filled triangle."),
            ('draw_filled_circle(t, 30, "blue", "lightblue")', "Filled circle."),
        ],
        sheet,
    )
    examples = [
        box(
            "House Recipe",
            [
                "jump_to(t, -100, -50)",
                'draw_filled_square(t, 160, "brown", "tan")',
                "jump_to(t, -120, -50)",
                'draw_filled_triangle(t, 200, "red", "tomato")',
            ],
            sheet,
        ),
        Spacer(1, 7),
        box(
            "Repeating Pattern",
            [
                "for _ in range(12):",
                "    draw_star(t, 50)",
                "    t.right(30)",
                "    t.forward(20)",
            ],
            sheet,
            PALETTE["green_soft"],
        ),
        Spacer(1, 7),
        box(
            "Spiral",
            [
                "for size in range(10, 160, 10):",
                "    t.forward(size)",
                "    t.right(90)",
            ],
            sheet,
            PALETTE["amber_soft"],
        ),
    ]
    right_examples = [
        box(
            "Color Palette",
            [
                '"red", "orange", "gold"',
                '"green", "limegreen"',
                '"blue", "lightblue"',
                '"purple", "plum"',
                '"black", "gray", "white"',
                '"brown", "tan", "pink"',
            ],
            sheet,
            PALETTE["amber_soft"],
        ),
        Spacer(1, 7),
        box(
            "Write Labels",
            [
                "jump_to(t, -80, 120)",
                't.color("black")',
                't.write("My picture")',
                "",
                't.write("Big", font=("Arial", 20, "bold"))',
            ],
            sheet,
        ),
        Spacer(1, 7),
        box(
            "Reusable Function",
            [
                "def draw_tree(t, x, y):",
                "    jump_to(t, x, y)",
                '    draw_filled_rectangle(t, 30, 100, "brown", "peru")',
                "    jump_to(t, x - 25, y + 75)",
                '    draw_filled_circle(t, 45, "green", "limegreen")',
            ],
            sheet,
            PALETTE["green_soft"],
        ),
    ]
    return [
        p("Drawing Recipes and Helper Functions", sheet["page_title"]),
        p(
            "Use these helpers from <b>drawings.py</b> to build pictures faster. "
            "You can copy the recipes and change numbers or colors.",
            sheet["subtitle"],
        ),
        p("Shape helpers", sheet["section"]),
        shape_helpers,
        Spacer(1, 7),
        p("Filled shape helpers", sheet["section"]),
        fill_helpers,
        Spacer(1, 8),
        two_column(examples, right_examples),
    ]


def build_interactive_page(sheet):
    interactive_rows = [
        ("def on_click(t, x, y):", "Runs when the user clicks the Turtle window."),
        ("def on_key(t, key):", "Runs when the user presses a supported key."),
        ("r / g / b", "Change the current pen color in the example."),
        ("arrow keys", "Move the turtle and draw in the example."),
        ("space", "Draw a star in the example."),
        ("t.clear()", "Clear the window."),
        ("draw_picture(t)", "Draw the starting picture again."),
    ]
    image_rows = [
        ('import_picture(t, "assets/example_picture.png", 0, 0, width=120)', "Place an image in the PNG preview."),
        ("pixel = get_pixel_color(t, 0, 0)", "Read an RGB color from the PNG preview."),
        ("draw_color_swatch(t, -80, 20, pixel)", "Draw a square showing that RGB color."),
    ]
    left_boxes = [
        box(
            "Click With Current Color",
            [
                "def on_click(t, x, y):",
                "    current = t.pencolor()",
                "    jump_to(t, x, y - 20)",
                "    draw_filled_circle(t, 20, current, current)",
            ],
            sheet,
        ),
        Spacer(1, 7),
        box(
            "Keyboard Example",
            [
                "def on_key(t, key):",
                '    if key == "r":',
                '        t.color("red")',
                '    if key == "space":',
                "        draw_star(t, 50)",
            ],
            sheet,
            PALETTE["green_soft"],
        ),
    ]
    right_boxes = [
        box(
            "Debug Checklist",
            [
                "Save drawings.py",
                "Read the terminal error",
                "Check parentheses: ( )",
                "Check quotes: \"red\"",
                "Check indentation",
                "Try uv run render",
            ],
            sheet,
            PALETTE["amber_soft"],
        ),
        Spacer(1, 7),
        box(
            "Common Mistakes",
            [
                "forward(100)  # missing t.",
                "t.color(red) # missing quotes",
                "t.goto(10)   # needs x and y",
                "if key = \"r\": # use ==",
            ],
            sheet,
        ),
    ]
    return [
        p("Interactive, Images, and Debugging", sheet["page_title"]),
        p(
            "<b>uv run interactive</b> reloads quickly after every save and remembers the window position. "
            "<b>uv run render</b> and <b>uv run live</b> create PNG previews.",
            sheet["subtitle"],
        ),
        p("Interactive hooks", sheet["section"]),
        command_table(interactive_rows, sheet),
        Spacer(1, 7),
        p("Images and pixels", sheet["section"]),
        command_table(image_rows, sheet),
        Spacer(1, 8),
        two_column(left_boxes, right_boxes),
        Spacer(1, 8),
        note(
            "When to use each preview",
            "Use interactive for real-time Turtle drawing and mouse/keyboard experiments. "
            "Use live or render when you need image import, pixel reading, or a saved PNG.",
            sheet,
            PALETTE["blue_soft"],
        ),
    ]


def build_pdf():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    sheet = styles()
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=letter,
        leftMargin=0.45 * inch,
        rightMargin=0.45 * inch,
        topMargin=0.42 * inch,
        bottomMargin=0.45 * inch,
        title="Turtle Drawing Cheatsheet",
        author="Turtle Drawing Template",
    )

    story = []
    story.extend(build_intro_page(sheet))
    story.append(PageBreak())
    story.extend(build_recipe_page(sheet))
    story.append(PageBreak())
    story.extend(build_interactive_page(sheet))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()
