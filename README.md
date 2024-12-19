# Stock-Prediction-System-using-ARIMA-and-GANs

This project is a web application built using Streamlit that allows users to forecast stock prices based on historical data. It uses multiple techniques including **Generative Adversarial Networks (GANs)**, **ARIMA/SARIMA models**, and **Prophet** for stock price prediction. The app also performs Exploratory Data Analysis (EDA), checks for stationarity, handles missing values, and more.

## Features

- **Data Collection**: Fetches stock data using the `yfinance` library.
- **Exploratory Data Analysis (EDA)**: Provides a variety of visualizations (line plots, scatter plots, histograms, QQ plots) and statistics for the selected stock.
- **Stationarity Check**: Uses the Augmented Dickey-Fuller (ADF) test to check if the stock price data is stationary.
- **ARIMA/SARIMA Model**: Identifies and fits ARIMA/SARIMA models for time-series forecasting.
- **GAN Model**: Uses a GAN-based model to generate stock price predictions.
- **Prophet Model**: Uses Facebook's Prophet model to generate long-term stock price forecasts.
- **Sentiment Analysis**: Uses the **FinBERT** model to perform sentiment analysis on financial text.

## Libraries Used

- `streamlit`: For building the web app.
- `yfinance`: For downloading stock data.
- `plotly`: For interactive visualizations.
- `tensorflow`: For building and training the GAN model.
- `prophet`: For time-series forecasting.
- `sklearn`: For data preprocessing and model evaluation.
- `statsmodels`: For ARIMA modeling and statistical analysis.
- `torch` and `transformers`: For sentiment analysis using the FinBERT model.

## Installation

To run this app locally, follow the steps below.

### Prerequisites

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/stock-forecast-app.git
   cd stock-forecast-app


2. Install the required libraries:

`pip install -r requirements.txt`

Alternatively, install the individual libraries:

`pip install streamlit yfinance plotly tensorflow prophet scikit-learn torch transformers statsmodels`

Running the App
To start the Streamlit app, run:
`streamlit run app.py`

## Usage

1. **Select a stock**: Choose the stock you want to analyze from the dropdown menu. Available stocks include `GOOG`, `AAPL`, `MSFT`, `GME`, and `TSLA`.
2. **Select prediction duration**: Use the slider to choose the number of years for stock price prediction (1-4 years).
3. **View Raw Data**: Check the raw stock data including open, close, high, and low prices.
4. **Visualization**: View various visualizations such as:
   - Stock price over time
   - Scatter plot of open vs close price
   - Histogram of close prices
   - QQ plot for normality check
5. **Stationarity Check**: The app checks if the stock data is stationary and performs transformations if necessary.
6. **Model Predictions**:
   - **ARIMA/SARIMA**: The app will fit an ARIMA model for forecasting.
   - **GAN Forecast**: Generate predictions using the GAN model trained on historical data.
   - **Prophet Forecast**: Generate long-term forecasts using the Prophet model.
7. **Sentiment Analysis**: Get sentiment analysis results based on financial text using the FinBERT model.

## Example Output

- **Stock Price Predictions**: Visualizes forecasted stock prices using different models.
- **ARIMA/SARIMA Summary**: Displays the ARIMA model summary including AIC/BIC criteria.
- **GAN Prediction**: Displays generated stock price prediction using the GAN model.
- **Prophet Forecast**: Shows the long-term forecast with interactive plots and components.

## Model Files

- **GAN Generator**: A neural network-based generator model used to predict stock prices.
- **GAN Discriminator**: A model used to distinguish between real and fake stock price data.
- **Prophet Model**: Uses the Prophet library to generate long-term stock price forecasts.


