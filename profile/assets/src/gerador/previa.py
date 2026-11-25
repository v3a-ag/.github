"""Prévia local: monta um HTML com peças e tira um print com o Chrome headless.

Uso: python -m gerador.previa saida.png largura arquivo1.svg arquivo2.gif ...
Cada arquivo -claro aparece sobre fundo branco (GitHub claro) e cada -escuro sobre #0d1117.
"""
import subprocess
import sys
from pathlib import Path

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def html(arquivos: list, largura: int = 830) -> str:
    blocos = []
    for a in arquivos:
        a = Path(a).resolve()
        fundo = "#0d1117" if "-escuro" in a.name else "#ffffff"
        blocos.append(
            f'<div style="background:{fundo};padding:12px">'
            f'<img src="file://{a}" style="width:{largura}px;display:block"></div>'
        )
    return f'<html><body style="margin:0">{"".join(blocos)}</body></html>'


def print_(saida: str, arquivos: list, largura: int = 830, altura: int = 2400, espera_ms: int = 2500) -> Path:
    saida = Path(saida).resolve()
    pagina = saida.with_suffix(".html")
    pagina.write_text(html(arquivos, largura), encoding="utf-8")
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
         f"--window-size={largura + 24},{altura}", f"--virtual-time-budget={espera_ms}",
         f"--screenshot={saida}", f"file://{pagina}"],
        check=True, capture_output=True,
    )
    return saida


if __name__ == "__main__":
    print(print_(sys.argv[1], sys.argv[3:], int(sys.argv[2])))
