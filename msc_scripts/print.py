import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load the CSV file
df = pd.read_csv('snp500_with_moving_average.csv', parse_dates=['Date'])

# Sort the DataFrame by date in ascending order
df = df.sort_values('Date').reset_index(drop=True)

# Create the plot
plt.figure(figsize=(12, 6))
plt.plot(df['Date'], df['Value'], label='Value')
plt.plot(df['Date'], df['21_Month_MA'], label='21-Month Moving Average', linestyle='--')

# Set plot title and labels
plt.title('S&P 500 Value and 21-Month Moving Average')
plt.xlabel('Date')
plt.ylabel('Value')

# Set the date format on the x-axis
plt.gca().xaxis.set_major_locator(mdates.YearLocator(10))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
plt.gcf().autofmt_xdate()  # Rotation

# Add a legend
plt.legend()

# Add a grid
plt.grid(True)

# Show the plot
plt.show()

