import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Task 1: Data Acquisition and Loading ---
print("Task 1: Loading Data...")
# Replace 'your_weather_data.csv' with your actual file path
file_path = 'your_weather_data.csv'
try:
    df = pd.read_csv(file_path)
    print("Data loaded successfully.")
    print("\nDataFrame Head:")
    print(df.head())
    print("\nDataFrame Info:")
    df.info()
    print("\nDataFrame Describe:")
    print(df.describe())
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    exit()

# --- Task 2: Data Cleaning and Processing ---
print("\n--- Task 2: Cleaning and Processing Data ---")

# **Step 2.1: Convert Date Column**
# Replace 'Date_Column_Name' with the actual name of your date column
DATE_COLUMN = 'Date_Column_Name'
df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], errors='coerce')
df.set_index(DATE_COLUMN, inplace=True)

# **Step 2.2: Define Relevant Columns**
# Replace these placeholders with your actual column names for Temperature, Rainfall, and Humidity
TEMP_COL = 'Temperature_C'
RAIN_COL = 'Rainfall_mm'
HUMIDITY_COL = 'Humidity_perc'

# Filter for relevant columns
relevant_cols = [TEMP_COL, RAIN_COL, HUMIDITY_COL]
df = df[relevant_cols].copy()

# **Step 2.3: Handle Missing Values** [cite: 21]
# Decide on your strategy:
# Option 1: Drop rows with any missing values
# df.dropna(inplace=True)

# Option 2: Fill missing temperature/humidity with the mean or median (Example using median)
# df[TEMP_COL].fillna(df[TEMP_COL].median(), inplace=True)
# df[HUMIDITY_COL].fillna(df[HUMIDITY_COL].median(), inplace=True)

# Option 3: Fill missing rainfall (often 0 for no rain)
# df[RAIN_COL].fillna(0, inplace=True)

# For this example, we'll drop rows with NaNs for simplicity, but choose the best for your data.
df.dropna(inplace=True)
print(f"Cleaned data shape: {df.shape}")

# --- Task 3: Statistical Analysis with NumPy ---
print("\n--- Task 3: Statistical Analysis ---")

# **Daily Statistics** (Already available in the DataFrame after cleaning)
print(f"Daily Mean Temperature: {np.mean(df[TEMP_COL]):.2f}")
print(f"Daily Max Humidity: {np.max(df[HUMIDITY_COL]):.2f}")

# **Monthly Statistics (Example: Mean Temperature)** [cite: 25, 26]
monthly_mean_temp = df[TEMP_COL].resample('M').mean()
print("\nMonthly Mean Temperature (first 5 months):")
print(monthly_mean_temp.head())

# **Yearly Statistics (Example: Total Rainfall)**
yearly_total_rain = df[RAIN_COL].resample('Y').sum()
print("\nYearly Total Rainfall:")
print(yearly_total_rain)

# --- Task 5: Grouping and Aggregation (Monthly Total Rainfall) ---
print("\n--- Task 5: Grouping and Aggregation ---")

# Using resampling for monthly aggregation 
monthly_rainfall_total = df[RAIN_COL].resample('M').sum()
print("\nMonthly Total Rainfall aggregated using resample (first 5 months):")
print(monthly_rainfall_total.head())

# --- Task 4: Visualization with Matplotlib ---
print("\n--- Task 4: Creating Visualizations ---")

# **Plot 1: Line Chart for Daily Temperature Trends** [cite: 29]
plt.figure(figsize=(12, 6))
plt.plot(df.index, df[TEMP_COL], label='Daily Temperature', color='coral')
plt.title('Daily Temperature Trend')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.grid(True)
# plt.savefig('daily_temp_trend.png') # Task 6: Save plot
# plt.show()

# **Plot 2: Bar Chart for Monthly Rainfall Totals** [cite: 30]
plt.figure(figsize=(10, 5))
monthly_rainfall_total.plot(kind='bar', color='skyblue')
plt.title('Monthly Rainfall Totals')
plt.xlabel('Month')
plt.ylabel('Total Rainfall (mm)')
plt.xticks(rotation=45)
plt.tight_layout()
# plt.savefig('monthly_rainfall_bar.png') # Task 6: Save plot
# plt.show()

# **Plot 3: Scatter Plot for Humidity vs. Temperature** [cite: 31]
plt.figure(figsize=(8, 6))
plt.scatter(df[HUMIDITY_COL], df[TEMP_COL], alpha=0.6, color='darkgreen')
plt.title('Humidity vs. Temperature')
plt.xlabel('Humidity (%)')
plt.ylabel('Temperature (°C)')
# plt.savefig('humidity_temp_scatter.png') # Task 6: Save plot
# plt.show()

# **Plot 4: Combine at least two plots in a single figure (Subplots)** [cite: 32]
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(14, 10))
fig.suptitle('Combined Weather Trends', fontsize=16)

# Subplot 1: Daily Temperature
axes[0].plot(df.index, df[TEMP_COL], label='Temperature', color='red')
axes[0].set_title('Daily Temperature')
axes[0].set_ylabel('Temperature (°C)')
axes[0].grid(True)

# Subplot 2: Daily Humidity
axes[1].plot(df.index, df[HUMIDITY_COL], label='Humidity', color='blue')
axes[1].set_title('Daily Humidity')
axes[1].set_xlabel('Date')
axes[1].set_ylabel('Humidity (%)')
axes[1].grid(True)

plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Adjust layout to prevent title overlap
# plt.savefig('combined_subplots.png') # Task 6: Save plot
plt.show() # Uncomment to display all plots at the end

# --- Task 6: Export and Storytelling ---
print("\n--- Task 6: Exporting Data ---")

# **Export cleaned data to a new CSV file** [cite: 37]
cleaned_file_path = 'cleaned_weather_data.csv'
df.to_csv(cleaned_file_path)
print(f"Cleaned data exported to {cleaned_file_path}")

# **Note on Report:** The report (Task 6, part 2) must be written separately (Markdown or .txt)
# and summarize the trends and anomalies you observe in the data and plots[cite: 39].

# Final Note: Remember to save all plots using plt.savefig() and include them in your submission[cite: 38].
