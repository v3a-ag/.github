import re
import tempfile
import unittest
from pathlib import Path

from publica import pecas

NOMES = list(pecas.PECAS)
COM_LOOP = {"hero", "hero-celular", "esteira", "esteira-celular", "anatomia", "anatomia-celular", "arquitetura", "arquitetura-celular"}


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
        for nome in ("hero", "esteira", "anatomia", "arquitetura", "principios", "stack", "rodape"):
            self.assertIn(f"{nome}-celular", pecas.PECAS)

    def test_publica_sem_numeros_de_escala(self):
        for t in _textos(pecas.COPY):
            limpo = re.sub(r"^0\d\.?$|n8n", "", t.replace("V3A", ""), flags=re.I)  # numeração e nome de ferramenta
            self.assertIsNone(re.search(r"\d", limpo), t)

    def test_secao_tem_titulo_dentro_do_bloco(self):
        for chave, (num, titulo, _) in pecas.COPY["secoes"].items():
            for nome in (chave, f"{chave}-celular"):
                self.assertIn(f"<title>{num} {titulo.capitalize()}.", self._svg(nome), nome)

    def test_claro_branco_sem_contorno_escuro_cinza(self):
        for nome in NOMES:
            claro, escuro = self._svg(nome, "claro"), self._svg(nome, "escuro")
            # cor do fundo checada em gerador.test_gerador.TestLegivelEmQualquerFundo; aqui: sem contorno
            self.assertNotRegex(claro, r'</style>(<g[^>]*>)?<rect [^>]*stroke', nome)
            self.assertIn('fill="#636466"', escuro, nome)

    def test_logo_e_grafismo_na_mesma_cor(self):
        for tema, cor in (("claro", "#FFCB05"), ("escuro", "#FFFFFF")):
            s = self._svg("hero", tema)
            self.assertIn(f'<g class="logo" fill="{cor}">', s)
            self.assertIn(f'<g fill="{cor}"><polygon class="gp0"', s)  # grafismo sobe peça por peça

    def test_entrada_so_no_hero_e_loops_nos_diagramas(self):
        for nome in NOMES:
            s = self._svg(nome)
            self.assertEqual("@keyframes entra" in s, nome.startswith("hero"), nome)
            self.assertEqual("infinite" in s, nome in COM_LOOP, nome)

    def test_em_repouso_so_a_primeira_variacao_aparece(self):
        s = self._svg("anatomia")
        self.assertRegex(s, r"\.ex1\{animation-delay:[\d.]+s;opacity:0\}")
        self.assertRegex(s, r"\.ex2\{animation-delay:[\d.]+s;opacity:0\}")
        self.assertNotRegex(s, r"\.ex0\{[^}]*opacity:0")
        h = self._svg("hero")
        self.assertIn(".pal{opacity:0}.pal0{opacity:1}", h)

    def test_hero_gira_as_palavras_e_o_e_desliza(self):
        h = self._svg("hero")
        self.assertEqual(h.count('<g class="pal pal'), len(pecas.PALAVRAS))
        self.assertEqual(h.count('<g class="e">'), 1)
        self.assertEqual(pecas.PALAVRAS[0], "TEMPO INTELIGENTE")
        from gerador import texto as tx
        for p in pecas.PALAVRAS:  # cabe na coluna do texto (desktop 390, celular 360)
            self.assertLess(tx.largura(p + " É", 25.5, 400, 0.005), 390, p)
            self.assertLess(tx.largura(p + " É", 24, 400, 0.005), 360, p)

    def test_motion_sem_linear_e_com_curvas_suaves(self):
        from gerador import motion
        for nome in NOMES:
            s = self._svg(nome)
            for regra in re.findall(r"animation:[^;}]*", s):
                if "linear" in regra:
                    self.assertIn("flui", regra, nome)
            if "@keyframes" in s and nome not in ("anatomia", "anatomia-celular"):
                self.assertTrue(motion.EASE_OUT in s or motion.EASE_IN_OUT in s, nome)

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
