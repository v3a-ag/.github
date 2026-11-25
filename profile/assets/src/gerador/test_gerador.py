import re
import tempfile
import unittest
from pathlib import Path

from gerador import marca, svg, texto


class TestTexto(unittest.TestCase):
    def test_acentos_viram_path(self):
        d, largura = texto.caminho("EXPERIÊNCIA ção", 40, peso=800)
        self.assertTrue(d.strip())
        self.assertGreater(largura, 0)
        # cada letra acentuada desenha algo: com e sem acento dão paths diferentes
        d2, _ = texto.caminho("EXPERIENCIA cao", 40, peso=800)
        self.assertNotEqual(d, d2)

    def test_peso_muda_largura(self):
        _, fino = texto.caminho("Automação", 40, peso=100)
        _, grosso = texto.caminho("Automação", 40, peso=900)
        self.assertGreater(grosso, fino)

    def test_tracking_negativo_encolhe(self):
        _, normal = texto.caminho("Automação", 40, peso=800)
        _, apertado = texto.caminho("Automação", 40, peso=800, tracking=-0.02)
        self.assertLess(apertado, normal)


class TestPeca(unittest.TestCase):
    def _peca(self, tema="claro"):
        d, _ = texto.caminho("Olá", 30, peso=800, x=10, y=40)
        corpo = f'<path d="{d}" fill="{marca.TEMAS[tema]["texto"]}"/>'
        return svg.peca(400, 100, corpo, tema, css="@keyframes a{from{opacity:0}to{opacity:1}}", titulo="Olá")

    def test_peca_sem_text_nem_externo(self):
        s = self._peca()
        self.assertNotIn("<text", s)
        self.assertNotRegex(s, r'href="https?:')
        self.assertNotRegex(s, r"url\(\s*['\"]?https?:")
        self.assertNotIn("@import", s)

    def test_peca_tem_reduced_motion(self):
        self.assertIn("prefers-reduced-motion: reduce", self._peca())

    def test_viewbox_e_largura(self):
        s = self._peca()
        self.assertIn('viewBox="0 0 400 100"', s)
        self.assertNotIn('width="100%"', s)
        self.assertIn("<title>Olá</title>", s)

    def test_salvar_gera_dois_temas(self):
        with tempfile.TemporaryDirectory() as t:
            arquivos = svg.salvar("teste", lambda tema: self._peca(tema), Path(t))
            nomes = sorted(p.name for p in arquivos)
            self.assertEqual(nomes, ["teste-claro.svg", "teste-escuro.svg"])
            claro = (Path(t) / "teste-claro.svg").read_text()
            escuro = (Path(t) / "teste-escuro.svg").read_text()
            self.assertNotEqual(claro, escuro)


class TestQuebra(unittest.TestCase):
    def test_quebrar_respeita_largura(self):
        frase = "O que tomava a tarde inteira agora roda sozinho, enquanto o time cuida do que importa."
        linhas = svg.quebrar(frase, 28, 400)
        self.assertGreater(len(linhas), 1)
        self.assertEqual(" ".join(linhas), frase)
        for l in linhas:
            self.assertLessEqual(texto.largura(l, 28), 400)

    def test_caber_reduz_tamanho(self):
        t = svg.caber("Relatório pronto, no padrão", 80, 300, peso=800)
        self.assertLess(t, 80)
        self.assertLessEqual(texto.largura("Relatório pronto, no padrão", t, 800), 300)


class TestMarca(unittest.TestCase):
    def test_temas_tem_chaves(self):
        for tema in ("claro", "escuro"):
            self.assertEqual(
                set(marca.TEMAS[tema]),
                {"fundo", "superficie", "texto", "texto_suave", "acento", "borda"},
            )

    def test_logo_institucional_tem_3_amarelo_e_sem_fundo(self):
        frag, (w, h) = marca.logo_paths("institucional", "escuro")
        self.assertIn(marca.CORES["amarelo"], frag)
        self.assertNotIn("<rect", frag)
        self.assertNotIn("var(--", frag)
        self.assertGreater(w, 0)
        self.assertGreater(h, 0)

    def test_logo_cor_segue_tema(self):
        claro, _ = marca.logo_paths("monograma", "claro")
        escuro, _ = marca.logo_paths("monograma", "escuro")
        self.assertIn(marca.TEMAS["claro"]["texto"], claro)
        self.assertIn(marca.TEMAS["escuro"]["texto"], escuro)


if __name__ == "__main__":
    unittest.main()
