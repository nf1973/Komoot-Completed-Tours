import json
import pandas as pd
from datetime import datetime
from collections import defaultdict

# Define the sport remapping as needed
SPORT_REMAPPING = {
    'jogging': 'Hike',
    'e_touringbicycle': 'Bike',
    'E_racebike': 'Bike',
    'E_touringbicycle': 'Bike',
    'Touringbicycle': 'Bike',
    'touringbicycle': 'Bike',
    'E_bike': 'Bike',
    'Hike': 'Hike',
    'hike': 'Hike',
    'racebike': 'Bike',
    'e_racebike': 'Bike',
}

def remap_sport(sport):
    return SPORT_REMAPPING.get(sport, sport)

# Load JSON data
try:
    with open('tours.json', 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    print("Error: tours.json file not found - did you already run extracttours.py?")
    exit()
    

tours = data['completed_tours']

# Initialize dictionaries for statistics
monthly_stats = defaultdict(lambda: {'count': 0, 'total_distance': 0})
sport_monthly_stats = defaultdict(lambda: defaultdict(lambda: {'count': 0, 'total_distance': 0}))

# Process each tour
for tour in tours:
    distance = tour['distance']
    original_sport = tour['sport']
    remapped_sport = remap_sport(original_sport)
    
    # Get month from the date
    date = tour['date']
    month = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m')
    
    # Update monthly statistics
    monthly_stats[month]['count'] += 1
    monthly_stats[month]['total_distance'] += distance
    
    # Update sport monthly statistics
    sport_monthly_stats[remapped_sport][month]['count'] += 1
    sport_monthly_stats[remapped_sport][month]['total_distance'] += distance

# Convert the statistics to DataFrames
monthly_df = pd.DataFrame([
    {'Month': month, 'Number of Tours': stats['count'], 'Total Distance (km)': stats['total_distance']}
    for month, stats in monthly_stats.items()
]).sort_values(by='Month')

# Print the overall monthly stats
print("Monthly Summary (all sports):")
print(monthly_df.to_string(index=False))

# Print individual sport tables
for sport, stats_by_month in sport_monthly_stats.items():
    sport_df = pd.DataFrame([
        {'Month': month, 'Number of Tours': stats['count'], 'Total Distance (km)': stats['total_distance']}
        for month, stats in stats_by_month.items()
    ]).sort_values(by='Month')
    
    print(f"\nSport: {sport}")
    print(sport_df.to_string(index=False))
