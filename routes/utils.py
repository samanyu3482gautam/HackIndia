import csv
import os
from django.conf import settings

def load_flight_data():
    flight_data = []
    csv_path = os.path.join(settings.BASE_DIR, 'static', 'flights.csv')

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert numeric fields to integers
            row['id']=int(row['id'])
            row['year'] = int(row['year'])
            row['month'] = int(row['month'])
            row['day'] = int(row['day'])
            row['hour'] = int(row['hour'])
            row['minute'] = int(row['minute'])
            row['sched_dep_time']=int(row['sched_dep_time'])
            row['sched_arr_time']=int(row['sched_arr_time'])
            row['arr_time'] = int(row['arr_time'])
            row['air_time'] = int(row['air_time'])
            row['flight_cost'] = int(row['flight_cost'])
            row['flight_number']=int(row['flight'])
            row['origin']=str(row['origin'])
            row['destination']=str(row['dest'])
            row['distance']=int(row['distance'])
            row['airline_name']=str(row['name'])
            flight_data.append(row)
    # print( flight_data)
    return flight_data



    
# {'id': '49998', 'year': 2013, 'month': 10, 'day': 25, 'dep_time': '1445', 'sched_dep_time': 1429, 
#  'arr_time': 1744, 'sched_arr_time': 1730, 'flight': '301', 'origin': 'JFK', 'dest': 'FLL', 
#  'air_time': 157, 'distance': 1069, 'hour': 14, 'minute': 29, 'name': 'JetBlue Airways', 
#  'Unnamed: 16': '99', 'flight_cost': 6012, 'flight_number': 301, 'destination': 'FLL', 
#  'airline_name': 'JetBlue Airways'}