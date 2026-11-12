"""Testes do validador da ficha v3a-projeto.yml.

Rodam o script como o workflow roda (processo separado, ficha em JSON,
convertida do YAML pelo yq no runner). Sem dependências fora da stdlib.

    python3 -m unittest discover -s testes -v
"""

import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(RAIZ, "scripts", "validar_ficha.py")
REPO = "N1-exemplo-pagina"

FICHA_VALIDA = {
    "versao": 1,
    "chave": "N1-exemplo-pagina",
    "bloco": "pagina_web_simples",
    "healthcheck": "/",
    "exposicao": "interface_humana",
    "dependencias_privadas": [],
    "servicos_compartilhados": [],
    "conversa_com_n8n": False,
    "apis_externas": [],
    "dados": {"classificacao": "interno", "persistencia": "nenhuma"},
    "recursos": {"memoria": "64m", "cpu": 0.25},
}


def validar(ficha, repositorio=REPO, cru=None):
    """Grava a ficha num arquivo temporário e roda o validador."""
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        f.write(cru if cru is not None else json.dumps(ficha))
        caminho = f.name
    try:
        r = subprocess.run(
            [sys.executable, SCRIPT, "--repositorio", repositorio, caminho],
            capture_output=True,
            text=True,
        )
    finally:
        os.unlink(caminho)
    return r.returncode, r.stdout + r.stderr


def com(**campos):
    f = copy.deepcopy(FICHA_VALIDA)
    f.update(campos)
    return f


class FichaValida(unittest.TestCase):
    def test_ficha_valida_passa(self):
        codigo, saida = validar(FICHA_VALIDA)
        self.assertEqual(codigo, 0, saida)
        self.assertIn("ficha válida", saida)

    def test_ficha_minima_passa(self):
        minima = {"versao": 1, "chave": REPO, "bloco": "pagina_web_simples"}
        codigo, saida = validar(minima)
        self.assertEqual(codigo, 0, saida)


class CamposDeInfraestrutura(unittest.TestCase):
    """TA-38: a ficha não aceita rede, sub-rede, alias, porta, mount nem label."""

    PROIBIDOS = [
        "porta", "portas", "port", "ports", "expose",
        "rede", "redes", "network", "networks", "network_mode",
        "sub-rede", "sub_rede", "subrede", "subnet",
        "alias", "aliases",
        "mount", "mounts", "volume", "volumes", "bind",
        "label", "labels", "rotulo", "rotulos",
        "privileged", "privilegiado", "cap_add", "devices",
        "container_name", "hostname", "ipv4_address", "extra_hosts",
    ]

    def test_cada_campo_proibido_no_topo_e_recusado(self):
        for campo in self.PROIBIDOS:
            with self.subTest(campo=campo):
                codigo, saida = validar(com(**{campo: "x"}))
                self.assertEqual(codigo, 1, saida)
                self.assertIn("campo de infraestrutura", saida)
                self.assertIn(campo, saida)

    def test_porta_numerica_e_recusada(self):
        codigo, saida = validar(com(porta=8080))
        self.assertEqual(codigo, 1, saida)
        self.assertIn("porta", saida)

    def test_campo_proibido_aninhado_e_recusado(self):
        f = com()
        f["recursos"]["porta"] = 80
        f["dados"]["Labels"] = {"qualquer.coisa": "sim"}
        codigo, saida = validar(f)
        self.assertEqual(codigo, 1, saida)
        self.assertIn("recursos.porta", saida)
        self.assertIn("dados.Labels", saida)

    def test_campo_proibido_dentro_de_lista_e_recusado(self):
        f = com(apis_externas=[{"alias": "x"}])
        codigo, saida = validar(f)
        self.assertEqual(codigo, 1, saida)
        self.assertIn("apis_externas[0].alias", saida)

    def test_valor_com_docker_sock_e_recusado(self):
        codigo, saida = validar(com(healthcheck="/var/run/docker.sock"))
        self.assertEqual(codigo, 1, saida)
        self.assertIn("docker.sock", saida)


class Esquema(unittest.TestCase):
    def test_campo_desconhecido_e_recusado(self):
        codigo, saida = validar(com(cor_favorita="azul"))
        self.assertEqual(codigo, 1, saida)
        self.assertIn("campo desconhecido", saida)
        self.assertIn("cor_favorita", saida)

    def test_chave_obrigatoria(self):
        f = com()
        del f["chave"]
        codigo, saida = validar(f)
        self.assertEqual(codigo, 1, saida)
        self.assertIn("chave", saida)
        self.assertIn("obrigatório", saida)

    def test_chave_com_formato_invalido(self):
        codigo, saida = validar(com(chave="teste_esteira"), repositorio="teste_esteira")
        self.assertEqual(codigo, 1, saida)
        self.assertIn("chave", saida)

    def test_chave_diferente_do_repositorio(self):
        codigo, saida = validar(com(chave="N1-outro-app"))
        self.assertEqual(codigo, 1, saida)
        self.assertIn("nome do repositório", saida)

    def test_bloco_desconhecido(self):
        codigo, saida = validar(com(bloco="kubernetes"))
        self.assertEqual(codigo, 1, saida)
        self.assertIn("bloco", saida)

    def test_versao_da_ficha_desconhecida(self):
        codigo, saida = validar(com(versao=2))
        self.assertEqual(codigo, 1, saida)
        self.assertIn("versao", saida)

    def test_healthcheck_precisa_comecar_com_barra(self):
        codigo, saida = validar(com(healthcheck="saude"))
        self.assertEqual(codigo, 1, saida)
        self.assertIn("healthcheck", saida)

    def test_servico_compartilhado_fora_da_lista(self):
        codigo, saida = validar(com(servicos_compartilhados=["redis"]))
        self.assertEqual(codigo, 1, saida)
        self.assertIn("servicos_compartilhados[0]", saida)

    def test_memoria_fora_do_limite(self):
        f = com()
        f["recursos"]["memoria"] = "4096m"
        codigo, saida = validar(f)
        self.assertEqual(codigo, 1, saida)
        self.assertIn("recursos.memoria", saida)

    def test_cpu_fora_do_limite(self):
        f = com()
        f["recursos"]["cpu"] = 8
        codigo, saida = validar(f)
        self.assertEqual(codigo, 1, saida)
        self.assertIn("recursos.cpu", saida)

    def test_tipo_errado(self):
        codigo, saida = validar(com(conversa_com_n8n="sim"))
        self.assertEqual(codigo, 1, saida)
        self.assertIn("conversa_com_n8n", saida)


class Politica(unittest.TestCase):
    def test_exposicao_maquina_bloqueada_ate_p18(self):
        codigo, saida = validar(com(exposicao="maquina"))
        self.assertEqual(codigo, 1, saida)
        self.assertIn("P-18", saida)


class Entrada(unittest.TestCase):
    def test_ficha_que_nao_e_objeto(self):
        codigo, saida = validar(None, cru="[1, 2]")
        self.assertEqual(codigo, 1, saida)
        self.assertIn("mapa", saida)

    def test_ficha_vazia(self):
        # yq converte arquivo vazio em null
        codigo, saida = validar(None, cru="null")
        self.assertEqual(codigo, 1, saida)

    def test_json_invalido(self):
        codigo, saida = validar(None, cru="{nao e json")
        self.assertEqual(codigo, 1, saida)
        self.assertIn("ilegível", saida)

    def test_arquivo_ausente(self):
        r = subprocess.run(
            [sys.executable, SCRIPT, "--repositorio", REPO, "/nao/existe.json"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("não encontrada", r.stdout + r.stderr)


class Saida(unittest.TestCase):
    def test_erros_saem_como_anotacao_do_actions(self):
        codigo, saida = validar(com(porta=80))
        self.assertEqual(codigo, 1)
        self.assertIn("::error", saida)
        self.assertIn("ficha recusada", saida)


if __name__ == "__main__":
    unittest.main()
