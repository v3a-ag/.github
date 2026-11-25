"""Converte texto em Geologica para contorno SVG (<path>), sem depender de fonte instalada."""
from functools import lru_cache

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

from .marca import RECURSOS


def _num(v: float) -> str:
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


@lru_cache(maxsize=1)
def _fonte() -> TTFont:
    return TTFont(RECURSOS / "Geologica.ttf")


@lru_cache(maxsize=None)
def _glyphset(peso: int):
    return _fonte().getGlyphSet(location={"wght": peso, "CRSV": 0, "SHRP": 0, "slnt": 0})


def _cmap():
    return _fonte().getBestCmap()


def largura(texto: str, tamanho: float, peso: int = 400, tracking: float = 0.0) -> float:
    return caminho(texto, tamanho, peso, tracking)[1]


def caminho(texto: str, tamanho: float, peso: int = 400, tracking: float = 0.0, x: float = 0, y: float = 0):
    """Retorna (d, largura). `y` é a linha de base; `tracking` em em (ex.: -0.02 = -2%)."""
    gs = _glyphset(peso)
    cmap = _cmap()
    upem = _fonte()["head"].unitsPerEm
    escala = tamanho / upem
    pen = SVGPathPen(gs, ntos=_num)
    cursor = 0.0
    for i, ch in enumerate(texto):
        nome = cmap.get(ord(ch), ".notdef")
        glifo = gs[nome]
        glifo.draw(TransformPen(pen, (escala, 0, 0, -escala, x + cursor, y)))
        cursor += glifo.width * escala
        if i < len(texto) - 1:
            cursor += tracking * tamanho
    return pen.getCommands(), cursor
