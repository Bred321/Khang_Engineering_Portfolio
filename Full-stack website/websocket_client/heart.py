import turtle as T
import math

# ---------- Setup ----------
T.bgcolor("black")
T.colormode(255)
T.hideturtle()
T.pensize(3)
T.speed(0)
T.tracer(0, 0)   # draw instantly (no animation)

# ---------- Heart parametric (classic) ----------
def heart_xy(t):
    # t in radians
    x = 16 * math.sin(t) ** 3
    y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
    return x, y

def draw_heart(scale=10, pos=(0, 0), fill=True, outline=(255, 80, 80), fill_color=(255, 0, 0), steps=300):
    cx, cy = pos
    T.color(outline)
    if fill:
        T.fillcolor(fill_color)
        T.begin_fill()

    # Move to first point without drawing
    t0 = 0.0
    x0, y0 = heart_xy(t0)
    T.penup()
    T.goto(cx + scale * x0, cy + scale * y0)
    T.pendown()

    # Trace the curve
    for k in range(1, steps + 1):
        t = (2 * math.pi) * k / steps
        x, y = heart_xy(t)
        T.goto(cx + scale * x, cy + scale * y)

    if fill:
        T.end_fill()

# ---------- Draw multiple hearts ----------
# One big filled heart:
draw_heart(scale=10, pos=(0, 0), fill=True)

# A few concentric outlines on top:
for s in (12, 14, 16):
    draw_heart(scale=s, pos=(0, 0), fill=False, outline=(255, 140, 140))

T.update()
T.done()
