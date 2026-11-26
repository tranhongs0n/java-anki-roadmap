# -*- coding: utf-8 -*-
"""Minimal AnkiConnect client (POST http://127.0.0.1:8765, protocol v6)."""
import json
import urllib.error
import urllib.request

URL = "http://127.0.0.1:8765"


class AnkiError(RuntimeError):
    pass


def call(action, **params):
    body = json.dumps({"action": action, "version": 6, "params": params}).encode("utf-8")
    req = urllib.request.Request(URL, data=body,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            resp = json.loads(r.read().decode("utf-8"))
    except urllib.error.URLError as e:
        raise AnkiError(
            "Cannot reach Anki on 127.0.0.1:8765.\n"
            "Open Anki, keep it running, and check that the AnkiConnect add-on "
            "(2055492159) is installed and enabled."
        ) from e
    if resp.get("error"):
        raise AnkiError(f"{action}: {resp['error']}")
    return resp.get("result")


# --- thin wrappers -----------------------------------------------------------

def version():
    return call("version")


def deck_names():
    return call("deckNames")


def create_deck(name):
    return call("createDeck", deck=name)


def model_names():
    return call("modelNames")


def model_fields(name):
    return call("modelFieldNames", modelName=name)


def create_model(name, fields, templates, css, is_cloze=False):
    return call("createModel", modelName=name, inOrderFields=fields,
                css=css, isCloze=bool(is_cloze), cardTemplates=templates)


def add_field(name, field):
    return call("modelFieldAdd", modelName=name, fieldName=field)


def update_styling(name, css):
    return call("updateModelStyling", model={"name": name, "css": css})


def store_media(filename, data_b64):
    return call("storeMediaFile", filename=filename, data=data_b64)


def media_names(pattern="*"):
    return call("getMediaFilesNames", pattern=pattern)


def add_notes(notes):
    return call("addNotes", notes=notes)


def update_note_fields(note_id, fields):
    return call("updateNoteFields", note={"id": note_id, "fields": fields})


def find_notes(query):
    return call("findNotes", query=query)


def notes_info(note_ids):
    return call("notesInfo", notes=note_ids)


def gui_browse(query):
    return call("guiBrowse", query=query)
