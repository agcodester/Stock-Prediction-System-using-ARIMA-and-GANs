# -*- coding: utf-8 -*-
"""ATS + ATML Project.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rGZ_z_TNJr_t7NMhuF-8bA8MaZbUa-oc

##Installing Libraries
"""

!pip install streamlit yfinance plotly

# pip install streamlit yfinance plotly tensorflow
import streamlit as st
from datetime import date, timedelta

import yfinance as yf
from plotly import graph_objs as go
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential, Model, load_model
from tensorflow.keras.layers import Dense, LeakyReLU, Reshape, LSTM, Input
from tensorflow.keras.optimizers import Adam

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('Stock Forecast App using GAN')

stocks = ('GOOG', 'AAPL', 'MSFT', 'GME')
selected_stock = st.selectbox('Select dataset for prediction', stocks)

n_years = st.slider('Years of prediction:', 1, 4)
period = n_years * 365

@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text('Loading data...')
data = load_data(selected_stock)
data_load_state.text('Loading data... done!')

st.subheader('Raw data')
st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
    fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

# Prepare data for GAN
def create_dataset(dataset, time_step=1):
    X, Y = [], []
    for i in range(len(dataset)-time_step-1):
        a = dataset[i:(i+time_step), 0]
        X.append(a)
        Y.append(dataset[i + time_step, 0])
    return np.array(X), np.array(Y)

time_series_data = data[['Date', 'Close']]
time_series_data.set_index('Date', inplace=True)
time_series_data = time_series_data.rename(columns={"Close": "Value"})

time_step = 10
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(time_series_data['Value'].values.reshape(-1, 1))

X_train, y_train = create_dataset(scaled_data, time_step)
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)

# Build the generator
def build_generator():
    model = Sequential()
    model.add(Dense(100, input_dim=time_step))
    model.add(LeakyReLU(alpha=0.2))
    model.add(Dense(time_step, activation='tanh'))
    model.add(Reshape((time_step, 1)))
    return model

# Build the discriminator
def build_discriminator():
    model = Sequential()
    model.add(LSTM(50, input_shape=(time_step, 1)))
    model.add(Dense(1, activation='sigmoid'))
    return model

# Build and compile the discriminator
discriminator = build_discriminator()
discriminator.compile(loss='binary_crossentropy', optimizer=Adam(0.0002, 0.5), metrics=['accuracy'])

# Build the generator
generator = build_generator()

# The generator takes noise as input and generates data
z = Input(shape=(time_step,))
generated_data = generator(z)

# For the combined model, we will only train the generator
discriminator.trainable = False

# The discriminator takes generated data as input and determines validity
validity = discriminator(generated_data)

# The combined model (stacked generator and discriminator)
combined = Model(z, validity)
combined.compile(loss='binary_crossentropy', optimizer=Adam(0.0002, 0.5))

# Training the GAN
epochs = 1000
batch_size = 32
valid = np.ones((batch_size, 1))
fake = np.zeros((batch_size, 1))

for epoch in range(epochs):
    # Train Discriminator
    idx = np.random.randint(0, X_train.shape[0], batch_size)
    real_data = X_train[idx]
    noise = np.random.normal(0, 1, (batch_size, time_step))
    gen_data = generator.predict(noise)
    d_loss_real = discriminator.train_on_batch(real_data, valid)
    d_loss_fake = discriminator.train_on_batch(gen_data, fake)
    d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

    # Train Generator
    noise = np.random.normal(0, 1, (batch_size, time_step))
    g_loss = combined.train_on_batch(noise, valid)

    # Print progress
    if epoch % 1000 == 0:
        print(f"{epoch} [D loss: {d_loss[0]} | D accuracy: {100*d_loss[1]}] [G loss: {g_loss}]")

# Save models
generator.save('gan_generator.h5')
discriminator.save('gan_discriminator.h5')

generator.save('gan_generator.h5')
discriminator.save('gan_discriminator.h5')

!python -m pip install prophet

"""# Streamlit Code:

## Importing Libraries:
"""

import streamlit as st
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import date
from datetime import datetime, timedelta
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from plotly import graph_objs as go
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from prophet import Prophet
from prophet.plot import plot_plotly
import scipy.stats as stats

"""## Data Collection:"""

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('Stock Forecast App using GAN and ARIMA/SARIMA')

# Data Collection
stocks = ('GOOG', 'AAPL', 'MSFT', 'GME', 'TSLA')
selected_stock = st.selectbox('Select dataset for prediction', stocks)

n_years = st.slider('Years of prediction:', 1, 4)
period = n_years * 365

@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

data_load_state = st.text('Loading data...')
data = load_data(selected_stock)
data_load_state.text('Loading data... done!')

"""## Exploratory Data Analysis (EDA)

"""

# Exploratory Data Analysis (EDA)
st.subheader('Raw data')
st.write(data.tail())

# Line Graph
st.subheader('Line Graph')
fig = go.Figure()
fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="Stock Close Price"))
fig.layout.update(title_text='Stock Close Price Over Time')
st.plotly_chart(fig)

# Scatter Plot
st.subheader('Scatter Plot')
fig = go.Figure()
fig.add_trace(go.Scatter(x=data['Open'], y=data['Close'], mode='markers', name='Open vs Close'))
fig.layout.update(title_text='Open vs Close Price')
st.plotly_chart(fig)

# Histogram
st.subheader('Histogram')
fig = go.Figure()
fig.add_trace(go.Histogram(x=data['Close'], nbinsx=50, name='Close Price Distribution'))
fig.layout.update(title_text='Histogram of Close Prices')
st.plotly_chart(fig)

# QQ Plot
st.subheader('QQ Plot')
fig, ax = plt.subplots()
stats.probplot(data['Close'].dropna(), dist="norm", plot=ax)
st.pyplot(fig)

# Descriptive Statistics
st.subheader('Descriptive Statistics')
st.write(data.describe())

"""## Dealing with Missing Values"""

# Dealing with Missing Values
if data.isnull().sum().sum() > 0:
    st.subheader('Dealing with Missing Values')
    st.write(data.isnull().sum())

    # Fill missing values
    data.fillna(method='ffill', inplace=True)
    st.write('Missing values handled.')

"""## Check Stationarity with ADF Test"""

# Check Stationarity with ADF Test
st.subheader('Stationarity Check (ADF Test)')
def test_stationarity(series):
    result = adfuller(series)
    st.write(f'ADF Statistic: {result[0]}')
    st.write(f'p-value: {result[1]}')
    st.write(f'Critical Values: {result[4]}')

test_stationarity(data['Close'])

"""## If not stationary, perform transformations"""

# If not stationary, perform transformations
if adfuller(data['Close'])[1] > 0.05:
    st.subheader('Transformations for Stationarity')
    # Example transformation: Log transformation
    data['Log_Close'] = np.log(data['Close'])
    test_stationarity(data['Log_Close'])

"""## Check Seasonality"""

# Check Seasonality
st.subheader('Seasonality Decomposition')
result = seasonal_decompose(data['Close'], model='additive', period=365)
st.write('Seasonal Decomposition')
fig = result.plot()
st.pyplot(fig)

"""## ACF and PACF Plots"""

# ACF and PACF Plots
st.subheader('ACF and PACF Plots')
fig, ax = plt.subplots(2, 1, figsize=(10, 8))
plot_acf(data['Close'].dropna(), ax=ax[0])
plot_pacf(data['Close'].dropna(), ax=ax[1])
st.pyplot(fig)

"""## ARIMA Model"""

# Identify ARIMA or SARIMA Model
st.subheader('ARIMA/SARIMA Model Identification')
st.write('Based on the ACF/PACF plots, we can identify the AR (p), MA (q), and differencing (d) orders.')

# Example ARIMA model fitting
st.write('Fitting ARIMA model (p=5, d=1, q=0)')
arima_model = ARIMA(data['Close'], order=(5, 1, 0))
arima_result = arima_model.fit()
st.write(arima_result.summary())

"""## AIC and BIC Criteria"""

# AIC and BIC Criteria
st.subheader('AIC and BIC Criteria')
st.write(f'AIC: {arima_result.aic}')
st.write(f'BIC: {arima_result.bic}')

"""## Load GAN Models"""

generator = load_model('gan_generator.h5')
discriminator = load_model('gan_discriminator.h5')

def create_dataset(dataset, time_step=1):
    X, Y = [], []
    for i in range(len(dataset)-time_step-1):
        a = dataset[i:(i+time_step), 0]
        X.append(a)
        Y.append(dataset[i + time_step, 0])
    return np.array(X), np.array(Y)

time_series_data = data[['Date', 'Close']]
time_series_data.set_index('Date', inplace=True)
time_series_data = time_series_data.rename(columns={"Close": "Value"})

time_step = 10
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(time_series_data['Value'].values.reshape(-1, 1))

X_train, y_train = create_dataset(scaled_data, time_step)
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)

# Make predictions with GAN
noise = np.random.normal(0, 1, (1, time_step))
generated_prediction = generator.predict(noise)
generated_prediction = generated_prediction.reshape(-1, 1)
generated_prediction = scaler.inverse_transform(generated_prediction)

st.subheader('Forecast data using GAN')
st.write(generated_prediction)

"""## Forecast Data"""

df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

st.subheader('Forecast data')
st.write(forecast.tail())

st.write(f'Forecast plot for {n_years} years')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("Forecast components")
fig2 = m.plot_components(forecast)
st.write(fig2)

"""## Generative AI Generated Report"""

@st.cache_resource
def load_finbert_model():
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
    return tokenizer, model

tokenizer, model = load_finbert_model()

def get_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    sentiment_score = probabilities[0][1].item() - probabilities[0][0].item()  # Positive - Negative
    return sentiment_score

def generate_financial_insight(stock_symbol, metric, value):
    prompts = [
        f"The {metric} of {stock_symbol} is {value}.",
        f"{stock_symbol}'s {metric} has reached {value}.",
        f"Investors are reacting to {stock_symbol}'s {metric} of {value}."
    ]
    sentiments = [get_sentiment(prompt) for prompt in prompts]
    avg_sentiment = sum(sentiments) / len(sentiments)

    if avg_sentiment > 0.5:
        return f"The {metric} of {value} for {stock_symbol} is very positive, indicating strong market confidence."
    elif avg_sentiment > 0.1:
        return f"The {metric} of {value} for {stock_symbol} is somewhat positive, suggesting moderate optimism in the market."
    elif avg_sentiment > -0.1:
        return f"The {metric} of {value} for {stock_symbol} is neutral, implying stable market conditions."
    elif avg_sentiment > -0.5:
        return f"The {metric} of {value} for {stock_symbol} is somewhat negative, hinting at some market concerns."
    else:
        return f"The {metric} of {value} for {stock_symbol} is very negative, indicating significant market apprehension."

def generate_financial_report(data, forecast, stock_symbol):
    # Extract relevant data
    current_price = data['Close'].iloc[-1]
    historical_high = data['Close'].max()
    historical_low = data['Close'].min()
    forecast_end = forecast['ds'].iloc[-1]
    forecast_price = forecast['yhat'].iloc[-1]

    # Calculate metrics
    price_change_1d = (data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2] * 100
    price_change_1m = (data['Close'].iloc[-1] - data['Close'].iloc[-30]) / data['Close'].iloc[-30] * 100 if len(data) >= 30 else None
    price_change_1y = (data['Close'].iloc[-1] - data['Close'].iloc[-252]) / data['Close'].iloc[-252] * 100 if len(data) >= 252 else None

    volatility = np.std(data['Close'].pct_change().dropna()) * np.sqrt(252) * 100

    # Generate AI insights
    price_diff_percentage = (forecast_price - current_price) / current_price * 100
    if price_diff_percentage > 10:
        outlook = "strongly bullish"
        sentiment = "very positive"
        recommendation = "BUY"
    elif price_diff_percentage > 5:
        outlook = "bullish"
        sentiment = "positive"
        recommendation = "BUY"
    elif price_diff_percentage > -5:
        outlook = "neutral"
        sentiment = "cautious"
        recommendation = "HOLD"
    elif price_diff_percentage > -10:
        outlook = "bearish"
        sentiment = "negative"
        recommendation = "HOLD"
    else:
        outlook = "strongly bearish"
        sentiment = "very negative"
        recommendation = "SELL"

    # Generate insights using FinBERT
    current_price_insight = generate_financial_insight(stock_symbol, "current price", f"${current_price:.2f}")
    forecast_price_insight = generate_financial_insight(stock_symbol, "forecasted price", f"${forecast_price:.2f}")
    volatility_insight = generate_financial_insight(stock_symbol, "volatility", f"{volatility:.2f}%")

    # Create the report
    st.subheader(f"AI-Generated Financial Report for {stock_symbol}")

    st.write("### Summary")
    st.write(f"As of {datetime.now().strftime('%Y-%m-%d')}, {stock_symbol} is showing a {outlook} trend based on our AI-powered analysis. The current market sentiment appears to be {sentiment}.")

    st.write("### Key Metrics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Price", f"${current_price:.2f}")
        st.metric("1D Change", f"{price_change_1d:.2f}%")
    with col2:
        st.metric("1M Change", f"{price_change_1m:.2f}%" if price_change_1m else "N/A")
        st.metric("1Y Change", f"{price_change_1y:.2f}%" if price_change_1y else "N/A")
    with col3:
        st.metric("52W High", f"${historical_high:.2f}")
        st.metric("52W Low", f"${historical_low:.2f}")

    st.write("### Market Analysis")
    st.write(current_price_insight)
    st.write(f"The stock has shown a volatility of {volatility:.2f}% over the past year. {volatility_insight}")

    st.write("### AI-Powered Forecast")
    st.write(f"Our AI model predicts that by {forecast_end.strftime('%Y-%m-%d')}, {stock_symbol} could reach ${forecast_price:.2f}.")
    st.write(f"This represents a potential {'increase' if forecast_price > current_price else 'decrease'} of {abs(price_diff_percentage):.2f}% from the current price.")
    st.write(forecast_price_insight)

    st.write("### Risk Factors")
    st.write("- Market volatility and economic uncertainties")
    st.write("- Regulatory changes in the relevant industry")
    st.write("- Competition and technological disruptions")

    st.write("### Recommendation")
    st.write(f"Based on our AI analysis, we maintain a **{recommendation}** recommendation for {stock_symbol}. {recommendation_details[recommendation]}")

    st.write("### Disclaimer")
    st.write("This report is generated by an AI model and should not be considered as financial advice. While we strive for accuracy, the content may contain errors or omissions. Always consult with a qualified financial advisor before making investment decisions.")

# Recommendation details
recommendation_details = {
    "BUY": "The stock shows strong potential for growth, but investors should be aware of the inherent risks and conduct their own due diligence.",
    "HOLD": "Given the current market conditions and our AI analysis, we suggest maintaining current positions. Investors should closely monitor market developments and reassess their position regularly.",
    "SELL": "Our analysis indicates potential downside risks. Investors might consider reducing their exposure, but should evaluate their individual financial situations and risk tolerance before making any decisions."
}

# Call this function in your main script after generating the forecast
generate_financial_report(data, forecast, selected_stock)

!wget -q -O - ipv4.icanhazip.com

! streamlit run app.py & npx localtunnel --port 8501
