import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# Define the tickers
tickers = ['TSLA', 'META']

# Define the date range
end_date = '2024-12-28'
start_date = '2024-01-01'

# Get the data
data = yf.download(tickers, start=start_date, end=end_date)

# Calculate the YTD returns
data_returns = data['Close'].pct_change().fillna(0).add(1).cumprod()

# Plot the data
plt.figure(figsize=(12,6))
for ticker in tickers:
    plt.plot(data_returns.index, data_returns[ticker], label=ticker)
plt.title('YTD Stock Price Gains for TSLA and META')
plt.xlabel('Date')
plt.ylabel('Price Gain')
plt.legend()
plt.grid(True)
plt.savefig('stock_gains.png')
