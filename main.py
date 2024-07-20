import functions_framework
import pandas as pd
import yfinance as yf
from google.cloud import storage
from flask import make_response
import os
from datetime import datetime

@functions_framework.http
def hello_http(request):
    try:
        # Baixar os dados
        ativos = ['PETR4.SA']
        start_date = '2020-01-01'
        end_date = '2024-07-01'
        data = yf.download(ativos, start=start_date, end=end_date)
        df = pd.DataFrame(data)

        # Reseta o index para transformar a data em uma nova coluna
        df.reset_index(inplace=True)

        # Arredonda as colunas numéricas para 3 casas decimais
        df[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']].round(3)
        
        # Salvar o DataFrame como CSV localmente
        csv_filename = '/tmp/petr4_data.csv'
        df.to_csv(csv_filename, index=False)
        
        # Configurar o cliente do Google Cloud Storage
        client = storage.Client()
        bucket_name = 'data_market_api_project'
        bucket = client.bucket(bucket_name)
        
        # Nome do arquivo no bucket
        current_date = datetime.now().strftime('%Y-%m-%d')
        destination_blob_name = f'petr4_data_{current_date}.csv'
        blob = bucket.blob(destination_blob_name)
        
        # Fazer o upload do arquivo CSV para o bucket
        if blob.exists():
            blob.upload_from_filename(csv_filename)
            response_text = f"Cloud Build Ok - File '{destination_blob_name}' already existed and has benn overwritten in bucket '{bucket_name}'."
        else:
            blob.upload_from_filename(csv_filename)
            response_text = f"Cloud Build Ok -File '{destination_blob_name}' created in bucket '{bucket_name}'."
        
        # Retornar a URL do arquivo no bucket
        response = make_response(response_text)
        response.headers['Content-Type'] = 'text/plain'
        
        return response
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        response = make_response(error_message)
        response.headers['Content-Type'] = 'text/plain'
        response.status_code = 500
        
        return response