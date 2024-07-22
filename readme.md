# Projeto: Google Cloud - Automatizando Funções

Estre projeto foi desenvolvido para solucionar um [desafio](./docs/questions.md) que tem por objetivo aprofundar o entendimento, a prática e a integração dos servicos da Google Cloud.

- **Cloud IAM**
  - Criação de chaves de serviço, criação e gerenciamento de usuários.

- **Cloud Functions**
  - Criação de functions com Python e a utilização do serviço de autenticação.

- **Cloud Build**
  - Gerenciamento de controle de versão e integração com o Cloud Functions.

- **Cloud Scheduler**
  - Agendamento de gatilhos específicos do Cloud Functions.

- **Cloud Storage**
  - Armazenamento de camadas de ETL diretamente do Cloud Functions.

- **BigQuery**
  - Leitura e transformações de dados em SQL.

---

# **Explicação detalhada de cada etapa do processo**

Neste projeto realizei a extração de ações da bolsa de valores através da API do Yahoo Finance (yfinance) através do Cloud Functions, fiz a separação dos dados de cada etapa do ETL no Cloud Storage e, o objetivo do script é automatizar o processo de coleta das informações diariamente às 21hs alimentando fluxo do sistema até chegar nas visualizações no BigQuery.

## **Criação do Projeto**

- Criação do Repositório no Github e Projeto no Google Cloud:
- **Repositório:** <https://github.com/devguilhermecarvalho/gcloud-automated-marketdata>
- **Google Cloud Project:**
  - **Nome do Projeto:** Project Automated Data Market
  - **ID do projeto:** project-automated-data-market
  - **Número do projeto:** 465934427557

## Cloud IAM - Configuração

Para criação das contas de usuários eu optei por escrever um script que ao ser executado faz a criação do usuário e já atribui as permissões e funções.

[Script: Criação de Usuários](./scripts/admin_user_assign_roles.sh)

Contas Criadas:

- **Data Engineer - Administrator**
  - Controle total, apenas das ferramentas utilizadas.

- **Analista - Administrator**
  - Controle de utilização apenas do BigQuery e do Looker.

### **Chave de Acesso:**

A Chave de Acesso/Service Account foi criada apenas para o usuário administrador, que tem controle total de todas as etapas do processo.

## Cloud Functions

- Para a utilização é necessário a ativação das APIs: Cloud Build, Cloud Functions, Cloud Logging API, Cloud Pub/Sub, Cloud Run Admin API

- Ambiente: 2nd gen
- Tipo de Gatilho: HTTPS
- Requer autenticação com o Cloud IAM
- Conta de Serviço: Data Engineer Administrator

## Cloud Build

O Cloud Build é reponsável pelo versionamento do código e um facilitador de desenvolvimento, pois através dele conseguimos conectar o repositório do Github com ambiente do Cloud Functions e sincronizar os arquivos a cada Push.

# Cloud Storage

- **Buckets:**
  - project-data-market
  - **Pastas:**
    - storage-raw-market-data
      - Armazena os arquivos diretamente da API e formato .parquet sem nenhuma tranformação.
    - storage-bronze-market-data
      - Faz a extração do arquivo .parquet para CSV e inclui algumas colunas de cálculos específicos.
    - storage-silver-market-data
      - Storage que fica disponível para armazenamento de análises.
    - storage-gold-market-data
      - Storage que fica disponível para armazenamento de resultados e processos finais.

# Cloud Scheduler
O job do Cloud Scheduler foi configurado de forma simples para ser executado através do gatilho HTTP com o método POST às 21hs de segunda a sexta-feira.

# BigQuery

Até o momento, o BigQuery está sendo utilizado somente para visualização final da tabela, deixando os dados de forma totalmente disponíveis para prosseguir em análise/compartilhamento para um ciêntista ou analista de dados.