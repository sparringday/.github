# SparringDay — workspace multi-repositório

Scaffold local para preparar a trilha AWS SAM do SparringDay em repositórios Git independentes. O conteúdo de infraestrutura, serviços e pipelines está intencionalmente em mockup/TODO para ser completado depois.

## Mapa

- `docs/adr/`: decisões e template de ADR.
- `infra/01-network` a `infra/11-observability`: uma stack por repositório.
- `services/`: oito serviços isolados.
- `frontend/web-portal` e `frontend/mobile`: aplicações web e mobile.
- `automation/`: workflows reutilizáveis, actions, CLI e kit de desenvolvimento por IA.
- `repos.yaml`: nomes, caminhos, tipos, owners e URLs GitHub planejadas.
- `workspace.code-workspace`: workspace multi-root para VS Code.

## Ordem pretendida de deploy futuro

`01-network` → `02-config` → `03-database` → `04-auth` → `05-storage` → `06-messaging` → `07-api` → `08-email` → `09-streaming` → `10-edge` → `11-observability` → serviços → frontend.

Esta ordem é apenas documentação para um futuro processo manual. Este scaffold não realiza deploy nem valida os recursos.

## Comandos preparados

- `make bootstrap`: verifica ferramentas locais (Node 22, SAM CLI, AWS CLI, GitHub CLI, cfn-lint e Checkov).
- `make clone`: clona os remotos declarados quando existirem; ignora repositórios já inicializados.
- `make sync`: busca atualizações dos remotos, sem fazer merge.
- `make check-all`: identifica workflows ainda em mockup e retorna pendências.

## Estado inicial

Os workflows reutilizáveis e os `ci.yml` são esqueletos com TODO e usam a referência prevista `@v1`. Eles só poderão rodar depois que os repositórios remotos forem criados, o modelo de pipeline existente for adaptado e a tag `v1` for publicada. Não há código funcional de serviços nem recursos AWS provisionáveis neste scaffold.

Os remotos estão declarados como `sparringday/<nome>`. As pastas locais já são repositórios Git separados com `origin` configurado; ainda não há criação/push dos repositórios remotos.
