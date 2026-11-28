# -*- coding: utf-8 -*-
"""Minimal Java syntax highlighter for Anki fields.

Usage:  highlight_fields(html) -> html

Only text inside <code>...</code> and <pre>...</pre> is touched. Cloze markers
({{c1:: ... }}) inside code are passed through untouched so Anki still works.
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
    "permits", "yield", "non-sealed", "true", "false", "null",
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
    """A capitalised identifier is a type only if something follows that binds
    to a type: another identifier, '<', '[', '(', '.', or a vararg/closing paren."""
    rest = src[pos:pos + 40].lstrip()
    if not rest:
        return False
    return rest[0].isalnum() or rest[0] in "_$<[(" or rest[0] == "."


def _span(cls, text):
    return f'<span class="{cls}">{html.escape(text, quote=False)}</span>'


def highlight_java(src):
    """src is RAW java text (not yet escaped)."""
    out = []
    prev_significant = ""
    for m in TOKEN.finditer(src):
        kind = m.lastgroup
        text = m.group(0)
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
            elif prev_significant == "." and re.match(r"\w", src[m.end():m.end() + 1] or ""):
                out.append(_span("fn", text))
            elif re.match(r"\s*\(", src[m.end():]):
                out.append(_span("fn", text))
            else:
                out.append(html.escape(text, quote=False))
        else:
            out.append(html.escape(text, quote=False))
        if kind != "ws":
            prev_significant = text
    return "".join(out)


BLOCK = re.compile(r"(<(code|pre)(\s[^>]*)?>)(.*?)(</\2>)", re.S | re.I)


def highlight_fields(text):
    """Highlight every <code>/<pre> block in an HTML field."""
    def repl(m):
        open_tag, tag, attrs, body, close_tag = m.group(1), m.group(2), m.group(3) or "", m.group(4), m.group(5)
        if "nohl" in attrs:
            return m.group(0)
        # strip tags that may already exist inside, keep cloze markers.
        # Emphasis tags must go too: a code block is plain text, and leaving <b>/<i>
        # in makes the highlighter escape them, so the learner sees literal "<b>".
        body = re.sub(r"</?span[^>]*>", "", body)
        body = re.sub(r"</?(b|i|strong|em|u|s|small|big|mark|font)\b[^>]*>", "", body, flags=re.I)
        body = body.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
        body = body.replace("&quot;", '"').replace("&#39;", "'")
        return f"{open_tag}{highlight_java(body)}{close_tag}"
    return BLOCK.sub(repl, text)


if __name__ == "__main__":
    demo = '<pre>Person a = new Person("Ana");\nfor (int i = 0; i &lt; 3; i++) { /* loop */ }\n// done</pre>'
    print(highlight_fields(demo))
