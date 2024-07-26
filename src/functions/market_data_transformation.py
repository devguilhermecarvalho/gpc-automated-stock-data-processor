import functions_framework
import pandas as pd
import yfinance as yf
from google.cloud import storage
from flask import make_response
from datetime import datetime

class TransformMarketData:
    """
    Classe para transformar os dados históricos do mercado de ações e armazená-los no Google Cloud Storage.
        A função load_historical_data() faz o seguinte:
            1. Carrega o arquivo Raw Parquet do bucket.
            2. Retorna o DataFrame com os dados históricos.

        A função transform_and_save_market_data() faz o seguinte:
            1. Carrega os dados históricos do arquivo Raw Parquet.
            2. Calcula a média entre a abertura e o fechamento.
            3. Calcula a diferença entre a abertura e o fechamento.
            4. Calcula a variação percentual do dia passado e do dia atual.
            5. Calcula a variação percentual do mês passado e do mês atual.
            6. Salva o DataFrame transformado em um arquivo CSV localmente.
            7. Faz o upload do arquivo CSV para o bucket.
            8. Retorna uma resposta com o status 200 se o upload for bem-sucedido, ou 500 em caso de erro.
    """
    def __init__(self, request):
        self.request = request

    def load_historical_data(self):
        try:
            # Criação do cliente de armazenamento do Google Cloud
            client = storage.Client()

            # Carregar arquivo da pasta raw do bucket
            load_bucket_name = 'project-data-market'
            bucket = client.bucket(load_bucket_name)
            blob = bucket.blob('storage-raw-market-data/raw_historical_data_market.parquet')

            parquet_filename = '/tmp/raw_historical_data_market.parquet'
            blob.download_to_filename(parquet_filename)

            df = pd.read_parquet(parquet_filename)
            return df
        except Exception as e:
            raise RuntimeError(f"Error loading data: {e}")

    def transform_and_save_market_data(self):
        try:
            # Carregar dados históricos
            df = self.load_historical_data()

            # Calcula a média entre a abertura e o fechamento
            df['Average'] = (df['Open'] + df['Close']) / 2

            # Calcula a diferença entre a abertura e o fechamento
            df['Difference'] = df['Close'] - df['Open']

            # Calcula a variação percentual do dia passado e do dia atual
            df['Daily_Variation'] = (df['Close'] - df['Open']) / df['Open'] * 100

            # Calcula a variação percentual do mês passado e do mês atual
            df['Monthly_Variation'] = (df['Close'] - df['Open']) / df['Open'] * 100

            # Salvar o DataFrame como CSV localmente
            csv_filename = '/tmp/stocks-market-data.csv'
            df.to_csv(csv_filename, index=False)

            # Criação do cliente de armazenamento do Google Cloud
            client = storage.Client()

            # Salvar o arquivo transformado no bucket
            current_date = datetime.now().strftime('%Y-%m-%d')
            destination_blob_name = f'storage-bronze-market-data/stocks-market-data_{current_date}.csv'
            bucket = client.bucket('project-data-market')
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(csv_filename)

            response_text = f"Transformed file '{destination_blob_name}' created in bucket '{bucket.name}'."
            response = make_response(response_text)
            response.headers['Content-Type'] = 'text/plain'
            return response
        except Exception as e:
            return make_response(str(e), 500)