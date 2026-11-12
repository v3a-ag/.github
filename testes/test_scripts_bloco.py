"""Testes dos scripts do bloco Página web simples.

    python3 -m unittest discover -s testes -v
"""

import os
import subprocess
import tempfile
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RODAR_TESTES = os.path.join(RAIZ, "scripts", "rodar_testes.sh")
VERIFICAR_BLOCO = os.path.join(RAIZ, "scripts", "verificar_bloco.sh")
PREPARAR = os.path.join(RAIZ, "scripts", "preparar_contexto.sh")
DOCKERFILE = os.path.join(RAIZ, "blocos", "pagina-web-simples", "Dockerfile")


def escrever(base, rel, conteudo="x"):
    p = os.path.join(base, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(conteudo)
    return p


def rodar(*cmd, cwd=None):
    r = subprocess.run(["bash", *cmd], capture_output=True, text=True, cwd=cwd)
    return r.returncode, r.stdout + r.stderr


class RodarTestes(unittest.TestCase):
    """TA-02: teste do projeto que falha para a esteira antes da imagem."""

    def test_sem_pasta_de_testes_passa_e_avisa(self):
        with tempfile.TemporaryDirectory() as d:
            codigo, saida = rodar(RODAR_TESTES, d)
            self.assertEqual(codigo, 0, saida)
            self.assertIn("nenhum teste do projeto", saida)

    def test_testes_que_passam(self):
        with tempfile.TemporaryDirectory() as d:
            escrever(d, "testes/a.sh", "exit 0\n")
            escrever(d, "testes/b.sh", "echo rodou-b\n")
            codigo, saida = rodar(RODAR_TESTES, d)
            self.assertEqual(codigo, 0, saida)
            self.assertIn("rodou-b", saida)
            self.assertIn("2 teste(s) passaram", saida)

    def test_teste_que_falha_para_a_esteira(self):
        with tempfile.TemporaryDirectory() as d:
            escrever(d, "testes/a.sh", "exit 0\n")
            escrever(d, "testes/b-falha.sh", "echo quebrou; exit 3\n")
            escrever(d, "testes/c.sh", "touch rodou-c\n")
            codigo, saida = rodar(RODAR_TESTES, d)
            self.assertEqual(codigo, 1, saida)
            self.assertIn("::error", saida)
            self.assertIn("b-falha.sh", saida)
            # para no primeiro que falha
            self.assertFalse(os.path.exists(os.path.join(d, "rodou-c")))

    def test_testes_rodam_na_raiz_do_repositorio(self):
        with tempfile.TemporaryDirectory() as d:
            escrever(d, "index.html", "<html></html>")
            escrever(d, "testes/a.sh", "test -f index.html\n")
            codigo, saida = rodar(RODAR_TESTES, d, cwd="/")
            self.assertEqual(codigo, 0, saida)


class VerificarBloco(unittest.TestCase):
    def test_pagina_com_index_passa(self):
        with tempfile.TemporaryDirectory() as d:
            escrever(d, "index.html", "<!doctype html><title>x</title>")
            codigo, saida = rodar(VERIFICAR_BLOCO, "pagina_web_simples", d)
            self.assertEqual(codigo, 0, saida)

    def test_pagina_sem_index_falha(self):
        with tempfile.TemporaryDirectory() as d:
            codigo, saida = rodar(VERIFICAR_BLOCO, "pagina_web_simples", d)
            self.assertEqual(codigo, 1, saida)
            self.assertIn("index.html", saida)

    def test_pagina_com_index_vazio_falha(self):
        with tempfile.TemporaryDirectory() as d:
            escrever(d, "index.html", "")
            codigo, saida = rodar(VERIFICAR_BLOCO, "pagina_web_simples", d)
            self.assertEqual(codigo, 1, saida)

    def test_pagina_sem_marcacao_html_falha(self):
        with tempfile.TemporaryDirectory() as d:
            escrever(d, "index.html", "só texto")
            codigo, saida = rodar(VERIFICAR_BLOCO, "pagina_web_simples", d)
            self.assertEqual(codigo, 1, saida)
            self.assertIn("HTML", saida)

    def test_pagina_com_cgi_bin_falha(self):
        with tempfile.TemporaryDirectory() as d:
            escrever(d, "index.html", "<html></html>")
            escrever(d, "cgi-bin/x", "#!/bin/sh\n")
            codigo, saida = rodar(VERIFICAR_BLOCO, "pagina_web_simples", d)
            self.assertEqual(codigo, 1, saida)
            self.assertIn("cgi-bin", saida)

    def test_bloco_desconhecido_falha(self):
        with tempfile.TemporaryDirectory() as d:
            codigo, saida = rodar(VERIFICAR_BLOCO, "outro", d)
            self.assertEqual(codigo, 1, saida)


class PrepararContexto(unittest.TestCase):
    def montar_repo(self, d):
        escrever(d, "index.html", "<html></html>")
        escrever(d, "css/estilo.css", "body{}")
        escrever(d, "v3a-projeto.yml", "versao: 1\n")
        for fora in ("README.md", "LICENSE", "testes/a.sh", ".github/workflows/esteira.yml",
                     ".git/config", "docs/decisao.md", "Dockerfile", ".gitignore"):
            escrever(d, fora)

    def test_contexto_tem_site_ficha_e_dockerfile_padrao(self):
        with tempfile.TemporaryDirectory() as repo, tempfile.TemporaryDirectory() as tmp:
            self.montar_repo(repo)
            ctx = os.path.join(tmp, "ctx")
            codigo, saida = rodar(PREPARAR, "pagina_web_simples", repo, ctx)
            self.assertEqual(codigo, 0, saida)
            self.assertTrue(os.path.isfile(os.path.join(ctx, "site", "index.html")))
            self.assertTrue(os.path.isfile(os.path.join(ctx, "site", "css", "estilo.css")))
            self.assertTrue(os.path.isfile(os.path.join(ctx, "v3a-projeto.yml")))
            with open(os.path.join(ctx, "Dockerfile")) as a, open(DOCKERFILE) as b:
                self.assertEqual(a.read(), b.read())

    def test_contexto_nao_leva_arquivos_fora_do_site(self):
        with tempfile.TemporaryDirectory() as repo, tempfile.TemporaryDirectory() as tmp:
            self.montar_repo(repo)
            ctx = os.path.join(tmp, "ctx")
            codigo, saida = rodar(PREPARAR, "pagina_web_simples", repo, ctx)
            self.assertEqual(codigo, 0, saida)
            site = os.path.join(ctx, "site")
            for fora in ("README.md", "LICENSE", "testes", ".github", ".git", "docs",
                         "Dockerfile", ".gitignore", "v3a-projeto.yml"):
                self.assertFalse(os.path.exists(os.path.join(site, fora)), fora)

    def test_dockerfile_do_repositorio_e_ignorado(self):
        with tempfile.TemporaryDirectory() as repo, tempfile.TemporaryDirectory() as tmp:
            self.montar_repo(repo)
            escrever(repo, "Dockerfile", "FROM ubuntu\nUSER root\n")
            ctx = os.path.join(tmp, "ctx")
            rodar(PREPARAR, "pagina_web_simples", repo, ctx)
            with open(os.path.join(ctx, "Dockerfile")) as a:
                self.assertNotIn("ubuntu", a.read())


class DockerfilePadrao(unittest.TestCase):
    def test_imagem_base_fixada_por_digest(self):
        with open(DOCKERFILE) as f:
            linhas = [l for l in f if l.startswith("FROM ")]
        self.assertEqual(len(linhas), 1)
        self.assertRegex(linhas[0], r"@sha256:[0-9a-f]{64}")

    def test_roda_sem_root(self):
        with open(DOCKERFILE) as f:
            conteudo = f.read()
        self.assertRegex(conteudo, r"\nUSER 65534:65534\n")

    def test_ficha_vai_para_dentro_da_imagem(self):
        with open(DOCKERFILE) as f:
            self.assertIn("COPY v3a-projeto.yml /v3a/v3a-projeto.yml", f.read())


if __name__ == "__main__":
    unittest.main()
