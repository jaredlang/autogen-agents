import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Calculate the start of the year
current_date = datetime(2024, 12, 29)
start_of_year = datetime(current_date.year, 1, 1)

# Format dates for yfinance
start_date = start_of_year.strftime('%Y-%m-%d')
end_date = current_date.strftime('%Y-%m-%d')

# Fetch stock data
tsla = yf.Ticker("TSLA")
meta = yf.Ticker("META")

tsla_data = tsla.history(start=start_date, end=end_date)
meta_data = meta.history(start=start_date, end=end_date)

# Calculate percentage gains
tsla_gains = (tsla_data['Close'] / tsla_data['Close'].iloc[0] - 1) * 100
meta_gains = (meta_data['Close'] / meta_data['Close'].iloc[0] - 1) * 100

# Create the plot
plt.figure(figsize=(12, 6))
plt.plot(tsla_gains.index, tsla_gains, label='TSLA')
plt.plot(meta_gains.index, meta_gains, label='META')

plt.title('YTD Stock Price Gains: TSLA vs META (2024)')
plt.xlabel('Date')
plt.ylabel('Percentage Gain (%)')
plt.legend()
plt.grid(True)

# Save the plot
plt.savefig('stock_gains.png')
print("Plot saved as 'stock_gains.png'")