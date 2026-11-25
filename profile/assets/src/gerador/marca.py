"""Tokens da marca V3A (manual: marca-v3a.figma.site) e o logo oficial."""
import re
from functools import lru_cache
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.svgLib.path import parse_path

RECURSOS = Path(__file__).parent / "recursos"

CORES = {
    "branco": "#FFFFFF",
    "nuvem": "#F0F0F0",
    "amarelo": "#FFCB05",
    "cinza_claro": "#A4A6A9",
    "cinza_escuro": "#636466",
    "preto": "#000000",
}

# Pares do manual: "Cinza Escuro - Nuvem" (claro) e "Nuvem - Cinza Escuro" (escuro).
TEMAS = {
    "claro": {
        "fundo": CORES["nuvem"],
        "superficie": CORES["branco"],
        "texto": CORES["cinza_escuro"],
        "texto_suave": CORES["cinza_escuro"],
        "acento": CORES["amarelo"],
        "borda": CORES["cinza_claro"],
    },
    "escuro": {
        "fundo": CORES["cinza_escuro"],
        "superficie": CORES["preto"],
        "texto": CORES["branco"],
        "texto_suave": CORES["nuvem"],
        "acento": CORES["amarelo"],
        "borda": CORES["cinza_claro"],
    },
}

_ARQUIVOS = {
    "institucional": "logo-institucional.svg",
    "monograma": "logo-monograma.svg",
}


@lru_cache(maxsize=None)
def _paths_do_logo(versao: str):
    """Lista de (d, cor_original) do SVG oficial, sem o retângulo de fundo."""
    bruto = (RECURSOS / _ARQUIVOS[versao]).read_text(encoding="utf-8")
    paths = []
    for m in re.finditer(r'<path d="([^"]+)" fill="var\(--fill-0, (#[0-9A-Fa-f]{6})\)"', bruto):
        paths.append((m.group(1), m.group(2).upper()))
    pen = BoundsPen(None)
    for d, _ in paths:
        parse_path(d, pen)
    return paths, pen.bounds


def logo_paths(versao: str, tema: str):
    """Fragmento SVG do logo com origem em (0,0) e o tamanho natural (w, h).

    O cinza do logo vira a cor de texto do tema; o "3" fica Amarelo.
    """
    paths, (x0, y0, x1, y1) = _paths_do_logo(versao)
    cor_texto = TEMAS[tema]["texto"]
    partes = []
    for d, cor in paths:
        fill = CORES["amarelo"] if cor == "#FFC600" else cor_texto
        partes.append(f'<path d="{d}" fill="{fill}"/>')
    frag = f'<g transform="translate({-x0:.3f} {-y0:.3f})">{"".join(partes)}</g>'
    return frag, (x1 - x0, y1 - y0)
