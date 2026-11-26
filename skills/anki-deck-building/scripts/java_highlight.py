# -*- coding: utf-8 -*-
"""Java tokeniser for Anki fields -> <span class="kw|type|fn|str|chr|num|cmt|ann|lit">.

Usage:
    from java_highlight import highlight_fields
    note_fields = [highlight_fields(f) for f in [front, back, extra]]

Only the inside of <code>/<pre> is touched. Cloze markers {{c1:: ... }} pass through
untouched so Anki still recognises them. Add class="nohl" to a tag to opt out.

Styling lives in the note type CSS; see references/card-patterns.md for the palette.
"""
import html
import re

KEYWORDS = {
    "abstract", "assert", "boolean", "break", "byte", "case", "catch", "char",
    "class", "const", "continue", "default", "do", "double", "else", "enum",
    "extends", "final", "finally", "float", "for", "goto", "if", "implements",
    "import", "instanceof", "int", "interface", "long", "native", "new",
    "package", "private", "protected", "public", "return", "short", "static",
    "strictfp", "super", "switch", "synchronized", "this", "throw", "throws",
    "transient", "try", "void", "volatile", "while", "var", "record", "sealed",
    "permits", "yield", "true", "false", "null",
}
LITERALS = {"true", "false", "null"}

TOKEN = re.compile(r"""
    (?P<cloze_open>\{\{c\d+::)          |
    (?P<cloze_close>\}\})               |
    (?P<comment>//[^\n]*|/\*.*?\*/)     |
    (?P<string>"(?:\\.|[^"\\])*")       |
    (?P<char>'(?:\\.|[^'\\])*')         |
    (?P<annotation>@[A-Za-z_]\w*)       |
    (?P<number>\b(?:0[xX][0-9a-fA-F_]+|\d[\d_]*(?:\.\d+)?[fFdDlL]?)\b) |
    (?P<ident>[A-Za-z_$][\w$]*)         |
    (?P<ws>\s+)                         |
    (?P<other>.)
""", re.S | re.X)


def _looks_like_type(src, pos):
    """A capitalised identifier is a type only when something binding follows it:
    another identifier, '<', '[', '(', '.'. Keeps short answers like 'Bea' plain."""
    rest = src[pos:pos + 40].lstrip()
    if not rest:
        return False
    return rest[0].isalnum() or rest[0] in "_$<[(" or rest[0] == "."


def _span(cls, text):
    return f'<span class="{cls}">{html.escape(text, quote=False)}</span>'


def highlight_java(src):
    """src is RAW java text, not yet HTML-escaped."""
    out, prev = [], ""
    for m in TOKEN.finditer(src):
        kind, text = m.lastgroup, m.group(0)
        if kind in ("cloze_open", "cloze_close"):
            out.append(text)
            continue
        if kind == "comment":
            out.append(_span("cmt", text))
        elif kind == "string":
            out.append(_span("str", text))
        elif kind == "char":
            out.append(_span("chr", text))
        elif kind == "annotation":
            out.append(_span("ann", text))
        elif kind == "number":
            out.append(_span("num", text))
        elif kind == "ident":
            if text in LITERALS:
                out.append(_span("lit", text))
            elif text in KEYWORDS:
                out.append(_span("kw", text))
            elif text[0].isupper() and _looks_like_type(src, m.end()):
                out.append(_span("type", text))
            elif prev == "." or re.match(r"\s*\(", src[m.end():]):
                out.append(_span("fn", text))
            else:
                out.append(html.escape(text, quote=False))
        else:
            out.append(html.escape(text, quote=False))
        if kind != "ws":
            prev = text
    return "".join(out)


BLOCK = re.compile(r"(<(code|pre)(\s[^>]*)?>)(.*?)(</\2>)", re.S | re.I)


def highlight_fields(text):
    """Highlight every <code>/<pre> block in one HTML field."""
    def repl(m):
        open_tag, attrs, body, close_tag = m.group(1), m.group(3) or "", m.group(4), m.group(5)
        if "nohl" in attrs:
            return m.group(0)
        body = re.sub(r"</?span[^>]*>", "", body)
        for ent, ch in (("&lt;", "<"), ("&gt;", ">"), ("&amp;", "&"), ("&quot;", '"'), ("&#39;", "'")):
            body = body.replace(ent, ch)
        return f"{open_tag}{highlight_java(body)}{close_tag}"
    return BLOCK.sub(repl, text)


if __name__ == "__main__":
    demo = '<pre>Person a = new Person("Ana");\nfor (int i = 0; i &lt; 3; i++) { /* loop */ }</pre>'
    print(highlight_fields(demo))
