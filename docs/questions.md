# Desafio Google Cloud

Extraia dados de uma API e salve no BigQuery.

### Ferramentas a serem utilizadas

- IAM para criar a conta de serviço.
- Cloud Function para extrair dados da API.
- Cloud Build para versionar a Cloud Function.
- Cloud Storage para armazenar os dados antes de enviá-los para o BigQuery.
- BigQuery para armazenar os dados finais.
- Cloud Scheduler para automatizar a execução da Cloud Function.

### Etapas

- **Etapa 0: Criando a Service Account**

    Crie uma conta de serviço para permitir a autenticação e autorização das operações necessárias. Esta conta de serviço será usada para testar localmente na sua máquina.

- **Etapa 1: Versionar usando o Cloud Build**

    Configure o Cloud Build para versionar o código da Cloud Function.
Esta etapa é crucial para automatizar as modificações no código da Cloud Function, facilitando o processo de testes e atualizações.

- **Etapa 2: Extrair dados da API**

    Desenvolva a Cloud Function para realizar a extração dos dados da API especificada.

    Certifique-se de que a função está corretamente configurada para lidar com a autenticação da API e o tratamento de dados.

- **Etapa 3: Salvar no Cloud Storage**

    Configure a Cloud Function para salvar os dados extraídos no Cloud Storage.

    Utilize o Cloud Storage como uma etapa intermediária para garantir que os dados estão disponíveis e seguros antes de serem enviados para o BigQuery.

- **Etapa 4: Salvar no BigQuery**

    Processe e transfira os dados do Cloud Storage para o BigQuery.

    Garanta que os dados estão organizados e formatados corretamente para análise no BigQuery.

- **Etapa 5: Automatização com Cloud Scheduler**

    Utilize o Cloud Scheduler para automatizar a execução periódica da Cloud Function.
    
    Configure a frequência e os horários de execução conforme necessário para manter os dados atualizados no BigQuery.