import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# Read the CSV file
df = pd.read_csv('snp500_with_moving_average.csv', parse_dates=['Date'])

# Ensure the DataFrame is sorted by date in ascending order
df = df.sort_values('Date').reset_index(drop=True)

# Clean the 'Value' column if necessary (remove commas and convert to float)
df['Value'] = df['Value'].astype(str).str.replace(',', '').astype(float)

# Simulate dollar-cost averaging: Invest $100 every month
df['Investment'] = 100  # Monthly investment amount
df['Shares_Purchased'] = df['Investment'] / df['Value']
df['Total_Shares'] = df['Shares_Purchased'].cumsum()
df['Total_Invested'] = df['Investment'].cumsum()
df['Portfolio_Value'] = df['Total_Shares'] * df['Value']

# Calculate the overall performance
total_invested = df['Total_Invested'].iloc[-1]
final_portfolio_value = df['Portfolio_Value'].iloc[-1]
total_gain = final_portfolio_value - total_invested

# Calculate the CAGR (Compound Annual Growth Rate)
start_date = df['Date'].iloc[0]
end_date = df['Date'].iloc[-1]
num_years = (end_date - start_date).days / 365.25  # Account for leap years
cagr = (final_portfolio_value / total_invested) ** (1 / num_years) - 1

# Print the results
print(f"Total Invested: ${total_invested:,.2f}")
print(f"Final Portfolio Value: ${final_portfolio_value:,.2f}")
print(f"Total Gain: ${total_gain:,.2f}")
print(f"Average Annual Rate of Return (CAGR): {cagr * 100:.2f}% over {num_years:.2f} years")

# Optional: Plot the portfolio value over time
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Portfolio_Value'], label='Portfolio Value')
plt.plot(df['Date'], df['Total_Invested'], label='Total Invested', linestyle='--')
plt.title('Portfolio Value Over Time')
plt.xlabel('Date')
plt.ylabel('Value ($)')
plt.legend()
plt.grid(True)
plt.gca().xaxis.set_major_locator(mdates.YearLocator(20))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gcf().autofmt_xdate()
plt.tight_layout()
plt.show()

