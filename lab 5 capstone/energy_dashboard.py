import pandas as pd
import numpy as np
import os
from pathlib import Path
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)  # Create output directory if it doesn't exist

# --- TASK 1: Data Ingestion and Validation ---
def task_1_ingest_data():
    """
    Automatically reads multiple CSV files from the /data/ directory,
    combines them, and cleans the resulting DataFrame.
    """
    print("--- Task 1: Data Ingestion and Validation ---")

    # Placeholder for the final combined DataFrame
    all_data = []

    # 1. Loop through /data/ directory and detect .csv files
    csv_files = list(DATA_DIR.glob("building_A_jan.csv"))

    if not csv_files:
        print(f"ERROR: No CSV files found in {DATA_DIR}. Please add sample data.")
        return pd.DataFrame()

    for file_path in csv_files:
        building_name = file_path.stem.split('_')[0].capitalize()
        month_name = file_path.stem.split('_')[-1].capitalize()

        try:
            # 2. Use pandas.read_csv()
            df = pd.read_csv(
                file_path,
                # 3. Handle corrupt data (e.g., skips bad lines)
                on_bad_lines='skip',
                header=0
            )

            # Standardize column names (if possible)
            # If file has more than 2 columns, try to pick first two relevant columns
            if len(df.columns) >= 2:
                df = df.iloc[:, :2]
                df.columns = ['Timestamp', 'kWh']
            else:
                df.columns = ['Timestamp', 'kWh']

            # Convert Timestamp to datetime objects for time-series analysis
            df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')

            # Drop rows where timestamp conversion failed
            df.dropna(subset=['Timestamp'], inplace=True)

            # Ensure kWh is numeric
            df['kWh'] = pd.to_numeric(df['kWh'], errors='coerce')

            # Drop rows with invalid kWh
            df.dropna(subset=['kWh'], inplace=True)

            # Add metadata (e.g., building name, month)
            df['Building'] = building_name
            df['Month'] = month_name

            all_data.append(df)
            print(f"Successfully loaded: {file_path.name}")

        except FileNotFoundError:
            print(f"LOG: Missing file detected: {file_path.name}")
        except Exception as e:
            print(f"LOG: Error processing {file_path.name}: {e}")

    # Combine all data into a single merged DataFrame
    if all_data:
        df_combined = pd.concat(all_data, ignore_index=True)
        # Final cleanup: Ensure 'kWh' is numeric and set index for resampling
        df_combined['kWh'] = pd.to_numeric(df_combined['kWh'], errors='coerce')
        df_combined.dropna(subset=['kWh', 'Timestamp'], inplace=True)
        df_combined.set_index('Timestamp', inplace=True)
        print("\nData Ingestion Complete. Combined DataFrame created.")
        return df_combined
    else:
        print("\nData Ingestion Failed: No data to combine.")
        return pd.DataFrame()


# --- TASK 2: Core Aggregation Logic ---
def calculate_daily_totals(df):
    """Calculates daily total consumption for all buildings."""
    # Use pd.Grouper on the Timestamp level for robust resampling
    daily_totals = (
        df.groupby(['Building', pd.Grouper(level='Timestamp', freq='D')])['kWh']
        .sum()
        .reset_index()
    )
    daily_totals.rename(columns={'kWh': 'Daily_kWh_Total'}, inplace=True)
    return daily_totals


def calculate_weekly_aggregates(df):
    """Calculates weekly total consumption for all buildings."""
    weekly_aggregates = (
        df.groupby(['Building', pd.Grouper(level='Timestamp', freq='W')])['kWh']
        .sum()
        .reset_index()
    )
    weekly_aggregates.rename(columns={'kWh': 'Weekly_kWh_Total'}, inplace=True)
    return weekly_aggregates


def building_wise_summary(df):
    """Calculates summary statistics per building."""
    summary = df.groupby('Building')['kWh'].agg(['mean', 'min', 'max', 'sum']).reset_index()
    summary.rename(columns={'sum': 'total'}, inplace=True)
    summary_dict = summary.set_index('Building').to_dict('index')
    return summary, summary_dict


def task_2_aggregate_data(df_combined):
    print("\n--- Task 2: Core Aggregation Logic ---")

    if df_combined.empty:
        print("Skipping aggregation: Input DataFrame is empty.")
        return None, None, None

    daily_data = calculate_daily_totals(df_combined)
    weekly_data = calculate_weekly_aggregates(df_combined)
    summary_df, summary_dict = building_wise_summary(df_combined)

    print("Aggregation Complete.")
    print("\nSample Daily Totals:")
    print(daily_data.head())
    print("\nBuilding Summary (DataFrame):")
    print(summary_df)

    return daily_data, weekly_data, summary_df


# --- TASK 3: Object-Oriented Modeling ---
class MeterReading:
    """Models a single energy reading."""
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh


class Building:
    """Models a single building with energy consumption history."""
    def __init__(self, name):
        self.name = name
        self.meter_readings = []  # Stores MeterReading objects

    def add_reading(self, timestamp, kwh):
        """Adds a new meter reading to the building's list."""
        self.meter_readings.append(MeterReading(timestamp, kwh))

    def calculate_total_consumption(self):
        """Calculates the total kWh consumption for the building."""
        return sum(r.kwh for r in self.meter_readings)

    def generate_report(self):
        """Generates a simple report string."""
        total = self.calculate_total_consumption()
        return f"{self.name}: Total Consumption = {total:.2f} kWh"


class BuildingManager:
    """Manages all building objects."""
    def __init__(self):
        self.buildings = {}  # Stores {name: Building_object}

    def add_data_from_dataframe(self, df):
        """Processes the combined DataFrame and populates the objects."""
        for name in df['Building'].unique():
            if name not in self.buildings:
                self.buildings[name] = Building(name)

            building_df = df[df['Building'] == name].reset_index()
            for _, row in building_df.iterrows():
                self.buildings[name].add_reading(row['Timestamp'], row['kWh'])

    def generate_all_reports(self):
        """Prints reports for all managed buildings."""
        print("\n--- Task 3: Object-Oriented Modeling Reports ---")
        for name, building in self.buildings.items():
            print(building.generate_report())


def task_3_oop_modeling(df_combined):
    if df_combined.empty:
        print("Skipping OOP Modeling: Input DataFrame is empty.")
        return None

    # Reset index and make 'Building' a regular column for easier iteration
    df_for_oop = df_combined.reset_index()

    manager = BuildingManager()
    manager.add_data_from_dataframe(df_for_oop)
    manager.generate_all_reports()

    return manager


# --- TASK 4: Visual Output with Matplotlib ---
def task_4_visualize_data(daily_data, weekly_data, summary_df, df_combined):
    print("\n--- Task 4: Visual Output with Matplotlib ---")

    if daily_data is None or weekly_data is None or summary_df is None or df_combined is None:
        print("Skipping visualization: Aggregated data is missing.")
        return

    fig, axes = plt.subplots(3, 1, figsize=(12, 18))

    # Plot 1: Trend Line (Daily Consumption)
    # Pivot daily_data for easy plotting (Timestamp as index, Buildings as columns)
    daily_pivot = daily_data.pivot(index='Timestamp', columns='Building', values='Daily_kWh_Total')
    daily_pivot.plot(kind='line', ax=axes[0])
    axes[0].set_title('Daily Energy Consumption Over Time', fontsize=14)
    axes[0].set_ylabel('Total kWh', fontsize=12)
    axes[0].set_xlabel('Date', fontsize=12)
    axes[0].legend(title='Building')

    # Plot 2: Bar Chart (Average Weekly Usage)
    avg_weekly = weekly_data.groupby('Building')['Weekly_kWh_Total'].mean().sort_values(ascending=False)
    avg_weekly.plot(kind='bar', ax=axes[1], color=plt.cm.Paired(np.arange(len(avg_weekly))))
    axes[1].set_title('Average Weekly Usage Across Buildings', fontsize=14)
    axes[1].set_ylabel('Average Weekly kWh', fontsize=12)
    axes[1].set_xlabel('Building Name', fontsize=12)
    axes[1].tick_params(axis='x', rotation=0)

    # Plot 3: Scatter Plot (Peak-Hour Consumption vs. Time)
    df_hourly = (
        df_combined.groupby(['Building', pd.Grouper(level='Timestamp', freq='H')])['kWh']
        .max()
        .reset_index()
    )
    df_hourly['Hour'] = df_hourly['Timestamp'].dt.hour

    for name, group in df_hourly.groupby('Building'):
        axes[2].scatter(group['Hour'], group['kWh'], label=name, alpha=0.6)

    axes[2].set_title('Peak Hourly Consumption by Time and Building', fontsize=14)
    axes[2].set_ylabel('Peak Hourly kWh', fontsize=12)
    axes[2].set_xlabel('Hour of Day (0-23)', fontsize=12)
    axes[2].legend(title='Building')
    axes[2].grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    dashboard_path = OUTPUT_DIR / "dashboard.png"
    plt.savefig(dashboard_path)
    print(f"\nDashboard saved to: {dashboard_path}")
    plt.close()


# --- TASK 5: Persistence and Executive Summary ---
def task_5_persistence_summary(df_combined, summary_df):
    print("\n--- Task 5: Persistence and Executive Summary ---")

    if df_combined.empty or summary_df is None:
        print("Skipping persistence and summary: Data is missing.")
        return

    # 1. Export: Final processed dataset
    cleaned_data_path = OUTPUT_DIR / "cleaned_energy_data.csv"
    df_combined.to_csv(cleaned_data_path)
    print(f"Exported cleaned data to: {cleaned_data_path}")

    # 2. Export: Summary stats
    summary_stats_path = OUTPUT_DIR / "building_summary.csv"
    summary_df.to_csv(summary_stats_path, index=False)
    print(f"Exported summary stats to: {summary_stats_path}")

    # 3. Create a short summary report
    total_campus_consumption = summary_df['total'].sum()

    highest_consumer = summary_df.loc[summary_df['total'].idxmax()]
    highest_consuming_building = highest_consumer['Building']
    highest_consuming_kwh = highest_consumer['total']

    # Calculate Peak Load Time
    df_temp = df_combined.reset_index()
    peak_load_time = df_temp.groupby(df_temp['Timestamp'].dt.hour)['kWh'].mean().idxmax()

    # Simple trend analysis: Compare first half vs second half of the data
    mid_point = len(df_combined) // 2
    first_half_sum = df_combined.iloc[:mid_point]['kWh'].sum()
    second_half_sum = df_combined.iloc[mid_point:]['kWh'].sum()
    trend = "increasing" if second_half_sum > first_half_sum else "decreasing or stable"

    summary_content = f"""
*** Executive Summary: Campus Energy Consumption Analysis ***

1. Total Campus Consumption: {total_campus_consumption:,.2f} kWh

2. Highest-Consuming Building: {highest_consuming_building}
   (Total: {highest_consuming_kwh:,.2f} kWh)

3. Peak Load Time: Hour {peak_load_time}:00 (suggesting high usage during standard business hours).

4. Overall Trend: Usage appears to be {trend} over the monitored period.

*** End of Summary ***
"""

    # 4. Save the summary report
    summary_path = OUTPUT_DIR / "summary.txt"
    with open(summary_path, 'w') as f:
        f.write(summary_content)

    # 5. Print this summary to the console
    print(summary_content)
    print(f"Summary saved to: {summary_path}")
    print("\nPersistence and Summary Complete.")


# --- MAIN EXECUTION BLOCK ---
if __name__ == "__main__":
    # Ensure data directory exists for Task 1
    DATA_DIR.mkdir(exist_ok=True)
    print(f"Check the '{DATA_DIR}' folder for your CSV data.")

    # Task 1 Execution
    df_combined = task_1_ingest_data()

    if df_combined.empty:
        print("\n--- Project Aborted: No valid data ingested. ---")
    else:
        # Task 2 Execution
        df_daily, df_weekly, df_summary = task_2_aggregate_data(df_combined)

        # Task 3 Execution
        manager = task_3_oop_modeling(df_combined)

        # Task 4 Execution (requires Task 2 outputs and original combined df)
        task_4_visualize_data(df_daily, df_weekly, df_summary, df_combined)

        # Task 5 Execution (requires Task 1 & 2 outputs)
        task_5_persistence_summary(df_combined, df_summary)

        print("\n*** Capstone Project Execution Complete! ***")
        print("Check the 'output' folder for your deliverables (PNG, CSVs, TXT).")