"""Montagem das peças SVG (claro/escuro) e helpers de texto."""
from html import escape
from pathlib import Path
from typing import Callable

from . import texto as _texto
from .marca import TEMAS

SEM_MOVIMENTO = (
    "@media (prefers-reduced-motion: reduce){*{animation:none!important;"
    "transition:none!important}}"
)


def peca(largura: int, altura: int, corpo: str, tema: str, css: str = "", titulo: str = "",
         fundo: bool = True, raio: int = 24) -> str:
    t = TEMAS[tema]
    bg = f'<rect width="{largura}" height="{altura}" rx="{raio}" fill="{t["fundo"]}"/>' if fundo else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largura} {altura}" '
        f'width="{largura}" height="{altura}" role="img">'
        f"<title>{escape(titulo)}</title>"
        f"<style>{css}{SEM_MOVIMENTO}</style>"
        f"{bg}{corpo}</svg>"
    )


def salvar(nome: str, gerar: Callable[[str], str], pasta: Path) -> list:
    pasta.mkdir(parents=True, exist_ok=True)
    saida = []
    for tema in ("claro", "escuro"):
        p = pasta / f"{nome}-{tema}.svg"
        p.write_text(gerar(tema), encoding="utf-8")
        saida.append(p)
    return saida


def linha(txt: str, x: float, y: float, tamanho: float, cor: str, peso: int = 400,
          tracking: float = 0.0, classe: str = "", ancora: str = "inicio") -> str:
    """Um <path> de texto. ancora: inicio | meio | fim."""
    _, w = _texto.caminho(txt, tamanho, peso, tracking)
    if ancora == "meio":
        x -= w / 2
    elif ancora == "fim":
        x -= w
    d, _ = _texto.caminho(txt, tamanho, peso, tracking, x=x, y=y)
    cls = f' class="{classe}"' if classe else ""
    return f'<path{cls} d="{d}" fill="{cor}"/>'


def quebrar(txt: str, tamanho: float, largura_max: float, peso: int = 400, tracking: float = 0.0) -> list:
    """Quebra em linhas que cabem em largura_max (medida real da Geologica)."""
    linhas, atual = [], ""
    for palavra in txt.split():
        tentativa = f"{atual} {palavra}".strip()
        if atual and _texto.largura(tentativa, tamanho, peso, tracking) > largura_max:
            linhas.append(atual)
            atual = palavra
        else:
            atual = tentativa
    if atual:
        linhas.append(atual)
    return linhas


def caber(txt: str, tamanho: float, largura_max: float, peso: int = 400, tracking: float = 0.0,
          minimo: float = 10) -> float:
    """Maior tamanho <= tamanho em que txt cabe numa linha."""
    while tamanho > minimo and _texto.largura(txt, tamanho, peso, tracking) > largura_max:
        tamanho -= 1
    return tamanho


def paragrafo(linhas: list, x: float, y: float, tamanho: float, cor: str, peso: int = 400,
              entrelinha: float = 1.3, tracking: float = 0.0, classe: str = "") -> str:
    return "".join(
        linha(l, x, y + i * tamanho * entrelinha, tamanho, cor, peso, tracking, classe)
        for i, l in enumerate(linhas)
    )
