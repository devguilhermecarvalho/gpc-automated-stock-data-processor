import functions_framework
import pandas as pd
import yfinance as yf
from google.cloud import storage
from flask import make_response
from datetime import datetime

@functions_framework.http
def main(request):
    """
    Função principal para obter, transformar e armazenar dados históricos do mercado de ações no Google Cloud Storage.
    """
    # Inicializa e executa o processo de obtenção de dados históricos
    data_fetcher = GetHistoricalData(request) # Instancia a classe GetHistoricalData
    fetch_response = data_fetcher.get_historical_data() # Executa a função da classe

    if fetch_response.status_code == 200: # Se a resposta for positiva, inicia-se o processo de transformação:
        data_transformer = TransformMarketData(request) # Instancia a classe TransformMarketData
        transform_response = data_transformer.transform_and_save_market_data()

        return transform_response
    else:
        return fetch_response

class GetHistoricalData:
    """
    Classe para obter dados históricos do mercado de ações e armazená-los no Google Cloud Storage.
        
        A função get_historical_data() faz o seguinte:
            1. Define a lista de ações para obter os dados históricos.
            2. Define o período solicitado para obter os dados históricos.
            3. Utiliza a biblioteca yfinance para obter os dados históricos das ações especificadas no período solicitado.
            4. Converte os dados obtidos em um DataFrame do pandas.
            5. Salva os dados brutos em formato Parquet localmente e  cria um cliente do Google Cloud Storage.
            6. Define o nome do bucket e o blob (objeto no bucket) para armazenar os dados históricos.
            7. Faz o upload do arquivo Parquet para o bucket.
            8. Retorna uma resposta com o status 200 se o upload for bem-sucedido, ou 500 em caso de erro.
    """
    def __init__(self, request):
        self.request = request

    def get_historical_data(self):
        try:
            # Lista de ações para obter os dados históricos
            stocks = ['PETR4.SA', 'VALE3.SA', 'ITUB4.SA', 'ABEV3.SA', 'BBDC4.SA']

            # Período solicitado
            request_start_date = '2020-01-01'
            request_end_date = datetime.now().strftime('%Y-%m-%d')

            # Inicializando uma lista para armazenar DataFrames
            all_dataframes = []

            # Download dos dados históricos para cada ação individualmente
            for stock in stocks:
                data = yf.download(stock, start=request_start_date, end=request_end_date)
                df = pd.DataFrame(data)
                df['Stock'] = stock  # Adiciona uma coluna com o nome da ação
                df[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']].round(3)
                all_dataframes.append(df)

            # Concatenando todos os DataFrames em um único DataFrame
            final_df = pd.concat(all_dataframes)

            # Salvando os dados brutos em formato Parquet
            parquet_filename = '/tmp/raw_historical_data_market.parquet'
            final_df.to_parquet(parquet_filename, index=False)

            # Criação do cliente de armazenamento do Google Cloud
            client = storage.Client()

            # Nome do bucket e blob (objeto no bucket)
            bucket_name = 'project-data-market'
            bucket = client.bucket(bucket_name)
            destination_blob_name = 'storage-raw-market-data/raw_historical_data_market.parquet'
            blob = bucket.blob(destination_blob_name)

            # Fazer o upload do arquivo Parquet para o bucket
            blob.upload_from_filename(parquet_filename)

            response_text = f"File '{destination_blob_name}' created/overwritten in bucket '{bucket_name}'."
            response = make_response(response_text)
            response.headers['Content-Type'] = 'text/plain'
            return response
        except Exception as e:
            return make_response(str(e), 500)

class TransformMarketData:
    """
    Classe para transformar os dados históricos do mercado de ações e armazená-los no Google Cloud Storage.
        A função load_historical_data() faz o seguinte:
            1. Carrega o arquivo Raw Parquet do bucket.
            2. Retorna o DataFrame com os dados históricos.

        A função transform_and_save_market_data() faz o seguinte:
            1. Chama a função load_historical_data() para obter os dados históricos.
            2. Resetar o índice do DataFrame.
            3. Arredondar as colunas 'Open', 'High', 'Low', 'Close', 'Adj Close' e 'Volume' para 5 casas decimais.
            4. Salvar o DataFrame transformado como CSV.
            6. Faz o upload do arquivo CSV para a pasta  o bucket .
            8. Retornar uma resposta com o status 200 se o upload for bem-sucedido, ou 500 em caso de erro.
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

            # Transformar os dados
            df = df.reset_index()
            df[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']].round(5)

            # Salvar o DataFrame como CSV localmente
            csv_filename = '/tmp/stocks-market-data.csv'
            df.to_csv(csv_filename, index=False)

            # Criação do cliente de armazenamento do Google Cloud
            client = storage.Client()

            # Salvar o arquivo transformado no bucket
            current_date = datetime.now().strftime('%Y-%m-%d')
            destination_blob_name = f'storage-gold-market-data/stocks-market-data_{current_date}.csv'
            bucket = client.bucket('project-data-market')
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(csv_filename)

            response_text = f"Transformed file '{destination_blob_name}' created in bucket '{bucket.name}'."
            response = make_response(response_text)
            response.headers['Content-Type'] = 'text/plain'
            return response
        except Exception as e:
            return make_response(str(e), 500)