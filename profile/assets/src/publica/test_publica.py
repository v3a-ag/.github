import re
import tempfile
import unittest
from pathlib import Path

from publica import pecas

NOMES = list(pecas.PECAS) + list(pecas.COPY["secoes"])
COM_LOOP = {"esteira", "esteira-celular", "anatomia", "anatomia-celular", "arquitetura", "arquitetura-celular"}


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

    def test_todo_diagrama_tem_versao_celular(self):
        for nome in ("hero", "esteira", "anatomia", "arquitetura", "principios", "stack", "fechamento"):
            self.assertIn(f"{nome}-celular", pecas.PECAS)

    def test_publica_sem_numeros_de_escala(self):
        for t in _textos(pecas.COPY):
            limpo = re.sub(r"^0\d\.?$|n8n", "", t.replace("V3A", ""), flags=re.I)  # numeração e nome de ferramenta
            self.assertIsNone(re.search(r"\d", limpo), t)

    def test_claro_sem_moldura_escuro_em_bloco(self):
        for nome in ("hero", "hero-celular", "fechamento", "fechamento-celular"):
            self.assertNotIn('fill="#636466"', self._svg(nome, "claro"), nome)
            self.assertIn('fill="#636466"', self._svg(nome, "escuro"), nome)

    def test_logo_e_grafismo_na_mesma_cor(self):
        for tema, cor in (("claro", "#FFCB05"), ("escuro", "#FFFFFF")):
            s = self._svg("hero", tema)
            self.assertIn(f'<g class="logo" fill="{cor}">', s)
            self.assertIn(f'<g class="graf" fill="{cor}">', s)

    def test_entrada_so_no_hero_e_loops_nos_diagramas(self):
        for nome in NOMES:
            s = self._svg(nome)
            self.assertEqual("@keyframes sobe" in s, nome.startswith("hero"), nome)
            self.assertEqual("infinite" in s, nome in COM_LOOP, nome)

    def test_ciclo_mostra_primeiro_exemplo_sem_animacao(self):
        s = self._svg("anatomia")
        self.assertIn(".ex1{animation-delay:4s;opacity:0}", s)
        self.assertIn(".ex2{animation-delay:8s;opacity:0}", s)

    def test_nada_cortado_na_borda(self):
        for nome in ("anatomia",):
            s = self._svg(nome)
            for x, w in re.findall(r'<rect x="([\d.]+)" y="[\d.]+" width="([\d.]+)" height="168"', s):
                self.assertLessEqual(float(x) + float(w) + 1.5, 830, nome)

    def test_animado_nao_tem_transform_proprio(self):
        for p in self.svgs:
            s = p.read_text()
            self.assertNotRegex(s, r'<g class="[^"]*" transform=', p.name)
            self.assertNotRegex(s, r'<g transform="[^"]*" class=', p.name)
            self.assertNotRegex(s, r'<(rect|circle|path) class="[^"]*"[^>]* transform=', p.name)

    def test_sem_text_nem_externo(self):
        for p in self.svgs:
            s = p.read_text()
            self.assertNotIn("<text", s, p.name)
            self.assertNotRegex(s, r'href="https?:', p.name)


if __name__ == "__main__":
    unittest.main()
