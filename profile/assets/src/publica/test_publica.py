import re
import tempfile
import unittest
from pathlib import Path

from publica import pecas

NOMES = ["hero", "hero-celular", "secao-01", "secao-02", "secao-03", "secao-04", "metodo", "fechamento"]


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

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def _svg(self, nome, tema="claro"):
        return (self.pasta / f"{nome}-{tema}.svg").read_text()

    def test_gera_todas_as_pecas(self):
        esperado = {f"{n}-{t}.svg" for n in NOMES for t in ("claro", "escuro")}
        self.assertEqual({p.name for p in self.svgs}, esperado)

    def test_publica_sem_numeros_de_escala(self):
        # numeração de seção/passo ("01.") é estilo do manual; contagem não
        for t in _textos(pecas.COPY):
            limpo = re.sub(r"^0\d\.?$", "", t.replace("V3A", ""))
            self.assertIsNone(re.search(r"\d", limpo), t)

    def test_claro_sem_moldura_escuro_em_bloco(self):
        for nome in ("hero", "hero-celular", "fechamento"):
            self.assertNotIn("<rect", self._svg(nome, "claro"), nome)
            self.assertIn('fill="#636466"', self._svg(nome, "escuro"), nome)

    def test_logo_e_grafismo_na_mesma_cor(self):
        for tema, cor in (("claro", "#FFCB05"), ("escuro", "#FFFFFF")):
            s = self._svg("hero", tema)
            self.assertIn(f'<g class="logo" fill="{cor}">', s)
            self.assertIn(f'<g class="graf" fill="{cor}">', s)

    def test_so_hero_tem_entrada_e_so_metodo_tem_loop(self):
        for nome in NOMES:
            s = self._svg(nome)
            tem_entrada = "@keyframes sobe" in s
            self.assertEqual(tem_entrada, nome.startswith("hero"), nome)
            self.assertEqual(s.count("infinite"), 1 if nome == "metodo" else 0, nome)

    def test_animado_nao_tem_transform_proprio(self):
        for p in self.svgs:
            s = p.read_text()
            self.assertNotRegex(s, r'<g class="[^"]*" transform=', p.name)
            self.assertNotRegex(s, r'<g transform="[^"]*" class=', p.name)

    def test_sem_text_nem_externo(self):
        for p in self.svgs:
            s = p.read_text()
            self.assertNotIn("<text", s, p.name)
            self.assertNotRegex(s, r'href="https?:', p.name)


if __name__ == "__main__":
    unittest.main()
