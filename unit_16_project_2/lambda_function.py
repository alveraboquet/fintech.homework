import json
import os
import boto3
import io
import csv
import sys

from pathlib import Path
from datetime import datetime, timedelta
from io import StringIO

# Imports require CryptoAgent Layer
import ccxt
import numpy as np
import pandas as pd

def lambda_handler(event, context):
    
    # Load env vars
    API_PUBLIC_KEY = os.getenv('API_PUBLIC_KEY')
    API_PRIVATE_KEY = os.getenv('API_PRIVATE_KEY')
    API_PAGE_SIZE = os.getenv('API_PAGE_SIZE')
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
    CACHE_FILE_NAME = os.getenv('CACHE_FILE_NAME')
    
    # Log event
    print(f'## EVENT - {event}')
    
    # Load cache from S3
    cache_df = load_cache(S3_BUCKET_NAME, CACHE_FILE_NAME)
    
    # If cache not found, init with 60 days worth of OHLCV
    if cache_df is None: 

        # Get datetime - today minus 60 days
        cache_start_datetime = datetime.today() - timedelta(days=60)
        
        # Convert to milliseconds
        cache_start_ms = cache_start_datetime.timestamp() * 1000
        
        # Log 
        print(f'Cache is empty. Initializing with data starting from {cache_start_datetime}.')
        
        # Init cache with 60d of data
        cache_df = fetch_OHLCV_API('BTC/USD', '1d', cache_start_ms, API_PUBLIC_KEY, API_PRIVATE_KEY)
        
        # Save cache to S3
        save_cache(S3_BUCKET_NAME, CACHE_FILE_NAME, cache_df)

    else:

        # Debug
        print(f'Cache found. {cache_df.shape[0]} records.')
        
        # Get cache end date in ms 
        end_date_ms = cache_df.iloc[-1, 0]
        
        # Call API for latest data
        latest = fetch_OHLCV_API('BTC/USD', '1d', end_date_ms, API_PUBLIC_KEY, API_PRIVATE_KEY)
        
        # Log 
        print(f'Fetching latest data. Adding {latest.shape[0]} records.')
        
        # Append latest data
        cache_df.append(latest)
        
        # Log 
        print(f'Total {cache_df.shape[0]} records.')
    
        # Save cache to S3
        save_cache(S3_BUCKET_NAME, CACHE_FILE_NAME, cache_df)

    
    # Return success response
    return success_response(f"Found cache with {cache_df.shape[0]} records!")


def success_response(msg):
    return {
        'statusCode': 200,
        'body': json.dumps(msg)
    }
    
def error_response(errCode, msg):
    return {
        'statusCode': errCode,
        'body': msg
    }
    
def load_cache(bucket, key):
  
    # Init boto3 client
    s3 = boto3.client('s3')
    
    try:
    
        # Get cache object
        obj = s3.get_object(Bucket=bucket, Key=key)
    
        # Read bytes
        data = io.BytesIO(obj['Body'].read())
        
        # Init dataframe
        df = pd.read_csv(
            data, 
            encoding='utf8',
            index_col="date",
            infer_datetime_format=True,
            parse_dates=True)
            
        return df
    
    except Exception as e: 
        
        # Log exception and return None
        print(f'load_cache exception: {e}')
        return None

    
def save_cache(bucket, key, cache):
    
    # Write cache to csv
    csv_buffer = StringIO()
    cache.to_csv(csv_buffer)
    
    # Get S3 resource
    s3_resource = boto3.resource('s3')
    
    # Put object
    s3_resource.Object(bucket, key).put(Body=csv_buffer.getvalue())
    
    # TODO - add exception handling
    return

def fetch_OHLCV_API(ticker, timeframe, since, api_key, api_secret):

    # Init CCXT Kraken API
    exchange = ccxt.kraken({
        'apiKey': api_key, 
        'secret': api_secret })
        
    btc_ohlcv = []

    while since < exchange.milliseconds ():
    
        # Page size
        limit = 20
        day_in_ms = 86400000
    
        # Fetch paged data 
        ohlcv_page = exchange.fetch_ohlcv(ticker, timeframe, since)
    
        if len(ohlcv_page):
    
            # Update since - last item in page + 86400000
            since = ohlcv_page[-1][0] + day_in_ms
    
            # Append page
            btc_ohlcv += ohlcv_page
        else:
            break
    
    # Init df
    btd_df = pd.DataFrame(btc_ohlcv)
    
    # Rename columns
    btd_df.columns = ['ms', 'open','high','low','close','volume']
    
    # Parse date
    btd_df['date'] = btd_df['ms'].apply(exchange.iso8601)
    
    # Set date as index 
    btd_df.set_index(pd.to_datetime(btd_df['date'], infer_datetime_format=True), inplace=True)
    
    # Drop temp columns
    btd_df.drop(btd_df.columns[6], axis=1, inplace=True)
    
    return btd_df




# print(f'## ENVIRONMENT - {os.environ}')


    # # Init boto3 client
    # s3 = boto3.client('s3')
    
    # # Params
    # bucket = 'crypto-agent-2021-03-14'
    # key = 'btc_ohlcv_cache.csv'
    
    # # Get cache object
    # obj = s3.get_object(Bucket=bucket, Key=key)
    
    # # Read bytes
    # data = io.BytesIO(obj['Body'].read())
    
    # # Init dataframe
    # df = pd.read_csv(
    #     data, 
    #     encoding='utf8',
    #     index_col="date",
    #     infer_datetime_format=True,
    #     parse_dates=True)
    
    
    
        # csv_buffer = StringIO()
    # df.to_csv(csv_buffer)
    # s3_resource = boto3.resource('s3')
    # s3_resource.Object(bucket, 'test.csv').put(Body=csv_buffer.getvalue())