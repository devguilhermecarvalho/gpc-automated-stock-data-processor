#!/bin/bash

# Criando Conta de Serviço:
gcloud iam service-accounts create data-engineer-administrator \
    --description="Usuário administrador geral" \
    --display-name="Data Engineer - Administrator" 

# Lista Contas de Serviço:
gcloud iam service-accounts list --project=project-automated-data-market

# Como executar o arquivo no GCloud CMD ↓
# Navega até o diretório:
    # > chmod +x assign_roles.sh
# Executa o script:
    # > ./assign_roles.sh

# Substitua USER_EMAIL pelo e-mail do usuário e PROJECT_ID pelo ID do seu projeto
USER_EMAIL="data-engineer-administrator@project-automated-data-market.iam.gserviceaccount.com"
PROJECT_ID="project-automated-data-market"
REGION="us-central1"
FUNCTION_NAME="project-data-market"

# Adiciona função Cloud Functions Admin
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$USER_EMAIL" \
  --role="roles/cloudfunctions.admin"

# Adiciona função Storage Admin
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$USER_EMAIL" \
  --role="roles/storage.admin"

# Adiciona função BigQuery Admin
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$USER_EMAIL" \
  --role="roles/bigquery.admin"

# Adiciona função Cloud Build Editor
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$USER_EMAIL" \
  --role="roles/cloudbuild.builds.editor"

# Adiciona função Cloud Scheduler Admin
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$USER_EMAIL" \
  --role="roles/cloudscheduler.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$USER_EMAIL" \
  --role="roles/compute.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
   --member="serviceAccount:$USER_EMAIL" \
   --role="roles/storage.objectViewer"

gcloud projects add-iam-policy-binding $PROJECT_ID \
   --member="serviceAccount:$USER_EMAIL" \
   --role="roles/storage.objects.get"

gcloud functions add-invoker-policy-binding $PROJECT_ID \
    --region="us-central1" \
    --member="serviceAccount:$USER_EMAIL"

gcloud projects add-iam-policy-binding $PROJECT_ID \
   --member="serviceAccount:$USER_EMAIL" \
   --role="roles/run.invoker"

# Listar funções na região especificada
gcloud functions list --project=$PROJECT_ID --regions=$REGION

# Adicionar permissão de invocação à função se existir
if gcloud functions describe $FUNCTION_NAME --project=$PROJECT_ID --regions=$REGION; then
    gcloud functions add-invoker-policy-binding $FUNCTION_NAME \
        --regions=$REGION \
        --member="serviceAccount:$USER_EMAIL"
else
    echo "Função $FUNCTION_NAME não encontrada na região $REGION."
    