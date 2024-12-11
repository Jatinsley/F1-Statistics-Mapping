# F1 Data Analysis Pipeline

## Overview

This Python-based project provides a pipeline for analyzing Formula 1 race data. The code addresses the challenge of extracting meaningful insights from race results, lap times, and other relevant data, helping users understand key performance aspects of drivers and races. The analysis focuses on aspects such as lap time consistency, pole-to-podium conversion, and race duration deviations from the historical average.

### Features:
- Analyze the correlation between pace consistency through fastest laps and final season positions.
- Calculate pole-to-podium conversion rates for drivers.
- Identify races with the most deviation from historical race duration.

## Why?

Formula 1 race data is publicly available and can provide valuable insights into various performance aspects of drivers and races. This project helps analyze these data points, enabling a deeper understanding of trends, consistency, and the relationship between lap time performance and race results. It’s an ideal tool for both F1 enthusiasts and researchers.

## Main Applications

- **Race Performance Analysis**: Correlation between lap times, fastest laps, and final positions.
- **Pole-to-Podium Conversion**: Conversion rate of pole positions to podium finishes for drivers.
- **Race Duration Analysis**: Identify races that deviate most from the historical race duration for each circuit.
- **General Race Insights**: Understand trends and performance metrics across seasons.

## Requirements

### Software Requirements:
- **Operating System**: Windows, macOS, or Linux.
- **Libraries**:
  - Python 3.7+
  - Pandas
  - NumPy
  - SciPy
  - Matplotlib
  - Seaborn

## Installation

### Step 1: Clone the Repository
'git clone https://github.com/<your-username>/f1-data-analysis.git cd f1-data-analysis'

### Step 2: Install Dependencies
Use `pip` to install the required Python libraries:
'pip install pandas numpy scipy matplotlib seaborn'

### Step 3: Download F1 Data
The following datasets are required for the analysis:
- `lap_times.csv`
- `results.csv`
- `driver_standings.csv`
- `drivers.csv`
- `races.csv`
- `qualifying.csv`

These CSV files should be placed in the `/f1db_csv/` folder.

## Analysis Questions

### Question 1: Fastest Lap vs Final Position

- **Goal**: Analyze whether setting the fastest lap correlates with a higher final position in the season.
- **Process**: Calculate lap time consistency (standard deviation) for each race based on the fastest lap achieved, then correlate it with the final season position.
- **Output**: 
- Correlation coefficient between fastest lap consistency and final season position.
- A bar plot showing the standard deviation of lap time consistency for each finishing position.

### Question 2: Pole-to-Podium Conversion Rate

- **Goal**: Determine how often pole positions result in podium finishes.
- **Process**: Track pole positions and podium finishes, then calculate the conversion rate for each driver.
- **Output**: 
- Average pole-to-podium conversion rate.
- Bar plot showing the conversion rate for each driver.

### Question 3: Most Deviating Race from Historical Average Total Race Duration

- **Goal**: Identify the race with the most deviation from the historical average race duration for each circuit.
- **Process**: Calculate total race duration for each race and compare it with the historical average for the same circuit.
- **Output**: 
- The race with the most deviation from historical race duration.
- Top 10 races with the largest deviations.

## Visualizations

The script generates the following visualizations:

1. **Variation in Lap Time Consistency**: A bar plot showing the standard deviation of lap times for different finishing positions (1-20).
2. **Pole-to-Podium Conversion Rate**: A bar chart displaying the conversion rate for each driver.
3. **Deviation of Average Lap Times**: A bar chart showing how average lap times deviate from the historical average for each race.

## Limitations

- **Data Dependency**: The analysis is dependent on the accuracy and completeness of the provided datasets. Missing or incorrect data may lead to incorrect results.
- **File Paths**: The data files must be placed in the `/f1db_csv/` directory for the pipeline to work.
- **Operating System**: The code has been developed and tested on Windows and macOS. The `f1_analysis.py` script should work across all these platforms as long as Python 3.7+ and the dependencies are correctly installed.

## Future Enhancements

- **Incorporate Additional Metrics**: Future versions of the analysis can include additional performance metrics, such as tire usage, pit stop times, and race strategy.
- **More Advanced Predictive Models**: Implement more advanced data models to predict race outcomes based on driver behavior and race conditions.
- **Real-Time Data Integration**: Allow the pipeline to integrate real-time race data to provide live analysis.

---

If you have any questions, issues, or suggestions for improvements, please feel free to open an issue or submit a pull request. Happy analyzing! 

