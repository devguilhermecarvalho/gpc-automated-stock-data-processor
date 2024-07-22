# Projeto: Google Cloud - Automatizando Funções

> Este projeto ter por objetivo entender o funcionamento e a integração dos servicos **Cloud IAM**, **Cloud Functions**, **Cloud Build**, **Cloud Scheduler**, **Cloud Storage** e **BigQuery**.

## Parte 01 - Criação do Projeto

Neste projeto estarei fazendo a extração de ações da bolsa de valores através da API do Yahoo Finance (yfinance), e automatizando o processo de coleta das cotações diariamente.

- Criação do Repositório no Github e Projeto no Google Cloud:
- Repositório: https://github.com/devguilhermecarvalho/gcloud-automated-marketdata
- Google Project:
    - **Nome do Projeto:** Project Automated Data Market
    - **ID do projeto:** project-automated-data-market
    - **Número do projeto:** 465934427557

## Cloud IAM - Configuração
Criação de contas de serviços:

- Conta Administrador:
    DataEngineer-Administrador
    - Administrador Cloud Functions
    - Administrador de Conexão Cloud Build
    - Administrador Cloud Storage
    - Administrador Cloud Scheduler
    - Administrador BigQuery

    - **Chave de Acesso:** service_account.json
- Conta Analista: data-analyst-administrator
    - Administrador BigQuery
    - Adiministrador Looker


## Cloud Functions
 - APIs Ativadas para utilização: Cloud Build, Cloud Functions, Cloud Logging API, Cloud Pub/Sub, Cloud Run Admin API

- Ambiente: 2nd gen
- Nome de função: project-test-cf-market-data
- região: us-central1
- Tipo de Gatilho: HTTPS
- Requer autenticação com o Cloud IAM
- Conta de Serviço: Data Engineer Administrator

## Cloud Build

- Nome: Project-test-build-market-data
- Evento: Enviar para uma ramificação (Será atualizado conforme o repositório)
- Fonte: 1gen

# Cloud Storage
- **Buckets:**
    - project-data-market
    - **Pastas:**
        - storage-raw-market-data
            - Armazena os arquivos históricos como .parquet.
        - storage-gold-market-data
            - Armazena os arquivos .CSV prontos para carregamento no BigQuery e análises.


gcloud projects add-iam-policy-binding project-data-market \ --member=serviceAccout:data-engineer-administrator@project-automated-data-market.iam.gserviceaccount.com --role=roles/storage.objectViewer

