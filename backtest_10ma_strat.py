import pandas as pd

# Read the CSV file into a DataFrame from the 'data' directory
# df = pd.read_csv('data/snp500_1800s.csv', parse_dates=['Date'])
# df = pd.read_csv('data/snp500_1900s.csv', parse_dates=['Date'])
df = pd.read_csv('data/snp500_2000s.csv', parse_dates=['Date'])

# Initialize variables
initial_capital = 100000
capital = initial_capital
position = 'invested'  # 'invested' or 'cash'
portfolio_value = capital
units = 0  # Number of units of the asset
verbose_output = []

# Get the initial Value to compute the initial units
initial_value = df.iloc[0]['Value']
units = capital / initial_value
capital = 0  # Since we've invested all capital
portfolio_value = units * initial_value

verbose_output.append(f"Starting backtest with initial capital: ${initial_capital:.2f}")
verbose_output.append(f"Initial investment: Bought {units:.4f} units at ${initial_value:.2f} each.\n")

# Loop over each row in the DataFrame starting from the first row
for index, row in df.iterrows():
    date = row['Date'].strftime('%Y-%m-%d')
    value = row['Value']
    ma = row['21_Month_MA']

    # Skip rows where 21_Month_MA is 0 (cannot compute MA)
    if ma == 0:
        # Update portfolio value if invested
        if position == 'invested':
            portfolio_value = units * value
        verbose_output.append(f"{date} | MA unavailable | Holding position | Portfolio Value: ${portfolio_value:.2f}")
        continue

    action = 'Hold'

    if position == 'invested':
        if value < ma:
            # Sell all units
            capital = units * value
            units = 0
            position = 'cash'
            portfolio_value = capital
            action = 'Sell'
            verbose_output.append(f"{date} | Value: ${value:.2f} | MA: ${ma:.2f} | Action: SELL at ${value:.2f} | Portfolio Value: ${portfolio_value:.2f}")
        else:
            # Hold position
            portfolio_value = units * value
            verbose_output.append(f"{date} | Value: ${value:.2f} | MA: ${ma:.2f} | Action: HOLD | Portfolio Value: ${portfolio_value:.2f}")
    elif position == 'cash':
        if value > ma:
            # Buy units with all capital
            units = capital / value
            capital = 0
            position = 'invested'
            portfolio_value = units * value
            action = 'Buy'
            verbose_output.append(f"{date} | Value: ${value:.2f} | MA: ${ma:.2f} | Action: BUY at ${value:.2f} | Portfolio Value: ${portfolio_value:.2f}")
        else:
            # Hold cash
            portfolio_value = capital
            verbose_output.append(f"{date} | Value: ${value:.2f} | MA: ${ma:.2f} | Action: HOLD CASH | Portfolio Value: ${portfolio_value:.2f}")

# Output the verbose logs
for log in verbose_output:
    print(log)

# Final portfolio performance
print("\nBacktest completed.")
print(f"Final Portfolio Value: ${portfolio_value:.2f}")
total_return = ((portfolio_value - initial_capital) / initial_capital) * 100
print(f"Total Return: {total_return:.2f}%")

