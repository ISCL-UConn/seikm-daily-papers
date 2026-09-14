"""Phrase matching over paper text.

Design notes
------------
* Matching is whole-word, so "CAD" never fires inside "cadence".
* Hyphens, slashes and underscores are normalised to spaces on BOTH the term
  and the text, so "physics-informed" matches "physics informed" and vice versa.
* A term written as an all-caps acronym in the config ("MBSE", "PINN", "CAD",
  "RAG") is matched case-SENSITIVELY. Without this, "RAG" matches the English
  word "rag" and "CAD" matches nothing useful. Terms with any lowercase letter
  ("Industry 4.0", "SysML", "digital twin") are matched case-insensitively.
* A trailing plural is tolerated on the last word ("robot" matches "robots").
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache

_SEPARATORS = re.compile(r"[-_/‐-―]+")
_WHITESPACE = re.compile(r"\s+")


def normalize(text: str) -> str:
    """Fold separators and whitespace so phrase matching is robust."""
    if not text:
        return ""
    text = _SEPARATORS.sub(" ", text)
    text = _WHITESPACE.sub(" ", text)
    return text.strip()


def is_acronym(term: str) -> bool:
    """True when the term's letters are all uppercase (MBSE, OPC UA, PINN)."""
    letters = [c for c in term if c.isalpha()]
    return bool(letters) and all(c.isupper() for c in letters)


@lru_cache(maxsize=4096)
def compile_term(term: str) -> tuple[re.Pattern, bool]:
    """Compile a phrase into a whole-word regex. Returns (pattern, case_sensitive)."""
    cased = is_acronym(term)
    norm = normalize(term)
    words = [re.escape(w) for w in norm.split(" ") if w]
    if not words:
        return re.compile(r"(?!x)x"), cased
    # Tolerate a plural on the final word.
    words[-1] = words[-1] + r"(?:s|es)?"
    body = r"\s+".join(words)
    pattern = r"(?<![A-Za-z0-9])" + body + r"(?![A-Za-z0-9])"
    flags = 0 if cased else re.IGNORECASE
    return re.compile(pattern, flags), cased


@dataclass(frozen=True)
class Hit:
    term: str
    in_title: bool


class TextIndex:
    """Pre-normalised title/abstract pair, matched against many terms."""

    __slots__ = ("title", "body", "combined")

    def __init__(self, title: str, abstract: str) -> None:
        self.title = normalize(title or "")
        self.body = normalize(abstract or "")
        self.combined = f"{self.title} . {self.body}"

    def find(self, term: str) -> Hit | None:
        pattern, _ = compile_term(term)
        if not pattern.search(self.combined):
            return None
        return Hit(term=term, in_title=bool(pattern.search(self.title)))
