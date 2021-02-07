# Unit 10—A Yen for the Future


## Background

The financial departments of large companies often deal with foreign currency transactions while doing international business. As a result, they are always looking for anything that can help them better understand the future direction and risk of various currencies. Hedge funds, too, are keenly interested in anything that will give them a consistent edge in predicting currency movements.

- - -

## Data

[Yen Data](data/yen.csv)

- - -

## Time-Series Forecasting

<br>

[Time-Series Analysis Notebook](./time_series_analysis.ipynb)

### Concepts

* Auto-Regressive (AR) Models 
    * use past to predict future
    * assumes some degress of autocorrelation
    * may have one or more significant lags*
* Moving Average (MA) Models
    * predicts future values based on past values at specified lag...
    * ...and number of significant lags
* ARMA: Automregressive Moving Average Model
    * assumes stationarityh
* ARMIMA: AutoRegressive Integrated Moving Average
    * can be applied to non-stationary data
* Stationarity: mean and variance constant across time
    * to stationize data: pct_change or diff
* Use AIC and BIC for goodness of fit (lower the better)
    * Akaike information criterion
    * Bayesian information criterion

<br>

### Questions and Answers

* <strong>Question:</strong> Based on your time series analysis, would you buy the yen now?
* <strong>Answer:</strong> I would not buy the Japanese Yen at this time

<br>

* <strong>Question:</strong> Is the risk of the yen expected to increase or decrease?
* <strong>Answer:</strong> Volatility and thus risk is increasing in the near short-term

<br>

* <strong>Question:</strong> Based on the model evaluation, would you feel confident in using these models for trading?
* <strong>Answer:</strong> Volatility and thus risk is increasing in the near short-term


- - -

## Linear Regression Forecasting

[Linear Regression Analysis Notebook](./regression_analysis.ipynb)

<br>

* <strong>Question:</strong> Does this model perform better or worse on out-of-sample data compared to in-sample data?
* <strong>Answer:</strong>This particular model performs better on out-of-sample data as compared to training data.

