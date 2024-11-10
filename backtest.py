import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Define file path to the CSV file inside the 'data' directory
#file_path = os.path.join('data', 'snp500_1800s.csv')
file_path = os.path.join('data', 'snp500_1900s.csv')
#file_path = os.path.join('data', 'snp500_2000s.csv')

# Brief strategy description
strategy_description = """
Strategy Description:
This strategy combines momentum with mean reversion on the S&P 500 index:
1. Buy if the price is above the 21-month simple moving average (SMA) - Absolute Momentum.
2. Buy if there is positive acceleration in 6-month returns (recent returns are better than previous returns) - Relative Momentum.
3. Buy if the price is more than 5% below the 21-month SMA, assuming a reversion to the mean - Mean Reversion.
4. Sell when the price drops below the 21-month SMA.

The goal is to maximize returns by capturing momentum trends while also taking advantage of mean-reversion opportunities.
"""

print(strategy_description)

# Load historical S&P 500 data from CSV file
data = pd.read_csv(file_path)

# Convert 'Date' column to datetime type and set as index
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Record start and end dates for additional context in output
start_date = data.index[0].date()
end_date = data.index[-1].date()

# Ensure that '21_Month_MA' is calculated (if not provided in the CSV)
if '21_Month_MA' not in data.columns or data['21_Month_MA'].eq(0).all():
    data['21_Month_MA'] = data['Value'].rolling(window=21).mean()

# Calculate 6-month percentage returns
data['6M_Return'] = data['Value'].pct_change(periods=6)

# Calculate 6-month percentage returns from six months prior
data['6M_Return_Prior'] = data['6M_Return'].shift(6)

# Calculate the difference in 6-month returns (Acceleration)
data['Return_Acceleration'] = data['6M_Return'] - data['6M_Return_Prior']

# Calculate the percentage difference from the 21-month SMA
data['Pct_Diff_SMA'] = (data['Value'] - data['21_Month_MA']) / data['21_Month_MA']

# Initialize columns for trading signals and positions
data['Signal'] = ''
data['Position'] = 0
data['Portfolio_Value'] = 1.0  # Start with an initial portfolio value of $1
data['Holdings'] = 0.0
data['Cash'] = 1.0
data['Trade'] = ''

position = 0  # 0 means no position, 1 means holding the asset
entry_price = 0.0
buy_count = 0  # Counter for buys
sell_count = 0  # Counter for sells

print("Starting backtest...")

for i in range(len(data)):
    date = data.index[i]
    price = data['Value'][i]
    sma = data['21_Month_MA'][i]
    acceleration = data['Return_Acceleration'][i]
    pct_diff_sma = data['Pct_Diff_SMA'][i]

    # Check for buy signal
    buy_signal = False
    if price > sma:
        # Absolute momentum condition
        buy_signal = True
        reason = "Price above 21-month SMA (Absolute Momentum)"
    elif acceleration > 0:
        # Relative momentum condition
        buy_signal = True
        reason = "Positive return acceleration (Relative Momentum)"
    elif pct_diff_sma < -0.05:
        # Mean reversion condition
        buy_signal = True
        reason = "Price more than 5% below 21-month SMA (Mean Reversion)"

    # Check for sell signal
    sell_signal = False
    if price < sma:
        sell_signal = True
        reason = "Price below 21-month SMA (Sell Signal)"

    # Trading logic
    if position == 0 and buy_signal:
        # Entering a new position
        position = 1
        entry_price = price
        data.at[date, 'Signal'] = 'Buy'
        data.at[date, 'Trade'] = f'Bought at {price:.2f}'
        data.at[date, 'Position'] = position
        data.at[date, 'Holdings'] = data['Cash'][i-1] * (price / price)
        data.at[date, 'Cash'] = 0.0
        data.at[date, 'Portfolio_Value'] = data['Holdings'][i]
        buy_count += 1
        print(f"{date.date()}: BUY signal triggered - {reason}. Entry price: {price:.2f}")
    elif position == 1 and sell_signal:
        # Exiting the position
        position = 0
        exit_price = price
        data.at[date, 'Signal'] = 'Sell'
        data.at[date, 'Trade'] = f'Sold at {price:.2f}'
        data.at[date, 'Position'] = position
        data.at[date, 'Cash'] = data['Holdings'][i-1] * (price / entry_price)
        data.at[date, 'Holdings'] = 0.0
        data.at[date, 'Portfolio_Value'] = data['Cash'][i]
        sell_count += 1
        print(f"{date.date()}: SELL signal triggered - {reason}. Exit price: {price:.2f}")
    else:
        # Hold position or stay in cash
        data.at[date, 'Position'] = position
        if position == 1:
            data.at[date, 'Holdings'] = data['Holdings'][i-1] * (price / data['Value'][i-1])
            data.at[date, 'Cash'] = 0.0
            data.at[date, 'Portfolio_Value'] = data['Holdings'][i]
            data.at[date, 'Trade'] = 'Hold'
            print(f"{date.date()}: Holding position. Current price: {price:.2f}")
        else:
            data.at[date, 'Cash'] = data['Cash'][i-1]
            data.at[date, 'Holdings'] = 0.0
            data.at[date, 'Portfolio_Value'] = data['Cash'][i]
            data.at[date, 'Trade'] = 'No Position'
            print(f"{date.date()}: No position. Current price: {price:.2f}")

# Calculate cumulative returns
data['Strategy_Returns'] = data['Portfolio_Value'].pct_change()
data['Cumulative_Strategy_Returns'] = (1 + data['Strategy_Returns']).cumprod()

# Buy-and-hold strategy returns
data['Buy_and_Hold_Returns'] = data['Value'] / data['Value'][0]
data['Cumulative_BH_Returns'] = data['Buy_and_Hold_Returns']

# Plot cumulative returns
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Cumulative_Strategy_Returns'], label='Strategy Returns')
plt.plot(data.index, data['Cumulative_BH_Returns'], label='Buy and Hold Returns')
plt.title('Cumulative Returns Comparison')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns')
plt.legend()
plt.grid(True)
plt.show()

# Calculate Buy-and-Hold performance
starting_price_bh = data['Value'].iloc[0]  # Entry price for Buy and Hold
ending_price_bh = data['Value'].iloc[-1]   # Exit price for Buy and Hold
buy_and_hold_ending_value = data['Cumulative_BH_Returns'].iloc[-1]

# Calculate Strategy performance
starting_portfolio_value = 1.0  # Initial portfolio value for the strategy
ending_portfolio_value = data['Portfolio_Value'].iloc[-1]

# Output detailed performance summary
print("\nPerformance Summary:")
print(f"  Start Date: {start_date}")
print(f"  End Date: {end_date}")

# Buy-and-Hold Performance
print("\nBuy and Hold Performance:")
print(f"  Entry Price: ${starting_price_bh:.2f}")
print(f"  Exit Price: ${ending_price_bh:.2f}")
print(f"  Starting Portfolio Value: ${starting_portfolio_value:.2f}")
print(f"  Ending Portfolio Value: ${buy_and_hold_ending_value:.2f}")
print(f"  Total Buy and Hold Return: {(buy_and_hold_ending_value - starting_portfolio_value) / starting_portfolio_value:.2%}")

# Strategy Performance
print("\nStrategy Performance:")
print(f"  Starting Portfolio Value: ${starting_portfolio_value:.2f}")
print(f"  Ending Portfolio Value (Strategy): ${ending_portfolio_value:.2f}")
print(f"  Total Strategy Return: {(ending_portfolio_value - starting_portfolio_value) / starting_portfolio_value:.2%}")
print(f"  Total Buys Executed: {buy_count}")
print(f"  Total Sells Executed: {sell_count}")

# Calculate and display maximum drawdown for additional context
def calculate_max_drawdown(cumulative_returns):
    roll_max = cumulative_returns.cummax()
    drawdown = cumulative_returns / roll_max - 1.0
    max_drawdown = drawdown.min()
    return max_drawdown

strategy_max_drawdown = calculate_max_drawdown(data['Cumulative_Strategy_Returns'])
bh_max_drawdown = calculate_max_drawdown(data['Cumulative_BH_Returns'])

print("\nDrawdown Summary:")
print(f"  Strategy Maximum Drawdown: {strategy_max_drawdown:.2%}")
print(f"  Buy and Hold Maximum Drawdown: {bh_max_drawdown:.2%}")
