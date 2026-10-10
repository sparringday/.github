<div align="center">
  <img src="https://avatars.githubusercontent.com/u/322831670?s=180&v=4" width="120" alt="SparringDay" />

SparringDay

A vitrine digital do boxe amador e semiprofissional

Suba no ranking. Mostre sua história.





</div>

O SparringDay organiza o ecossistema de sparrings de boxe em uma experiência única: conecta atletas e academias, estrutura eventos, registra resultados e transforma cada confronto em histórico e ranking auditável.

Nossa missão é dar visibilidade a talentos reais do boxe. Construímos uma plataforma forte, comunitária, neutra e tecnológica para que a trajetória de quem treina e compete não dependa de conversas dispersas ou memória informal.

O ecossistema

Atletas

Academias

Eventos

Juizes e ranking

Perfil público, histórico e classificação individual

Presença institucional, vínculo de atletas e organização de eventos

Inscrições, convites, chaves, card e resultados

Registro por token e recálculo auditável do ranking

flowchart LR
    A[Atleta] --> B[Academia]
    B --> C[Evento]
    C --> D[Juiz]
    D --> E[Resultado]
    E --> F[Ranking]
    F --> A

Jornada do MVP

O atleta cria seu perfil e se vincula a uma academia ou atua como independente.

A academia cria um evento e a administração realiza a aprovação.

O evento recebe inscrições ou convites e o sistema organiza as chaves.

O juiz registra o resultado por um acesso seguro e temporário.

O resultado atualiza o evento, o historico dos atletas e o ranking nacional.

Estado atual

O projeto está em consolidação do MVP funcional. O portal público possui uma experiência navegável, enquanto integrações reais de backend, persistência, autenticação, autorização, operação administrativa e ranking estão em evolução.

O objetivo do primeiro corte é operar de ponta a ponta com atletas, academias, eventos, resultados e ranking nacional. Análise de vídeo por IA, streaming, pagamentos, marketplace e aplicativo mobile permanecem fora do MVP.

Engenharia

A arquitetura alvo prioriza simplicidade operacional, baixo custo e evolução segura:

frontend em React e Tailwind CSS, distribuído por Amazon S3 e CloudFront;

APIs serverless com Amazon API Gateway e AWS Lambda;

persistência em Amazon DynamoDB;

autenticação e autorização com Amazon Cognito;

configuração por ambiente com AWS Systems Manager Parameter Store;

infraestrutura como código com Terraform;

integração e entrega contínua com GitHub Actions;

ambientes oficiais de homologação e produção.

Repositórios principais

Repositório

Responsabilidade

sparringday

Fonte oficial de produto, regras, arquitetura, roadmap e decisões técnicas

sparringday-portal

Portal e experiência principal da plataforma

sparringday-api

Contratos e serviços da API

sparringday-infra

Infraestrutura, ambientes e provisionamento

sparringday-devops

Pipelines, automações e padrões reutilizáveis de CI/CD

Parte do código e da documentação pode exigir acesso enquanto o MVP está em consolidação.

Documentação

Visão geral do projeto

Status atual

Escopo funcional do MVP

Fluxos do MVP

Regras do ranking

Arquitetura

Roadmap

<div align="center">
  <strong>Sua história no boxe merece ser registrada.</strong>
</div>
