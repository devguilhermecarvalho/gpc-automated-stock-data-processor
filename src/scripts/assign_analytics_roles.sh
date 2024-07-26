#!/bin/bash

# Como executar o arquivo no GCloud CMD:
# 1. Abra a CLI do GCloud e faça a abertura do Editor.
# 2. Crie um novo arquivo .sh e copie o conteúdo abaixo.
# 3. Navegue até o diretório:
#    > chmod +x analytics_user_assign_roles.sh
# 4. Execute o script:
#    > ./analytics_user_assign_roles.sh

# Criando Conta de Serviço:
gcloud iam service-accounts create analytic-administrator
    --description="Service Account for Analytics Administrator"
    --display-name="Analytic administrator"

# Listar Contas de Serviço:
gcloud iam service-accounts list --project=project-automated-data-market

USER_EMAIL="analytic-administrator@project-automated-data-market.iam.gserviceaccount.com"
PROJECT_ID="project-automated-data-market"
REGION="us-central1"
FUNCTION_NAME="project-data-market"


# Conceder papéis de BigQuery
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$USER_EMAIL" \
    --role="roles/bigquery.dataViewer"
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$USER_EMAIL" \
    --role="roles/bigquery.dataEditor"
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$USER_EMAIL" \
    --role="roles/bigquery.jobUser"

# Conceder papéis de Cloud Storage
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$USER_EMAIL" \
    --role="roles/storage.objectViewer"
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$USER_EMAIL" \
    --role="roles/storage.objectCreator"

# Conceder papéis de Dataproc (se necessário)
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$USER_EMAIL" \
    --role="roles/dataproc.viewer"

# Conceder papéis de Pub/Sub (se necessário)
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$USER_EMAIL" \
    --role="roles/pubsub.subscriber"