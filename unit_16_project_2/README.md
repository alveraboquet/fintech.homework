# Crypto Adviser: Agent to the Moon

## Team Members

* Brian Hampson

<br>

- - -

<br>

## Project Description

<br>

The objective of this project is to build a cryptocurrency notification agent that will continuously monitor OHLCV data and trigger alerts when common market indicators exceed configurable thresholds. When an alert is triggered, various ML models (LSTM RNN, Linear Regression, and GARCH) will be employed to predict future price action . Additionally, NLP will be leveraged to perform sentiment analysis on recent news articles. Resultant data will be summarized and then emailed or text messaged to subscribed recipients.

<br>

- - -

<br>

## Data Sources


* Crypto OHLCV - CCXT - Kraken
* News headlines - newsapi

<br>

- - -

<br>

## Machine Learning Models

* LSTM RNN
* Linear Regression
* GARCH (???)
* nltk.sentiment.vader SentimentIntensityAnalyzer
* word cloud (time permitting)

<br>

- - -

<br>

## Task Breakdown

* setup git repo
* initial project planning, readme
* investigation
    * data sources
    * machine learning models
    * trading signals
* high level architecture and design
* models - using google colab
    * for each model
        * clean data
        * build and train
        * back-testing
        * save model on S3
* lambda development
    * lambda security, roles and permissions        
        * IAM app user
        * S3 read/write access
    * logging
    * read agent config from S3
    * read model from S3
    * run lambda on schedule
    * OHLCV - data caching - optimize data calls, ensure sufficient historical data
    * fetch and clean data
    * evaluate trading signals
    * run ML models, make predictions
    * plots and graphs (save to S3, access from email)
    * summarize results
    * send email or text
* Configure S3 storage 
* build presentation
* finalize readme

## Next steps
* persistant storage - DynamoDB
    * tables
        * agent
            * alerts
            * triggers
        * openTrades
        * completedTrades
* REST API to encapsulate data calls and updates to DynamoDB
* web dashboard



























