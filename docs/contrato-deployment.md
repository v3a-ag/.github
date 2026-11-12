# Contrato do deployment (versão 1) [proposta]

O Actions não publica nada no servidor. Ele deixa um **pedido de publicação**: um deployment do GitHub no ambiente `producao`, com o payload abaixo. O agente de deploy lê o pedido, confere e publica. Este arquivo é o contrato entre os dois lados.

## Quem cria

| Workflow | Quando | Tipo |
| --- | --- | --- |
| `esteira-reutilizavel.yml` | push na `main`, depois de ficha válida, testes verdes e imagem publicada | `deploy` |
| `voltar-versao-reutilizavel.yml` | disparo manual com digest e motivo | `rollback` |

Nenhum outro caminho cria deployment. Ficha recusada ou teste que falha param o run antes da imagem e antes do deployment.

## Campos do deployment

| Campo da API | Valor |
| --- | --- |
| `environment` | `producao` |
| `ref` | o commit do pedido (40 caracteres hexadecimais) |
| `task` | `deploy` (nos dois tipos; o tipo está no payload) |
| `auto_merge` | `false` |
| `required_contexts` | `[]`: quem confere checks e aprovação é o agente |
| `production_environment` | `true` |
| `transient_environment` | `false` |
| `description` | `<tipo> <commit curto> <digest curto>` |

**Ordem.** O `id` do deployment é crescente e é a ordem dos pedidos. O agente segue o pedido mais recente de cada CHAVE, não a idade do commit. O job que cria deployments tem `concurrency` por repositório, sem cancelar, para dois merges seguidos não inverterem a ordem.

## Payload

```json
{
  "contrato": 1,
  "tipo": "deploy",
  "chave": "N1-exemplo-pagina",
  "commit": "0123456789abcdef0123456789abcdef01234567",
  "imagem": "ghcr.io/v3a-ag/n1-exemplo-pagina",
  "digest": "sha256:<64 hexadecimais>",
  "ficha_sha256": "<64 hexadecimais>",
  "autor": "login-no-github",
  "motivo": "push na main",
  "execucao": 123456789,
  "tentativa": 1,
  "origem": null
}
```

| Campo | Tipo | `deploy` | `rollback` |
| --- | --- | --- | --- |
| `contrato` | inteiro | `1` | `1` |
| `tipo` | `deploy` ou `rollback` | `deploy` | `rollback` |
| `chave` | CHAVE | da ficha (igual ao nome do repositório) | copiada do pedido de origem |
| `commit` | 40 hex | o commit do push | o commit da versão de volta |
| `imagem` | texto | `ghcr.io/<organização>/<chave em minúsculas>` | idem, conferida |
| `digest` | `sha256:` + 64 hex | o digest da imagem gerada agora | o digest pedido, que precisa existir no GHCR |
| `ficha_sha256` | 64 hex | sha256 do `v3a-projeto.yml` do commit | copiado do pedido de origem |
| `autor` | login do GitHub | quem disparou o run | quem disparou o "voltar versão" |
| `motivo` | texto, até 200 caracteres, uma linha | `push na main` | o motivo informado (obrigatório) |
| `execucao` | inteiro | id do run do Actions que fez o pedido | idem |
| `tentativa` | inteiro | tentativa do run (`1` no primeiro) | idem |
| `origem` | inteiro ou `null` | `null` | `id` do deployment que publicou esse digest antes |

**Sem segredos.** O payload não leva token, senha, cookie, e-mail, endereço de servidor nem nome de rede. O autor é o login, nunca o e-mail.

**A ficha dentro da imagem.** A imagem leva a ficha em `/v3a/v3a-projeto.yml`. O agente lê a ficha de lá e confere o `ficha_sha256`: o que está no ar e o que foi testado são a mesma coisa.

## O que o agente confere antes de publicar

1. `chave` igual ao nome do repositório e presente na lista autorizada.
2. `imagem` igual a `ghcr.io/<organização>/<chave em minúsculas>` e `digest` no formato certo; o digest baixado é o do pedido.
3. `commit` igual ao `sha` do deployment e na `main`.
4. Pelo `execucao`, o run (`GET /repos/{dono}/{repo}/actions/runs/{execucao}`) terminou com sucesso e os `referenced_workflows` trazem o workflow reutilizável na versão fixada. O deployment é criado no último passo do run; o agente espera o run terminar.
5. Aprovação: o commit e todos os commits desde a última versão publicada vieram de PR com Approve (regra da organização).
6. Pedido mais antigo que o último aplicado: status `inactive`. Pedido repetido (mesmo digest já no ar): nada muda.

## Status (escritos só pelo agente)

| Status da API | Nome na esteira | Quando |
| --- | --- | --- |
| nenhum ainda | pendente | o pedido existe e o agente ainda não leu |
| `in_progress` | em andamento | o agente pegou o pedido |
| `success` | sucesso | versão no ar e saudável |
| `failure` | falha | healthcheck falhou; a versão anterior voltou |
| `error` | erro | recusado antes do Docker; o motivo vai na `description` (ex.: `erro: sem aprovação`) |
| `inactive` | inativo | pedido substituído por um mais novo ou chegado atrasado |

## Consulta

O agente lista `GET /repos/{dono}/{repo}/deployments?environment=producao` só nos repositórios autorizados, com requisição condicional (`If-None-Match` com o ETag da consulta anterior), e lê os status de cada pedido novo.
