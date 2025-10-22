"""
Simple Backtesting Engine -- Moving Average Crossover Strategy
DescriptionL
Simulates a simple trading strategy on historical stock data
using Python's yfinance, pandas, and imported matplotlib.pyplot libraries 
"""

#-----1. IMPORTED LIBRARIES -----
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

#-----2. DOWNLOAD HISTORICAL DATA -----
data = yf.download("AAPL", start="2020-01-01", end="2023-01-01", auto_adjust=False)

# Keep only the Close price for simplicity
data = data[['Close']]

#-----3. DEFINE STRATEGY PARAMETERS -----
SHORT_WINDOW = 20
LONG_WINDOW = 50
INITIAL_BALANCE = 10000

#-----4. CALCULATE MOVING AVERAGES -----
data['Short_MA'] = data['Close'].rolling(window=SHORT_WINDOW).mean()
data['Long_MA'] = data['Close'].rolling(window=LONG_WINDOW).mean()

# Remove NaN rows from moving averages
data = data.dropna()

#-----5. GENERATE TRADING SIGNALS -----
# Signal = 1 -> Buy (Short MA above Long MA)
# Signal = -1 -> Sell (Short MA below Long MA)
data['Signal'] = 0
data.loc[data['Short_MA'] > data['Long_MA'], 'Signal'] = 1
data.loc[data['Short_MA'] < data['Long_MA'], 'Signal'] = -1

#Reset index to ensure clean iteration
data = data.reset_index(drop=True)

#-----6. BACKTEST SIMULATION -----
balance = INITIAL_BALANCE
position = 0    # Number of shares currently held
portfolio_values = []

for i in range(len(data)):
    price = data['Close'].iloc[i].item()
    signal = int(data['Signal'].iloc[i])
    
    #BUY: when signal says 1 and we hold no shares
    if signal == 1 and position == 0:
        position = int(balance // price)  # buy as many shares as possible 
        balance = 0
    
    #SELL: when signal says -1 and we hold shares
    elif signal == -1 and position > 0:
        balance = position * price   # sell all shares
        position = 0
        
    # Track total portfolio value (cash + market value of shares)
    total_value = balance + position * price
    portfolio_values.append(total_value)
    
data['Portfolio'] = portfolio_values

#-----7. RESULTS -----
# Final Return & Profit %
final_value = data['Portfolio'].iloc[-1]
profit = final_value - INITIAL_BALANCE
percent_return = profit / INITIAL_BALANCE

print("FINAL RETURN")
print(f"Initial Balance: ${INITIAL_BALANCE:,.2f}")
print(f"Final Balance: ${final_value:,.2f}")
print(f"Net Profit: ${profit:,.2f} ({percent_return * 100:.2f}%)")

#-----8. VISUALIZATION -----
plt.figure(figsize=(12,6))
plt.plot(data['Close'], label='Stock Price', alpha=0.7)
plt.plot(data['Short_MA'], label=f'Short {SHORT_WINDOW}-Day MA')
plt.plot(data['Long_MA'], label=f'Long {LONG_WINDOW}-Day MA')
plt.title("Moving Average Crossover Strategy - AAPL")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(12,5))
plt.plot(data['Portfolio'], label='Portfolio Value')
plt.title("Portfolio Value Over Time")
plt.xlabel("Date")
plt.ylabel("Portfolio ($)")
plt.legend()
plt.grid(True)
plt.show()
