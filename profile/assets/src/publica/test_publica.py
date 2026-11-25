import re
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from publica import gif_fluxo, pecas

NOMES = ["banner", "card-horas", "card-planilha", "card-painel", "card-relatorio",
         "card-ia", "card-durar", "trabalho", "fechamento"]


def _textos(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _textos(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from _textos(v)


class TestPublica(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.pasta = Path(cls.tmp.name)
        cls.svgs = pecas.gerar_todas(cls.pasta)
        cls.gifs = gif_fluxo.gerar(cls.pasta)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_gera_todas_as_pecas(self):
        esperado = {f"{n}-{t}.svg" for n in NOMES for t in ("claro", "escuro")}
        self.assertEqual({p.name for p in self.svgs}, esperado)
        for p in self.svgs:
            self.assertTrue(p.exists())

    def test_publica_sem_digitos(self):
        for t in _textos(pecas.COPY):
            self.assertIsNone(re.search(r"\d", t.replace("V3A", "")), t)
        for t in gif_fluxo.PASSOS:
            self.assertIsNone(re.search(r"\d", t.replace("V3A", "")), t)

    def test_gif_limites(self):
        self.assertEqual({p.name for p in self.gifs}, {"fluxo-claro.gif", "fluxo-escuro.gif"})
        for p in self.gifs:
            self.assertLessEqual(p.stat().st_size, 1_500_000)
            with Image.open(p) as im:
                self.assertLessEqual(im.width, 900)
                self.assertGreater(im.n_frames, 1)
                self.assertEqual(im.info.get("loop"), 0)

    def test_banner_tem_animacao(self):
        s = (self.pasta / "banner-claro.svg").read_text()
        self.assertIn("@keyframes", s)

    def test_animado_nao_tem_transform_proprio(self):
        # CSS transform da animação sobrescreve o atributo transform do SVG
        for p in self.svgs:
            s = p.read_text()
            self.assertNotRegex(s, r'<g class="[^"]*" transform=', p.name)
            self.assertNotRegex(s, r'<g transform="[^"]*" class=', p.name)

    def test_cards_sem_entrada(self):
        for n in NOMES:
            if n == "banner":
                continue
            s = (self.pasta / f"{n}-claro.svg").read_text()
            self.assertNotIn("entra", s, n)
            self.assertLessEqual(s.count("infinite"), 1, n)

    def test_sem_text_nem_externo(self):
        for p in self.svgs:
            s = p.read_text()
            self.assertNotIn("<text", s, p.name)
            self.assertNotRegex(s, r'href="https?:', p.name)


if __name__ == "__main__":
    unittest.main()
