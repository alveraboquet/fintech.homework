# from sklearn.metrics import mean_squared_error, r2_score
# import tensorflow as tf
# from tensorflow import random
# from tensorflow import keras
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import LSTM, Dense, Dropout

import json
import os
import boto3
import io
import csv
import sys

from pathlib import Path
from datetime import datetime, timedelta
from io import StringIO
from botocore.exceptions import ClientError

# Layer: numpy_pandas_ccxt_layer
import ccxt
import numpy as np
import pandas as pd

def lambda_handler(event, context):
    
    # Log event obj
    print(f'*** EVENT *** - {event}')
    
    # Load environment vars
    API_PUBLIC_KEY = os.getenv('API_PUBLIC_KEY')
    API_PRIVATE_KEY = os.getenv('API_PRIVATE_KEY')
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
    CACHE_FILE_NAME = os.getenv('CACHE_FILE_NAME')
    ALERT_WINDOW = int(os.getenv('ALERT_WINDOW'))
    API_PAGE_SIZE = int(os.getenv('API_PAGE_SIZE'))
    EMAIL_SENDER = os.getenv('EMAIL_SENDER')
    EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS')
    
    # Init CacheManager
    cm = CacheManager(
        API_PUBLIC_KEY, 
        API_PRIVATE_KEY, 
        S3_BUCKET_NAME, 
        CACHE_FILE_NAME)
    
    # Load cache from S3 and get latest from API
    ohlcv_df = cm.load_and_fetch_OHLCV()
    
    # Calculate trading signals
    # Contains full dataset for plotting
    signals_df = get_trading_signals_df(ohlcv_df)
    
    # Get alerts
    alerts_ls = get_alerts(signals_df, ALERT_WINDOW)
    
    # Further processing required if there are alerts
    if len(alerts_ls) > 0:
    
        # Generate plots and save to S3
        plot_signals(signals_df)
        
        # TODO
        # Load Keras model from S3
        # Make price predictions
        # Additional plotting
        # Summarize results
        
        # Send email
        send_email(EMAIL_SENDER, EMAIL_RECIPIENTS, alerts_ls)

        #  Log 
        print(f'DEBUG - {len(alerts_ls)} alerts triggered!')

    # Return success response
    return success_response(f'*** RESPONSE *** - Found cache with {ohlcv_df.shape[0]} records. Alerts: {json.dumps(alerts_ls)}')

    
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


def calc_ema_alert(row):
    if row['ema_signal'] == 1 :
        return 'EWMA 30/60 crossover, potential long position'
    if row['ema_signal'] == -1:
        return 'EWMA 30/60 crossover, potential short position'
    return ''


def calc_bollinger_alert(row):
    if row['bollinger_signal'] == 1 :
        return 'Bollinger 30 day crossover, potential long position'
    if row['bollinger_signal'] == -1:
        return 'Bollinger 30 day crossover, potential short position'
    return '' 


def get_trading_signals_df(ohlcv_df):

    # Log
    print(f'DEBUG - get_trading_signals_df - {ohlcv_df.shape[0]} records')
    
    # Trading signal params
    short_window = 30
    long_window = 60
    bollinger_window = 30
    
    # Make copy of df and drop nulls
    btc_ohlcv = ohlcv_df.copy().dropna()
    
    # Calculate daily returns
    btc_ohlcv['daily_return'] = btc_ohlcv['close'].pct_change()
    
    # Need to init calculated fields
    btc_ohlcv["ema_chg"] = 0.0
    btc_ohlcv["ema_signal"] = 0.0
    btc_ohlcv["ema_alert"] = ''
    
    # Calculate exponential moving average  
    btc_ohlcv["ema_30"] = btc_ohlcv["close"].ewm(halflife=short_window).mean()
    btc_ohlcv["ema_60"] = btc_ohlcv["close"].ewm(halflife=long_window).mean()
    btc_ohlcv["ema_chg"][short_window:] = np.where(btc_ohlcv["ema_30"][short_window:] > btc_ohlcv["ema_60"][short_window:], 1.0, 0.0)
    btc_ohlcv["ema_signal"] = btc_ohlcv["ema_chg"].diff()
    btc_ohlcv["ema_alert"] = btc_ohlcv.apply(lambda row: calc_ema_alert(row), axis=1)
    
    # Calculate rolling mean and standard deviation
    btc_ohlcv['bollinger_mid_band'] = btc_ohlcv['close'].rolling(window=bollinger_window).mean()
    btc_ohlcv['bollinger_std'] = btc_ohlcv['close'].rolling(window=20).std()
    
    # Calculate upper and lowers bands of bollinger band
    btc_ohlcv['bollinger_upper_band'] = btc_ohlcv['bollinger_mid_band'] + (btc_ohlcv['bollinger_std'] * 1)
    btc_ohlcv['bollinger_lower_band'] = btc_ohlcv['bollinger_mid_band'] - (btc_ohlcv['bollinger_std'] * 1)
    
    # Calculate bollinger band trading signal
    btc_ohlcv['bollinger_long'] = np.where(btc_ohlcv['close'] < btc_ohlcv['bollinger_lower_band'], 1.0, 0.0)
    btc_ohlcv['bollinger_short'] = np.where(btc_ohlcv['close'] > btc_ohlcv['bollinger_upper_band'], -1.0, 0.0)
    btc_ohlcv['bollinger_signal'] = btc_ohlcv['bollinger_long'] + btc_ohlcv['bollinger_short']
    
    return btc_ohlcv[['ms','close','daily_return','ema_30','ema_60','ema_chg','ema_signal', 'ema_alert']].dropna()  


def get_alerts(signals_df, alert_window):

  # Filter signals based on alert_window and ema_alert
  alerts_df = signals_df.iloc[-alert_window:,:].query('not ema_signal == 0')[['close','ema_alert']]
  alerts_df['datetime'] = alerts_df.index.format()
  alerts_df = alerts_df[['datetime','close','ema_alert']]

  # Convert to list of tuples
  alerts_ls = [tuple(x) for x in alerts_df.to_records(index=False)]

  return alerts_ls


def send_email(sender, recipient, alerts):
    
    # Log
    print(f'DEBUG - Sending email alert from: {sender} to {recipient}')
    
    # Email params
    CONFIGURATION_SET = 'ConfigSet'
    AWS_REGION = 'us-west-2'
    SUBJECT = 'Crypto Advisor - BTC Alert!'
    BODY_TEXT = 'testing body text'
    BODY_HTML = get_email_body(alerts)
    CHARSET = 'UTF-8'
    
    # Init SES client
    client = boto3.client('ses', region_name = AWS_REGION)

    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination = { 'ToAddresses': [recipient,] },
            Message = {
                'Body': {
                    'Html': { 'Charset': CHARSET, 'Data': BODY_HTML },
                    'Text': { 'Charset': CHARSET, 'Data': BODY_TEXT },
                },
                'Subject': { 'Charset': CHARSET, 'Data': SUBJECT }
            },
            Source = sender
        )
        # Display an error if something goes wrong.	
    except ClientError as e:
        print(f"ERROR - Client error sending email: {e.response['Error']['Message']}")
    else:
        print(f'DEBUG - Email success, message id: {response["MessageId"]}')


def get_email_body(alerts):

    alerts_html = get_alerts_html(alerts)

    html = f"""
        <html>
            <body>
                <img src='https://crypto-agent-public.s3-us-west-2.amazonaws.com/email_header.png' alt='Crypto Advisor'/>   
                <h2>Triggers</h2>
                <p>
                    The following technical indicators have triggered an alert for Bitcoin:
                    {alerts_html}
                </p><br/><br/>
                <img src='https://crypto-agent-public.s3-us-west-2.amazonaws.com/btc_ema_30_60.png' alt='BTC plot'/>
                <h2>Model Predictions</h2>
                <p>
                    <ul>
                        <li>LSTM</li>
                        <li>Linear Regression</li>
                    </ul>
                </p>
                <br/><br/>
                <h2>Headlines</h2>
                Include relevent market news.
                <br/><br/>
                <h2>Sentiment Analysis</h2>    
                Summarize sentiment analyis scores for latest news headlines.    
            </body>
        </html>
        """ 
    return html

def get_alerts_html(alerts):
    list_html = '<ul>'
    for item in alerts: list_html += f'<li>{item[2]}</li>'
    list_html += '</ul>'
    return list_html


def plot_signals(df):
    try:
        # plt = df[['close', 'ema_30', 'ema_60']].plot(figsize=(20,10))
        test = ''
    except Exception as err:
        exception_type = type(err).__name__
        print(f'ERROR - {exception_type}')


class CacheManager:

    def __init__(self, api_key, api_secret, s3_bucket, s3_key):
        """Constructs CacheManager object."""
        
        # Log
        print(f'DEBUG - Initializing cache manager')
    
        self.api_key = api_key
        self.api_secret = api_secret
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        
        # Cache data
        self.cache_df = None
        
        # Init boto3 client
        self.s3_client = boto3.client('s3')
        
        # Init CCXT Kraken API
        self.api = ccxt.kraken({
            'apiKey': self.api_key, 
            'secret': self.api_secret })
        
    
    def load_and_fetch_OHLCV(self):
        
        # Load cache from S3
        self._load_cache()
        
        # If cache not found, init with 60 days worth of OHLCV
        if self.cache_df is None: 
        
            # Get datetime - today minus 60 days
            cache_start_datetime = datetime.today() - timedelta(days=60)
            
            # Convert to milliseconds
            cache_start_ms = cache_start_datetime.timestamp() * 1000
            
            # Log 
            print(f'DEBUG - Cache is empty. Initializing with data starting from {cache_start_datetime}.')
            
            # Init cache with 60d of data
            self.cache_df = self._fetch_OHLCV('BTC/USD', '1d', cache_start_ms)
            
            # Save cache to S3
            self._save_cache()
        
        else:
        
            # Debug
            print(f'DEBUG - Cache found with {self.cache_df.shape[0]} records.')
            
            # Get cache end date in ms 
            end_date_ms = self.cache_df.iloc[-1, 0] + 86400000
            
            # Call API for latest data
            latest = self._fetch_OHLCV('BTC/USD', '1d', end_date_ms)
                
            if not latest is None:
                
                # Log 
                print(f'DEBUG - Fetching latest data, adding {latest.shape[0]} records.')
                
                # Append latest data
                self.cache_df = self.cache_df.append(latest, ignore_index=False)
                
                # Save cache to S3
                self._save_cache()
            
            # Log 
            print(f'DEBUG - Cache has {self.cache_df.shape[0]} records.')
        
        return self.cache_df
    

    def _load_cache(self):

        try:
        
            # Get cache object
            obj = self.s3_client.get_object(Bucket=self.s3_bucket, Key=self.s3_key)
            
            # Read bytes
            data = io.BytesIO(obj['Body'].read())
        
            # Init cache dataframe
            self.cache_df = pd.read_csv(
                data, 
                encoding='utf8',
                index_col="date",
                infer_datetime_format=True,
                parse_dates=True)
        
            return True
        
        except Exception as e: 
        
            # Log exception and return None
            print(f'load_cache exception: {e}')
            return False
    
    def _save_cache(self):
    
        if self.cache_df is None: return False
            
        # Write cache to csv
        csv_buffer = StringIO()
        self.cache_df.to_csv(csv_buffer)
        
        # Get S3 resource
        s3_resource = boto3.resource('s3')
        
        # Put object
        s3_resource.Object(self.s3_bucket, self.s3_key).put(Body=csv_buffer.getvalue())
        
        # TODO - add exception handling
        return True
    
    
    def _fetch_OHLCV(self, ticker, timeframe, since):
    
        btc_ohlcv = []
        
        while since < self.api.milliseconds ():
        
            # Page size
            limit = 20
            day_in_ms = 86400000
            
            # Fetch paged data 
            ohlcv_page = self.api.fetch_ohlcv(ticker, timeframe, since)
            
            if len(ohlcv_page):
            
                # Update since - last item in page + 86400000
                since = ohlcv_page[-1][0] + day_in_ms
            
                # Append page
                btc_ohlcv += ohlcv_page
                
            else:
                break
        
        # Init df
        btd_df = pd.DataFrame(btc_ohlcv)
        
        # If no data returned, return None
        if btd_df.shape[0] == 0: return None
        
        # Rename columns
        btd_df.columns = ['ms', 'open','high','low','close','volume']
        
        # Parse date
        btd_df['date'] = btd_df['ms'].apply(self.api.iso8601)
        
        # Set date as index 
        btd_df.set_index(pd.to_datetime(btd_df['date'], infer_datetime_format=True), inplace=True)
        
        # Drop temp columns
        btd_df.drop(btd_df.columns[6], axis=1, inplace=True)
        
        return btd_df
    

