# -*- coding: utf-8 -*-
"""Draw every diagram used by the cards. Run after editing, before build.py."""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
MEDIA = os.path.join(BASE, "media")
os.makedirs(MEDIA, exist_ok=True)

FONT = "C:/Windows/Fonts/segoeui.ttf"
FONTB = "C:/Windows/Fonts/segoeuib.ttf"
MONO = "C:/Windows/Fonts/consola.ttf"
BG = "#fdfdfd"


def jdk_jre_jvm():
    W, H = 900, 620
    img = Image.new("RGB", (W, H), "#ffffff")
    d = ImageDraw.Draw(img)
    f_lbl = ImageFont.truetype(FONTB, 30)
    f_sub = ImageFont.truetype(FONT, 20)
    f_small = ImageFont.truetype(FONT, 17)

    def box(x0, y0, x1, y1, color, width=3):
        d.rounded_rectangle([x0, y0, x1, y1], radius=18, outline=color, width=width)

    box(30, 40, 870, 560, "#1565c0", 4)
    d.text((55, 55), "JDK", font=f_lbl, fill="#1565c0")
    d.text((130, 65), "Java Development Kit", font=f_sub, fill="#1565c0")

    box(90, 120, 810, 500, "#2e7d32", 4)
    d.text((115, 132), "JRE", font=f_lbl, fill="#2e7d32")
    d.text((190, 142), "Java Runtime Environment", font=f_sub, fill="#2e7d32")

    box(160, 210, 740, 430, "#c62828", 4)
    d.text((185, 222), "JVM", font=f_lbl, fill="#c62828")
    d.text((265, 232), "Java Virtual Machine", font=f_sub, fill="#c62828")
    d.text((200, 300), "loads .class bytecode", font=f_small, fill="#444")
    d.text((200, 330), "verifies it, then executes it", font=f_small, fill="#444")
    d.text((200, 360), "handles memory + GC", font=f_small, fill="#444")

    d.text((120, 450), "core class libraries (java.base, ...)", font=f_small, fill="#444")
    d.text((70, 512), "javac, javadoc, jshell, jar, jlink", font=f_small, fill="#444")
    d.text((30, 580), "compile-time  ->  runtime", font=f_sub, fill="#666")
    img.save(os.path.join(MEDIA, "jdk-jre-jvm.png"))


def landscape():
    W, H = 1040, 930
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f_t = ImageFont.truetype(FONTB, 34)
    f_b = ImageFont.truetype(FONTB, 20)
    f_s = ImageFont.truetype(FONT, 16)

    d.text((40, 28), "The Java roadmap in four bands", fill="#111", font=f_t)
    d.text((40, 74), "each band builds on the one above it", fill="#777", font=f_s)

    bands = [
        ("01 Language core", "#1565c0", ["01 Foundations", "02 Object Model", "03 Language Features"]),
        ("02 Data and flow", "#6a1b9a", ["04 Collections", "05 Functional Programming", "06 Concurrency"]),
        ("03 Talking to the world", "#00695c", ["07 IO and Network", "08 Persistence", "09 Build and Frameworks"]),
        ("04 Keeping it correct", "#b26a00", ["10 Testing", "11 Logging", "12 Documentation"]),
    ]

    y = 112
    bh = 150
    for i, (label, color, items) in enumerate(bands):
        d.rounded_rectangle([40, y, W - 40, y + bh], radius=14, outline=color, width=3,
                            fill="#ffffff")
        d.text((62, y + 14), label, fill=color, font=f_b)
        left, right, gap = 62, W - 40 - 24, 16
        bw = (right - left - 2 * gap) / 3
        for j, it in enumerate(items):
            x0 = left + j * (bw + gap)
            d.rounded_rectangle([x0, y + 54, x0 + bw, y + bh - 18], radius=10, fill=color)
            tw = d.textlength(it, font=f_s)
            d.text((x0 + (bw - tw) / 2, y + 90), it, fill="#ffffff", font=f_s)
        if i < len(bands) - 1:
            cy = y + bh + 5
            d.line([(W / 2, cy), (W / 2, cy + 20)], fill="#999", width=3)
            d.polygon([(W / 2 - 8, cy + 18), (W / 2 + 8, cy + 18), (W / 2, cy + 30)], fill="#999")
        y += bh + 46

    d.text((40, H - 46), "study top to bottom: do not start a band before the one above is solid",
           fill="#777", font=f_s)
    img.save(os.path.join(MEDIA, "java-landscape.png"))


def stack_heap():
    W, H = 940, 640
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f_t = ImageFont.truetype(FONTB, 26)
    f = ImageFont.truetype(FONT, 19)
    f_h = ImageFont.truetype(FONTB, 18)
    fm = ImageFont.truetype(MONO, 17)

    d.text((40, 26), "Where a Java object lives", fill="#111", font=f_t)

    d.rounded_rectangle([40, 90, 410, 470], radius=12, outline="#1565c0", width=3)
    d.text((60, 102), "STACK  (one per thread)", fill="#1565c0", font=f_h)
    d.rounded_rectangle([66, 152, 384, 336], radius=8, outline="#90caf9", width=2)
    d.text((82, 162), "main() frame", fill="#555", font=f)
    d.text((82, 202), "int x = 5;", fill="#111", font=fm)
    d.text((82, 234), "Person p = new Person();", fill="#111", font=fm)
    d.text((82, 284), "x  ->  5", fill="#0d47a1", font=fm)
    d.text((82, 314), "p  ->  reference", fill="#c62828", font=fm)
    d.text((66, 396), "locals + references", fill="#666", font=f)
    d.text((66, 426), "freed when the frame exits", fill="#666", font=f)

    d.rounded_rectangle([490, 90, 900, 470], radius=12, outline="#2e7d32", width=3)
    d.text((510, 102), "HEAP  (shared by threads)", fill="#2e7d32", font=f_h)
    d.rounded_rectangle([516, 160, 874, 340], radius=8, outline="#a5d6a7", width=2)
    d.text((532, 172), "Person object", fill="#555", font=f)
    d.text((532, 212), 'name  = "Ana"', fill="#111", font=fm)
    d.text((532, 244), "age   = 31", fill="#111", font=fm)
    d.text((532, 288), "class ptr -> Person.class", fill="#111", font=fm)
    d.text((516, 396), "all objects and arrays", fill="#666", font=f)
    d.text((516, 426), "reclaimed only by the GC", fill="#666", font=f)

    d.line([(388, 318), (508, 250)], fill="#c62828", width=3)
    d.polygon([(498, 240), (516, 248), (500, 260)], fill="#c62828")

    d.text((40, 520), "assignment copies the reference, never the object", fill="#777", font=f)
    d.text((40, 556), "an object is collectable when no live reference reaches it", fill="#777", font=f)
    img.save(os.path.join(MEDIA, "stack-heap.png"))


if __name__ == "__main__":
    jdk_jre_jvm()
    landscape()
    stack_heap()
    print("wrote", [f for f in sorted(os.listdir(MEDIA)) if f.endswith(".png")])
