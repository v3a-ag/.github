# .github da v3a-ag

Repositório público da organização, só com conteúdo genérico: a esteira de publicação dos apps, o esquema da ficha do projeto e os modelos de bloco. Não tem endereço de servidor, segredo, nome de rede nem dado de cliente.

## Conteúdo

| Caminho | O que é |
| --- | --- |
| [`.github/workflows/esteira-reutilizavel.yml`](.github/workflows/esteira-reutilizavel.yml) | esteira (`workflow_call`): valida a ficha, roda os testes, gera a imagem no GHCR e registra o deployment `producao` |
| [`.github/workflows/voltar-versao-reutilizavel.yml`](.github/workflows/voltar-versao-reutilizavel.yml) | voltar versão (`workflow_call`): deployment novo do tipo `rollback` com o digest de uma versão já publicada, sem rebuild |
| [`acoes/`](acoes/) | ações compostas usadas pela esteira (verificar; preparar a imagem) |
| [`scripts/`](scripts/) | validador da ficha, verificação do bloco, testes do projeto, contexto de build |
| [`esquema/v3a-projeto.schema.json`](esquema/v3a-projeto.schema.json) | esquema da ficha `v3a-projeto.yml` |
| [`blocos/pagina-web-simples/`](blocos/pagina-web-simples/) | bloco Página web simples: Dockerfile padrão e repositório de exemplo |
| [`docs/ficha.md`](docs/ficha.md) | a ficha, campo a campo |
| [`docs/contrato-deployment.md`](docs/contrato-deployment.md) | o contrato do deployment entre o Actions e o agente de deploy |
| [`testes/`](testes/) | testes do validador e dos scripts |

## Como um repositório usa

Dois chamadores em `.github/workflows/` (exemplos em [`blocos/pagina-web-simples/exemplo/.github/workflows/`](blocos/pagina-web-simples/exemplo/.github/workflows/)), sempre fixados pelo commit desta esteira:

```yaml
jobs:
  esteira:
    uses: v3a-ag/.github/.github/workflows/esteira-reutilizavel.yml@<commit>
    with:
      publicar: ${{ github.event_name == 'push' }}
```

No PR, só ficha e testes (um job, leitura do conteúdo). No push na `main`, ficha, testes, imagem e deployment (um job, com escrita só em pacotes e deployments). Falhou a ficha ou um teste: nenhuma imagem e nenhum deployment.

## Regras desta esteira

- Ações de terceiros fixadas pelo commit, com a versão em comentário.
- Permissões mínimas declaradas em cada job.
- Um job por execução, alvo de até 3 minutos, cache do build no cache do Actions.
- A esteira não fala com servidor nenhum: ela só deixa o pedido (o deployment); quem publica é o agente de deploy, que busca os pedidos.

## Testes

```bash
python3 -m unittest discover -s testes -v
bash testes/rodar_fichas_yaml.sh   # precisa do yq
```

## Licença

Proprietária. Ver [LICENSE](LICENSE).
