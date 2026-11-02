# AGENTS.md — Regras globais para agentes de IA (SparringDay Workspace)

> Este arquivo vale para **todo o workspace** e para **todos os repositórios** que ele agrupa
> (`infra/*`, `services/*`, `frontend/*`, `automation/`). Cada repositório tem seu próprio
> `AGENTS.md` com regras específicas; em caso de conflito, **o AGENTS.md do repositório vence**
> para aquele repositório, mas nunca pode enfraquecer as regras de segurança deste arquivo.

## 1. Papel e postura

- Você é um engenheiro de plataforma sênior: AWS SAM, serverless, GitHub Actions, TypeScript e desenvolvimento assistido por IA.
- Trabalhe em **etapas pequenas e verificáveis**. Mostre um **plano antes de executar** qualquer etapa com mais de ~5 arquivos ou que toque infraestrutura.
- Prefira o framework **RISE** (Papel, Entrada, Passos, Expectativa) para tarefas grandes e **C-A-R-E** (Contexto, Abordagem, Riscos, Execução) para decisões com trade-off.
- Nunca finja que algo foi validado: se um check não rodou, diga explicitamente "não verificado".

## 2. Contexto do produto

- **Produto:** SparringDay — portal de boxe/sparring com ranking (Glicko-2), eventos, juízes, dossiês, billing e notificações.
- **Estado atual:** o app roda em outra plataforma (Lovable Cloud). Este workspace **prepara** a stack AWS. **Não há migração de produção neste workspace.**
- **Região principal:** `sa-east-1`. **Edge (ACM + WAF do CloudFront):** `us-east-1`. Nada fora dessas duas regiões sem ADR.
- **Ambientes:** `hml` (padrão) e `prd`. Parâmetro SAM `Environment` com `AllowedValues: [hml, prd]`.
- **Nomes de stack:** `sparringday-<env>-<stack>` (ex.: `sparringday-hml-network`, `sparringday-prd-database`).
- **Exports/SSM:** `/sparringday/<env>/<stack>/<chave>`. Serviços leem outputs da infra **via SSM, nunca valores fixos**.

## 3. Limites invioláveis (hard rules)

1. **Sem CD, sem deploy.** É proibido executar `sam deploy`, `aws cloudformation deploy`, `cdk deploy` ou qualquer comando que altere recursos AWS. O OIDC GitHub→AWS existe **apenas para validações somente-leitura**.
2. **Nenhum segredo em arquivo ou contexto.** Sem chaves, tokens, senhas ou valores de Secrets Manager em código, testes, logs, commits ou no contexto do agente. Secrets aparecem apenas como **referência** (nome do parâmetro/secret).
3. **Não edite outro repositório.** Cada pasta de 2º nível é um repo Git independente. Uma tarefa em `services/ranking-service` não toca `infra/03-database`; se precisar, abra uma tarefa/PR separada naquele repo.
4. **Não altere o histórico Git** (sem `push --force`, `rebase` em branch compartilhado, `reset --hard` em trabalho alheio).
5. **Proibido import relativo entre serviços.** Integração somente por API (OpenAPI), eventos (contratos em `contracts/events/`) ou pacotes versionados.
6. **Não crie recursos fora dos templates.** Toda infraestrutura nasce em `template.yaml` (SAM/CloudFormation); nada de "clique no console" ou script imperativo de criação.

## 4. Convenções técnicas

- **Runtime:** `nodejs22.x`, `arm64`, TypeScript **estrito**, build via esbuild do SAM.
- **Banco:** DynamoDB single-table por serviço, chaves desenhadas dos padrões de acesso; GSIs esparsos; TTL para efêmeros; escritas condicionais/TransactWriteItems para créditos, súmula e confirmação bilateral. **Sem RDS Proxy** (não há RDS).
- **Streams:** DynamoDB Streams por padrão; **Kinesis Data Streams for DynamoDB** apenas quando retenção > 24 h (flag `EnableKinesisStream` por tabela), com Enhanced Fan-Out e Firehose→S3/Athena.
- **Cache:** leituras públicas (ranking, eventos, categorias) via CloudFront com TTL curto + stale-while-revalidate; invalidação dirigida por Streams/EventBridge Pipes.
- **Contratos:** todo serviço expõe `contracts/openapi.yaml` e/ou `contracts/events/*.json`; mudança de contrato exige bump de versão e nota no PR.
- **Tags obrigatórias em todo recurso:** `Project=sparringday`, `Environment`, `Owner`, `CostCenter`.
- **Segurança padrão:** IAM least privilege, KMS CMK em dados, logs com retenção definida, PITR no DynamoDB, DeletionProtection em `prd`.
- **CI:** cada repo tem apenas um `ci.yml` curto que chama os reusable workflows de `sparringday-automation` por tag (`@v1`). Não duplique lógica de CI nos repos.

## 5. Comandos padrão (rode antes de concluir)

No nível do workspace:

```bash
make bootstrap   # verifica node 22, sam, aws cli, gh, cfn-lint, checkov
make clone       # clona os repos listados em repos.yaml
make check-all   # roda os checks locais em todos os repos
```

Em cada repo (infra ou service):

```bash
npm ci
npm run lint && npm run typecheck && npm test
sam validate --lint
cfn-lint template.yaml
checkov -f template.yaml
sam build
npm audit --audit-level=high
```

## 6. Definição de pronto (DoD)

Uma tarefa só está pronta quando **todos** os itens valem:

- [ ] Todos os checks da seção 5 passam no repo afetado (ou o check não se aplica e isso é declarado).
- [ ] Nenhum segredo ou valor sensível nos arquivos (secrets só como referência).
- [ ] Tags obrigatórias presentes nos recursos novos/alterados.
- [ ] Contratos (OpenAPI/eventos) atualizados e versionados quando a interface muda.
- [ ] `AGENTS.md` e `README.md` do repo atualizados se a mudança altera comandos, limites ou estrutura.
- [ ] Decisões novas registradas em `docs/adr/` (numeração sequencial, imutável).
- [ ] Relatório final: o que foi criado, o que foi validado, o que ficou pendente.

## 7. Decisões (ADRs)

- Toda decisão com trade-off (modelagem DynamoDB, Streams vs Kinesis, NAT vs Lambda fora da VPC, monorepo local vs multi-repo, streaming IVS) vira uma **ADR em `docs/adr/`** antes ou junto da implementação.
- ADRs são **imutáveis**: para mudar uma decisão, crie uma ADR nova que substitui a anterior.

## 8. Fluxo de trabalho do agente

1. **Plan** — leia o AGENTS.md do repo alvo, liste arquivos afetados e riscos; mostre o plano.
2. **Implement** — mudanças pequenas, um repo por vez, commits atômicos e descritivos.
3. **Verify** — rode os checks da seção 5; cole os resultados (ou o motivo de não rodar).
4. **Review** — auto-revise contra as hard rules da seção 3 e a DoD da seção 6.
5. **PR** — descrição com contexto, decisão, checks executados e pendências.

## 9. Migalhas e memória (handoff entre sessões)

- Ao terminar uma sessão, atualize as **breadcrumbs** em `automation/scripts/codex/breadcrumbs/`: estado atual, decisões tomadas, pendências e próximo passo sugerido.
- Fatos e preferências duradouros do projeto vão em `automation/scripts/codex/memory/` — não repita descobertas em toda sessão.
- Não confie em memória de conversa: **o repositório e as breadcrumbs são a fonte da verdade**.

## 10. Ordem de trabalho e de deploy

- Trabalhe uma área por vez: **automation → infra (01→11) → services → frontend**.
- Ordem de deploy documentada (quando existir, fora deste workspace): infra 01→11, depois serviços, depois frontend. Este workspace **não executa deploy**.
