"""Turn arXiv's TeX-flavoured metadata into readable Unicode.

arXiv feeds carry author names and titles exactly as the submitter typed them
in LaTeX: ``Jo\~ao``, ``Krist\'ina``, ``\"Ostlund``, ``$\beta$ Titanium``. Left
alone those land in the digest verbatim and look broken.

This is deliberately a readability pass, not a TeX engine. Anything it does not
recognise is left as plain text rather than mangled further.
"""
from __future__ import annotations

import re
import unicodedata

# \'e  \"o  \~a  \`e  \^e  \=a  \.z  — accent applied to the following letter
_COMBINING = {
    "'": "\u0301",   # acute
    "`": "\u0300",   # grave
    '"': "\u0308",   # diaeresis
    "^": "\u0302",   # circumflex
    "~": "\u0303",   # tilde
    "=": "\u0304",   # macron
    ".": "\u0307",   # dot above
    "u": "\u0306",   # breve
    "v": "\u030C",   # caron
    "H": "\u030B",   # double acute
    "c": "\u0327",   # cedilla
    "k": "\u0328",   # ogonek
    "d": "\u0323",   # dot below
    "b": "\u0331",   # macron below
    "r": "\u030A",   # ring above
}

# Standalone letter commands.
_LITERAL = {
    r"\ss": "ß", r"\aa": "å", r"\AA": "Å", r"\o": "ø", r"\O": "Ø",
    r"\l": "ł", r"\L": "Ł", r"\ae": "æ", r"\AE": "Æ", r"\oe": "œ",
    r"\OE": "Œ", r"\i": "ı", r"\j": "ȷ", r"\dh": "ð", r"\th": "þ",
    r"\dag": "†", r"\ddag": "‡", r"\pounds": "£", r"\copyright": "©",
    r"\textendash": "–", r"\textemdash": "—", r"\ldots": "…",
    r"\&": "&", r"\%": "%", r"\$": "$", r"\#": "#", r"\_": "_",
}

_GREEK = {
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "epsilon": "ε",
    "zeta": "ζ", "eta": "η", "theta": "θ", "iota": "ι", "kappa": "κ",
    "lambda": "λ", "mu": "μ", "nu": "ν", "xi": "ξ", "pi": "π", "rho": "ρ",
    "sigma": "σ", "tau": "τ", "upsilon": "υ", "phi": "φ", "chi": "χ",
    "psi": "ψ", "omega": "ω",
    "Gamma": "Γ", "Delta": "Δ", "Theta": "Θ", "Lambda": "Λ", "Xi": "Ξ",
    "Pi": "Π", "Sigma": "Σ", "Upsilon": "Υ", "Phi": "Φ", "Psi": "Ψ",
    "Omega": "Ω",
    "times": "×", "cdot": "·", "pm": "±", "approx": "≈", "leq": "≤",
    "geq": "≥", "neq": "≠", "rightarrow": "→", "to": "→", "infty": "∞",
    "degree": "°", "circ": "°", "sim": "~", "propto": "∝", "in": "∈",
}

# \'{e} or \'e   |   \c{c}   |   \v{s}
_ACCENT_BRACED = re.compile(r"\\([`'\"^~=.uvHckdbr])\{(\\?[A-Za-z])\}")
_ACCENT_BARE = re.compile(r"\\([`'\"^~=.])\s*(\\?[A-Za-z])")
_ACCENT_WORD = re.compile(r"\\([uvHckdbr])\s+([A-Za-z])")
# \textit{x}, \emph{x}, \mathrm{x}, \text{x} ...
_WRAPPER = re.compile(
    r"\\(?:emph|textit|textbf|textrm|textsc|texttt|textsf|mathrm|mathbf|"
    r"mathit|mathcal|mathbb|text|bm|boldsymbol|operatorname)\s*\{([^{}]*)\}"
)
_GREEK_CMD = re.compile(r"\\([A-Za-z]+)")
_MATH = re.compile(r"\$+([^$]*)\$+")
_SUP = re.compile(r"\^\{?([0-9n+\-]+)\}?")
_SUB = re.compile(r"_\{?([0-9n+\-]+)\}?")
_BRACES = re.compile(r"[{}]")
_WS = re.compile(r"\s+")

_SUPS = str.maketrans("0123456789n+-", "⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ⁺⁻")
_SUBS = str.maketrans("0123456789n+-", "₀₁₂₃₄₅₆₇₈₉ₙ₊₋")


def _apply_accent(mark: str, letter: str) -> str:
    letter = letter.lstrip("\\")
    if letter in ("i", "j"):          # \'{\i} -> í, dotless i takes the accent
        letter = letter
    combining = _COMBINING.get(mark)
    if not combining:
        return letter
    return unicodedata.normalize("NFC", letter + combining)


def detex(text: str) -> str:
    """Best-effort LaTeX -> Unicode for titles, abstracts and author names."""
    if not text or "\\" not in text and "$" not in text and "{" not in text:
        return _WS.sub(" ", text or "").strip()

    out = text
    out = _WRAPPER.sub(r"\1", out)
    out = _ACCENT_BRACED.sub(lambda m: _apply_accent(m.group(1), m.group(2)), out)
    out = _ACCENT_WORD.sub(lambda m: _apply_accent(m.group(1), m.group(2)), out)
    out = _ACCENT_BARE.sub(lambda m: _apply_accent(m.group(1), m.group(2)), out)

    for cmd, repl in _LITERAL.items():
        out = out.replace(cmd + "{}", repl).replace(cmd, repl)

    # Inside math, render sub/superscripts before the braces are stripped.
    def _math(m: re.Match) -> str:
        inner = m.group(1)
        inner = _SUP.sub(lambda s: s.group(1).translate(_SUPS), inner)
        inner = _SUB.sub(lambda s: s.group(1).translate(_SUBS), inner)
        return inner

    out = _MATH.sub(_math, out)
    out = _GREEK_CMD.sub(lambda m: _GREEK.get(m.group(1), m.group(1)), out)
    out = _BRACES.sub("", out)
    out = out.replace("\\", "")
    return _WS.sub(" ", out).strip()


def clean_authors(names: list[str]) -> list[str]:
    """detex each name and drop the affiliations arXiv sometimes inlines."""
    cleaned: list[str] = []
    for raw in names:
        name = detex(raw)
        # "Matthieu Rauch (Nantes Univ - ECN, GeM)" -> "Matthieu Rauch"
        name = re.sub(r"\s*\([^)]*\)\s*$", "", name).strip()
        name = re.sub(r"\s*\([^)]*$", "", name).strip()   # unbalanced tail
        if name and name not in cleaned:
            cleaned.append(name)
    return cleaned
