# -*- coding: utf-8 -*-
"""Generate decks.json: the numbered, nested deck tree for roadmap.sh/java."""
import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = "00 Java Roadmap"

SECTIONS = [
    ("01 Foundations", "Syntax, types, control flow, how a program runs", [
        "learn-the-basics", "basic-syntax", "data-types", "conditionals", "arrays", "loops",
        "variables-and-scopes", "type-casting", "strings-and-methods",
        "math-operations", "lifecycle-of-a-program",
    ]),
    ("02 Object Model", "Classes, objects, inheritance, interfaces, access", [
        "classes-and-objects", "attributes-and-methods", "access-specifiers",
        "static-keyword", "nested-classes", "basics-of-oop", "object-lifecycle",
        "method-chaining", "enums", "final-keyword", "abstraction", "inheritance",
        "method-overloading--overriding", "static-vs-dynamic-binding", "interfaces",
        "encapsulation", "record", "packages", "initializer-block",
        "pass-by-value--pass-by-reference",
    ]),
    ("03 Language Features", "Exceptions, annotations, lambdas, modules", [
        "exception-handling", "annotations", "lambda-expressions", "modules",
    ]),
    ("04 Collections", "List, Set, Map, Queue, iterators, optionals", [
        "array-vs-arraylist", "set", "map", "queue", "stack", "dequeue",
        "iterator", "generic-collections", "optionals",
    ]),
    ("05 Functional Programming", "Functional interfaces, streams, composition", [
        "functional-interfaces", "high-order-functions",
        "functional-composition", "stream-api",
    ]),
    ("06 Concurrency", "Threads, virtual threads, memory model, volatile", [
        "concurrency", "threads", "virtual-threads", "java-memory-model",
        "volatile-keyword",
    ]),
    ("07 IO, Network, Data Formats", "Files, sockets, crypto, dates, regex", [
        "io-operations", "file-operations", "networking", "cryptography",
        "date-and-time", "regular-expressions",
    ]),
    ("08 Persistence", "JDBC, JPA, Hibernate, EBean", [
        "database-access", "jdbc", "spring-data-jpa", "hibernate", "ebean",
    ]),
    ("09 Build and Frameworks", "Maven, Gradle, DI, Spring, Quarkus, Javalin", [
        "build-tools", "maven", "gradle", "bazel", "dependency-injection",
        "web-frameworks", "spring-spring-boot", "quarkus", "play-framework",
        "javalin",
    ]),
    ("10 Testing", "Unit, integration, behaviour tests, mocking, load", [
        "testing", "junit", "testng", "rest-assured", "jmeter", "cucumber-jvm",
        "mocking--mockito",
    ]),
    ("11 Logging", "Logging frameworks and bindings", [
        "logging-frameworks", "logback", "log4j2", "slf4j", "tinylog",
    ]),
    ("12 Documentation", "Javadoc conventions", [
        "documentation", "javadoc",
    ]),
]


def clean(name):
    """Deck-safe title: no path separators, no '::', ASCII only."""
    name = name.replace(" / ", " vs ").replace("/", "-")
    name = re.sub(r'[\\:*?"<>|]', "-", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name


LEVEL0 = {
    "n": "00",
    "deck": "00 Big Picture",
    "deck_path": f"{ROOT}::00 Big Picture",
    "desc": "The whole roadmap on one page: what each area is for, how they depend on each other",
    "cards": 19, "topics": [],
}


def main():
    docs = json.load(open(os.path.join(BASE, "docs.json"), encoding="utf-8"))
    by_slug = {d["slug"]: d for d in docs}
    used = set()
    tree = {"deck": ROOT, "deck_path": ROOT, "sections": [LEVEL0]}

    for s_i, (sec_name, sec_desc, slugs) in enumerate(SECTIONS, start=1):
        sec = {"n": f"{s_i:02d}", "deck": sec_name,
               "deck_path": f"{ROOT}::{sec_name}", "desc": sec_desc, "topics": []}
        # level 1: the section skeleton, written when you start that section
        sec["topics"].append({
            "n": "00", "deck": "00 Overview", "title": "Overview",
            "deck_path": f"{ROOT}::{sec_name}::00 Overview",
            "slug": f"overview-{s_i:02d}", "source_md": "", "summary": sec_desc,
            "resources": [], "n_resources": 0, "synthetic": True,
        })
        for t_i, slug in enumerate(slugs, start=1):
            d = by_slug.get(slug)
            if d is None:
                raise SystemExit(f"missing doc: {slug}")
            used.add(slug)
            title = clean(d["title"])
            topic_deck = f"{t_i:02d} {title}"
            sec["topics"].append({
                "n": f"{t_i:02d}",
                "deck": topic_deck,
                "deck_path": f"{ROOT}::{sec_name}::{topic_deck}",
                "title": title,
                "slug": slug,
                "source_md": f"https://github.com/nilbuild/developer-roadmap/blob/master/roadmaps/java/content/{d['file']}",
                "resources": [{"type": r[0], "label": r[1], "url": r[2]} for r in d["res"]],
                "n_resources": d["n_res"],
                "summary": d["desc"][:600],
            })
        tree["sections"].append(sec)

    missing = sorted(set(by_slug) - used)
    if missing:
        raise SystemExit(f"unmapped docs: {missing}")

    json.dump(tree, open(os.path.join(BASE, "decks.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    n_topics = sum(len(s["topics"]) for s in tree["sections"])
    print(f"{len(tree['sections'])} sections, {n_topics} topic decks "
          f"(incl. 12 section overviews + 00 Big Picture)")


if __name__ == "__main__":
    main()
