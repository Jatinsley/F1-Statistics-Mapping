import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind

# Set the directory where your F1 data CSV files are stored
#data_dir = os.path.join(os.getcwd(), 'f1db_csv')  # Assuming f1db_csv is in the same directory as the script

# Paths to required CSVs
lap_times_path = 'lap_times.csv'
results_path = 'results.csv'
driver_standings_path = 'driver_standings.csv'
drivers_path = 'drivers.csv'
races_path = 'races.csv'
qualifying_path = 'qualifying.csv'

# Load necessary datasets
lap_times = pd.read_csv(lap_times_path)
results = pd.read_csv(results_path)
driver_standings = pd.read_csv(driver_standings_path)
drivers = pd.read_csv(drivers_path)
races = pd.read_csv(races_path)
qualifying = pd.read_csv(qualifying_path)

# Convert lap times to seconds
lap_times['seconds'] = lap_times['milliseconds'] / 1000

# Compute the number of laps for each race
race_laps = lap_times.groupby('raceId')['lap'].max().reset_index()
race_laps.rename(columns={'lap': 'num_laps'}, inplace=True)
races = races.merge(race_laps, on='raceId', how='left')

# ---------------------------------------
# Question 1: Fastest Lap vs Final Position
# ---------------------------------------

# Find the fastest lap for each race
fastest_laps = lap_times.loc[lap_times.groupby('raceId')['milliseconds'].idxmin()]

# Extract relevant columns: raceId, driverId, milliseconds
fastest_laps = fastest_laps[['raceId', 'driverId', 'milliseconds']]

# Calculate the standard deviation of lap times for each driver in each race using numpy
def calculate_std(group):
    return np.std(group, ddof=1)  # Sample standard deviation

lap_times['fastest_driver_std_dev'] = lap_times.groupby(['raceId', 'driverId'])['milliseconds'].transform(calculate_std)

# Merge the standard deviation data into the fastest_laps dataframe
fastest_laps = fastest_laps.merge(lap_times[['raceId', 'driverId', 'fastest_driver_std_dev']].drop_duplicates(), on=['raceId', 'driverId'], how='left')

# Add season information to the fastest_laps dataframe
fastest_laps = fastest_laps.merge(races[['raceId', 'year']], on='raceId', how='left')

# Add season finishing positions to the fastest_laps dataframe
fastest_laps = fastest_laps.merge(driver_standings[['raceId', 'driverId', 'position']], on=['raceId', 'driverId'], how='left')

# Drop duplicates and keep relevant columns
fastest_laps = fastest_laps.drop_duplicates(subset=['raceId', 'driverId'])

# Filter to include only season positions 1-10
correlation_data = fastest_laps[(fastest_laps['position'] <= 20)][['fastest_driver_std_dev', 'position']].dropna()

# Correlation analysis: Standard deviation vs. season finishing position
correlation_coefficient = correlation_data['fastest_driver_std_dev'].corr(correlation_data['position'])

print(f"Correlation Coefficient: {correlation_coefficient}")

# Group by season finishing position and calculate the standard deviation of lap time standard deviations
position_std_devs = correlation_data.groupby('position')['fastest_driver_std_dev'].std()



plt.bar(position_std_devs.index, position_std_devs.values, alpha=0.7, width=0.9)  # Adjust width for better alignment
plt.xticks(ticks=range(1, len(position_std_devs.index) + 1))  # Ensure ticks are at integer positions
plt.xlabel('Season Finishing Position')
plt.ylabel('Standard Deviation of Lap Time Standard Deviations')
plt.title('Variation in Lap Time Consistency Across Finishing Positions')
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Optional: Add a grid for clarity
plt.show()




print("------------------------------------------------------------------------------------------------------------------------------------------------")
print("| Question 1: Does achieving the fastest lap increase a driver’s final position or season ranking by boosting pace consistency? |")
# Output the results
print("Standard Deviations of Lap Time Standard Deviations by Position:")
print(position_std_devs)

print("------------------------------------------------------------------------------------------------------------------------------------------------")


# ---------------------------------------
# Question 2: Pole-to-Podium Conversion Rate
# ---------------------------------------

# Merge qualifying and results data to track pole positions and podiums
pole_to_podium = qualifying[['raceId', 'driverId', 'position']].merge(results[['raceId', 'driverId', 'positionOrder']],on=['raceId', 'driverId'], how='inner')

# Determine if driver finished on podium
pole_to_podium['podium'] = pole_to_podium['positionOrder'] <= 3

# Calculate conversion rate per driver
conversion_rate = pole_to_podium.groupby('driverId').agg(poles=('position', lambda x: (x == 1).sum()),podiums=('podium', 'sum')).reset_index()

# Exclude drivers with zero poles
conversion_rate = conversion_rate[conversion_rate['poles'] > 0]

# Calculate conversion rate
conversion_rate['conversion_rate'] = conversion_rate['podiums'] / conversion_rate['poles']

# Calculate average conversion rate
average_conversion_rate = conversion_rate['conversion_rate'].mean()
print("| Question 2: What is the conversion rate of pole positions to podium finishes? |")
print("| Average Conversion Rate: {:.3f}:1".format(average_conversion_rate, ), "for all drivers")
print("------------------------------------------------------------------------------------------------------------------------------------------------")

# ---------------------------------------
# Question 3: Most Deviating Race from Historical Average Total Race Duration
# ---------------------------------------

# Compute average lap time per raceId
avg_lap_time_per_race = lap_times.groupby('raceId')['seconds'].mean().reset_index()
avg_lap_time_per_race.rename(columns={'seconds': 'avg_lap_time'}, inplace=True)

# Merge with races to get number of laps and circuitId
avg_lap_time_per_race = avg_lap_time_per_race.merge(races[['raceId', 'name', 'date', 'circuitId', 'num_laps']], on='raceId', how='left')

# Compute total race duration per raceId
avg_lap_time_per_race['total_race_duration'] = avg_lap_time_per_race['avg_lap_time'] * avg_lap_time_per_race['num_laps']

# Compute historical average total race duration per circuitId
historical_avg_duration = avg_lap_time_per_race.groupby('circuitId')['total_race_duration'].mean().reset_index()
historical_avg_duration.rename(columns={'total_race_duration': 'avg_circuit_duration'}, inplace=True)

# Merge historical average duration into avg_lap_time_per_race
avg_lap_time_per_race = avg_lap_time_per_race.merge(historical_avg_duration, on='circuitId', how='left')

# Calculate deviation as the absolute difference between race total duration and circuit average total duration
avg_lap_time_per_race['deviation'] = abs(avg_lap_time_per_race['total_race_duration'] - avg_lap_time_per_race['avg_circuit_duration'])

# Identify the most deviating race and the top 10 deviating races
most_deviating_race = avg_lap_time_per_race.loc[avg_lap_time_per_race['deviation'].idxmax()]
deviant_race_id = most_deviating_race['raceId']
top_10_races = avg_lap_time_per_race.nlargest(10, 'deviation')[['name', 'date', 'raceId', 'deviation']]

print("| Question 3: What race has the most deviation from historical average total race duration? |")
print("| Race Name:", most_deviating_race['name'], "| Date:", most_deviating_race['date'], "| Race ID:", int(deviant_race_id))
print("| Deviation (Total Duration): {:.2f} seconds | Circuit Avg Total Duration: {:.2f} seconds | Deviation (Race Duration Difference): {:.2f} seconds".format(
    most_deviating_race['total_race_duration'], most_deviating_race['avg_circuit_duration'],most_deviating_race['deviation']))
print("------------------------------------------------------------------------------------------------------------------------------------------------")
print("| Top 10 Most Deviating Races From Historical Average |")
print("| Name                           | Date       | Race ID | Deviation per Driver (seconds)")
for _, row in top_10_races.iterrows():
    print(f"| {row['name']:<30} | {row['date']} | {int(row['raceId']):<7} | {row['deviation']:.2f}")
# ---------------------------------------
# Question 4: Predicting Position Based on Historical Performance
# ---------------------------------------

# Sort results by driverId and raceId
results_sorted = results.sort_values(['driverId', 'raceId'])

# Calculate cumulative average position up to the current race for each driver
results_sorted['historical_avg_position'] = results_sorted.groupby('driverId')['positionOrder'].expanding().mean().shift(1).reset_index(level=0, drop=True)

# Remove rows where historical average position is NaN (first race for each driver)
performance_correlation_data = results_sorted.dropna(subset=['historical_avg_position'])

# Calculate correlation between historical average position and current position
position_prediction_corr = performance_correlation_data[['positionOrder', 'historical_avg_position']].corr()

print("------------------------------------------------------------------------------------------------------------------------------------------------")
print("| Question 4: For a given circuit, can we reliably predict an individual's race position based on their historical performance? |")
print("| Correlation between Historical Average Position and Current Position | r = {:.2f}".format(
    position_prediction_corr.loc['positionOrder', 'historical_avg_position']))
print("------------------------------------------------------------------------------------------------------------------------------------------------")

# ---------------------------------------
# Print Results
# ---------------------------------------

# Create mappings for driver id and race id
driver_name_mapping = drivers.set_index('driverId')['surname']
race_name_mapping = races.set_index('raceId').apply(lambda x: f"{x['name']} ({x['date']})", axis=1)



# 2. Conversion Rate of Pole Positions to Podium Finishes
#retrieve number of pole positions per driverId by identifying grid position <=3
pole_positions = results[results['grid'] <= 3].groupby('driverId').size()
#retrieve number of podium finishes per driverId by identifying positionOrder <= 3
podium_finishes = results[results['positionOrder'] <= 3].groupby('driverId').size()
conversion_rate = (podium_finishes / pole_positions).dropna().sort_values()

# Replace driverId with surnames in index
conversion_rate.index = conversion_rate.index.map(driver_name_mapping)

# Plot
plt.figure(figsize=(12, 6))
conversion_rate.plot(kind='bar', color='skyblue')
plt.title('Number of Pole Positions per Podium Finish by Driver')
plt.xlabel('Driver Surname')
plt.ylabel('Conversion Rate')
plt.xticks(rotation=60)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

# 3. Deviation of Average Lap Times per Race
lap_times['time_seconds'] = lap_times['milliseconds'] / 1000
average_lap_times_per_race = lap_times.groupby('raceId')['time_seconds'].mean()
historical_average_lap_time = lap_times['time_seconds'].mean()

# Calculate deviations
deviation = (average_lap_times_per_race - historical_average_lap_time).abs()

# Replace raceId with race names/dates in index
deviation.index = deviation.index.map(race_name_mapping)

# Plot
plt.figure(figsize=(14, 7))
deviation.plot(kind='bar', color='lightcoral')
plt.title('Deviation of Average Lap Times from Historical Average (per Race)')
plt.xlabel('Race Name (Date)')
plt.ylabel('Average Deviation in Seconds (per Lap)')
plt.xticks(rotation=60)
plt.grid(axis='y')
plt.tight_layout()
plt.show()