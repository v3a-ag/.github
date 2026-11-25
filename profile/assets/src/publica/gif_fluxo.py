"""GIF 'do pedido ao uso': quatro passos que acendem em sequência (Pillow + Geologica)."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from gerador import marca

PASSOS = ["Uma área pede", "A gente desenha", "Entra em produção", "O time usa"]
TITULO = "Do pedido ao uso"
L, A, K = 880, 360, 2  # desenha em 2x e reduz (antialias)
FPS = 12
PAGINA = {"claro": "#FFFFFF", "escuro": "#0D1117"}  # fundo do GitHub em cada tema


def _fonte(tamanho: int, peso: int) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(str(marca.RECURSOS / "Geologica.ttf"), tamanho * K)
    f.set_variation_by_axes([peso, 0, 0, 0])
    return f


def _hex(c: str):
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def _icone(d: ImageDraw.ImageDraw, i: int, cx: float, cy: float, cor, acento):
    s, w = K, 4 * K
    if i == 0:  # balão
        d.rounded_rectangle([cx - 22 * s, cy - 18 * s, cx + 22 * s, cy + 10 * s], 6 * s, outline=cor, width=w)
        d.polygon([(cx - 10 * s, cy + 10 * s), (cx - 16 * s, cy + 22 * s), (cx, cy + 10 * s)], fill=cor)
        d.line([cx - 12 * s, cy - 6 * s, cx + 12 * s, cy - 6 * s], fill=acento, width=w)
    elif i == 1:  # lápis
        d.line([cx - 18 * s, cy + 18 * s, cx + 14 * s, cy - 14 * s], fill=cor, width=10 * s)
        d.line([cx + 8 * s, cy - 20 * s, cx + 20 * s, cy - 8 * s], fill=acento, width=w)
    elif i == 2:  # play / produção
        d.polygon([(cx - 12 * s, cy - 18 * s), (cx - 12 * s, cy + 18 * s), (cx + 18 * s, cy)], outline=cor, width=w)
        d.ellipse([cx - 4 * s, cy - 4 * s, cx + 4 * s, cy + 4 * s], fill=acento)
    else:  # time
        for dx in (-11, 11):
            d.ellipse([cx + (dx - 7) * s, cy - 20 * s, cx + (dx + 7) * s, cy - 6 * s], outline=cor, width=w)
        d.arc([cx - 26 * s, cy - 2 * s, cx + 4 * s, cy + 28 * s], 180, 360, fill=cor, width=w)
        d.arc([cx - 4 * s, cy - 2 * s, cx + 26 * s, cy + 28 * s], 180, 360, fill=acento, width=w)


def _quadro(tema: str, ativo: int, progresso: float) -> Image.Image:
    """ativo = passo aceso mais adiantado (-1 = nenhum); progresso 0..1 da linha até o próximo."""
    t = {k: _hex(v) for k, v in marca.TEMAS[tema].items()}
    im = Image.new("RGB", (L * K, A * K), _hex(PAGINA[tema]))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, L * K - 1, A * K - 1], 13 * K, fill=t["fundo"])
    d.text((48 * K, 40 * K), TITULO, font=_fonte(34, 800), fill=t["texto"])
    d.rounded_rectangle([48 * K, 92 * K, 128 * K, 98 * K], 3 * K, fill=t["acento"])
    xs = [L * (i + 0.5) / 4 for i in range(4)]
    cy, r = 196, 46
    for i in range(3):  # trilhos
        x1, x2 = (xs[i] + r) * K, (xs[i + 1] - r) * K
        d.line([x1, cy * K, x2, cy * K], fill=t["borda"], width=3 * K)
        feito = 1.0 if i < ativo else (progresso if i == ativo else 0.0)
        if feito > 0:
            d.line([x1, cy * K, x1 + (x2 - x1) * feito, cy * K], fill=t["acento"], width=6 * K)
    rotulo = _fonte(20, 700)
    for i, x in enumerate(xs):
        aceso = i <= ativo
        caixa = [(x - r) * K, (cy - r) * K, (x + r) * K, (cy + r) * K]
        d.ellipse(caixa, fill=t["superficie"] if aceso else t["fundo"],
                  outline=t["acento"] if aceso else t["borda"], width=(6 if aceso else 3) * K)
        _icone(d, i, x * K, cy * K, t["texto"] if aceso else t["borda"], t["acento"] if aceso else t["borda"])
        d.text((x * K, (cy + r + 34) * K), PASSOS[i], font=rotulo, anchor="mt",
               fill=t["texto"] if aceso else t["borda"])
    return im.resize((L, A), Image.LANCZOS)


def _sequencia(tema: str):
    quadros = []  # (imagem, duração ms)
    quadros.append((_quadro(tema, -1, 0), 700))
    for passo in range(4):
        quadros.append((_quadro(tema, passo, 0), 900))
        if passo < 3:
            n = 6
            for k in range(1, n + 1):
                quadros.append((_quadro(tema, passo, k / n), int(1000 / FPS)))
    quadros.append((_quadro(tema, 3, 0), 2200))
    return quadros


def gerar(pasta: Path) -> list:
    pasta.mkdir(parents=True, exist_ok=True)
    saida = []
    for tema in ("claro", "escuro"):
        seq = _sequencia(tema)
        imgs = [q.quantize(colors=64, method=Image.MEDIANCUT) for q, _ in seq]
        p = pasta / f"fluxo-{tema}.gif"
        imgs[0].save(p, save_all=True, append_images=imgs[1:], duration=[ms for _, ms in seq],
                     loop=0, optimize=True, disposal=1)
        saida.append(p)
    return saida


if __name__ == "__main__":
    import sys
    for p in gerar(Path(sys.argv[1] if len(sys.argv) > 1 else "saida")):
        print(p)
