import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_data(filename):
    # Define the path to the data folder
    data_folder = 'data/'
    
    # Construct the full file path
    file_path = data_folder + filename

    # Load the CSV file
    df = pd.read_csv(file_path, parse_dates=['Date'])

    # Sort the DataFrame by date in ascending order
    df = df.sort_values('Date').reset_index(drop=True)

    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Value'], label='Value')
    plt.plot(df['Date'], df['21_Month_MA'], label='21-Month Moving Average', linestyle='--')

    # Set plot title and labels
    plt.title(f'S&P 500 Value and 21-Month Moving Average - {filename}')
    plt.xlabel('Date')
    plt.ylabel('Value')

    # Set the date format on the x-axis
    plt.gca().xaxis.set_major_locator(mdates.YearLocator(5))  # Changed from 10 to 5 years
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gcf().autofmt_xdate()  # Rotation

    # Add a legend
    plt.legend()

    # Add a grid
    plt.grid(True)

    # Show the plot
    plt.show()

# File names
files = ['snp500_1800s.csv', 'snp500_1900s.csv', 'snp500_2000s.csv']

# Plot each file
for file in files:
    plot_data(file)

