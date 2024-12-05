import pandas as pd
import matplotlib.pyplot as plt

# Initialize the global counter for open positions and closed trades
total_positions_open = 0
total_trades_closed = 0

# Step 1: Load the CSV file into a DataFrame, skipping the first 5 rows and last 7 rows
date_format = '%m/%d/%y, %I:%M %p'  # Date format based on your CSV structure

# Read the entire CSV file first, skipping the first 5 rows (header) and manually slicing off the last 7 rows
df = pd.read_csv('backtesting_data/StrategyReports_SPX_111924333.csv', 
                 sep=';', 
                 skiprows=5,  # Skip the first 5 rows
                 parse_dates=['Date/Time'], 
                 dayfirst=False, 
                 date_format=lambda x: pd.to_datetime(x, format=date_format))

# Remove the last 7 rows
df = df.iloc[:-7]

# Step 2: Process the P/L data
def clean_pl(value):
    # Remove dollar sign, commas, and handle parentheses for negative values
    if pd.isna(value) or value == '':
        return 0.0  # Treat empty or NaN as break-even (0.0)
    value = value.replace('$', '').replace(',', '').replace('(', '-').replace(')', '').strip()
    return float(value)

# Apply P/L cleaning
df['P/L'] = df['P/L'].apply(clean_pl)

# Step 3: Count open positions based on the 'Position' column
# Assuming that non-zero values in 'Position' indicate an open position
total_positions_open = (df['Position'] != 0.0).sum()

# Step 4: Calculate win rate
# Assuming a trade is a win if 'P/L' > 0
total_trades = len(df[df['P/L'] != 0.0])  # Exclude break-even trades
winning_trades = len(df[df['P/L'] > 0.0])
win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0

# Determine the color for win rate based on its value
win_rate_color = 'green' if win_rate > 50 else 'red'

# Step 5: Count successfully closed trades
# A trade is considered successfully closed if 'Position' changes from non-zero to zero
# We look at shifts in the 'Position' column to detect these changes
df['Position_shifted'] = df['Position'].shift(1, fill_value=0)  # Shift the 'Position' column down by 1
successful_trades_closed = len(df[(df['Position_shifted'] != 0) & (df['Position'] == 0)])

# Step 6: Extract the necessary data for plotting
pl_data = df['P/L'].tolist()
date_objects = df['Date/Time'].tolist()

# Step 7: Plot the P/L Data
plt.figure(figsize=(12, 6))
plt.plot(date_objects, pl_data, marker='o', linestyle='-', color='b', label='P/L')
plt.title('P/L Over Time')
plt.xlabel('Date/Time')
plt.ylabel('Profit/Loss ($)')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.grid(True)

# Add labels for open positions (black), win rate (dynamic color), and successfully closed trades (blue)
plt.text(0.5, 0.95, f"Open Positions: {total_positions_open}", 
         transform=plt.gca().transAxes, fontsize=12, color='black', 
         verticalalignment='top', horizontalalignment='center')

plt.text(0.5, 0.90, f"Win Rate: {win_rate:.2f}%", 
         transform=plt.gca().transAxes, fontsize=12, color=win_rate_color, 
         verticalalignment='top', horizontalalignment='center')

plt.text(0.5, 0.85, f"Closed Trades: {successful_trades_closed}", 
         transform=plt.gca().transAxes, fontsize=12, color='blue', 
         verticalalignment='top', horizontalalignment='center')

plt.tight_layout()  # Adjust layout
plt.legend()
plt.show()
