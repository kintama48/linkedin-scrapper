# from event_register.linkedin import LinkedInScraper
# import xlsxwriter
# from dotenv import load_dotenv
# import os

# # Load environment variables from .env file
# load_dotenv()

# # Get environment variables
# email = os.getenv('EMAIL')
# password = os.getenv('PASSWORD')
# search_query = os.getenv('SEARCH_QUERY')
# pages = int(os.getenv('PAGES'))

# # Example usage:
# if __name__ == "__main__":
#     scraper = LinkedInScraper(email, password, search_query, pages)
#     scraper.run()
#     print("Data compiled successfully")
import pandas as pd
import matplotlib.pyplot as plt

# Load data from the CSV file
file_path = "results.csv"
df = pd.read_csv(file_path)

# Convert the timestamp to datetime
df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='ms')

# Convert the timeStamp to CST (Central Standard Time)
df['timeStamp'] = df['timeStamp'].dt.tz_localize('UTC').dt.tz_convert('America/Chicago')

# Add a new column to indicate whether the request was successful or not
df['order_status'] = df['responseCode'].apply(lambda x: 'Success' if x == 200 else 'Failure')

# Group by exact time (minutes) and order status
df['time'] = df['timeStamp'].dt.strftime('%H:%M')  # Extracting only hours and minutes
grouped = df.groupby(['time', 'order_status']).size().unstack(fill_value=0)

# Plot all orders
plt.figure(figsize=(12, 8))
ax1 = plt.subplot(211)
grouped.plot(kind='bar', stacked=True, ax=ax1, color={'Success': 'blue', 'Failure': 'red'})

# Customize the plot
plt.title('Number of Orders Over Time')
plt.xlabel('Time (HH:MM)')
plt.ylabel('Number of Orders')
plt.legend(title='Order Status')
plt.xticks(rotation=45)

# Plot failures only
ax2 = plt.subplot(212)
failures = grouped['Failure'] if 'Failure' in grouped.columns else []
failures.plot(kind='bar', color='red', ax=ax2)

# Customize the failures plot
plt.title('Number of Failures Over Time')
plt.xlabel('Time (HH:MM)')
plt.ylabel('Number of Failures')
plt.xticks(rotation=45)

# Calculate totals
total_orders = df.shape[0]
total_success = df[df['order_status'] == 'Success'].shape[0]
total_failures = df[df['order_status'] == 'Failure'].shape[0]
error_rate = total_failures / total_orders * 100 if total_orders > 0 else 0

# Add a table to display total orders, successes, failures with more spacing
table_data = [
    ['Total Orders', total_orders],
    ['Total Successes', total_success],
    ['Total Failures', total_failures],
    ['Error Rate (%)', f'{error_rate:.2f}%']
]
plt.table(cellText=table_data, colLabels=['Metric', 'Value'], cellLoc='center', loc='bottom', bbox=[0.25, -0.4, 0.5, 0.2], cellColours=[['white', 'white']] * len(table_data), colColours=['lightgrey', 'lightgrey'])

# Adjust layout
plt.tight_layout()

# Save the plot to a file
plt.savefig('orders_with_failures_spaced_table.png')

