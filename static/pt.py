# import pandas as pd

# def fill_missing_round_int(csv_filepath, fill_value=0):
#     """
#     Reads a CSV file, identifies numeric columns with missing values (empty strings or NaN),
#     rounds existing decimal values to the nearest integer, and fills missing values
#     with a specified integer, ensuring the column's type is integer.

#     Args:
#         csv_filepath (str): The path to the CSV file.
#         fill_value (int, optional): The integer value to fill missing entries with. Defaults to 0.

#     Returns:
#         pandas.DataFrame: The modified DataFrame with rounded values and missing values filled as integers.
#                           Returns None if the file is not found or an error occurs.
#     """
#     try:
#         # Read the CSV file into a pandas DataFrame
#         df = pd.read_csv(csv_filepath)

#         for col in df.columns:
#             if pd.api.types.is_numeric_dtype(df[col]):
#                 print(f"Processing numeric column: '{col}'")
#                 # Round existing numeric values to the nearest integer
#                 df[col] = df[col].apply(lambda x: round(x) if pd.notna(x) else x)

#                 # Fill NaN values
#                 df[col].fillna(fill_value, inplace=True)

#                 # Fill empty strings (convert to NaN first for consistency)
#                 df[col].replace('', pd.NA, inplace=True)
#                 df[col].fillna(fill_value, inplace=True)

#                 # Explicitly try to cast to nullable integer type
#                 try:
#                     df[col] = df[col].astype('Int64')
#                 except Exception as e:
#                     print(f"Warning: Could not safely cast column '{col}' to integer: {e}")

#             else:
#                 print(f"Column '{col}' is not numeric. Skipping.")

#         return df

#     except FileNotFoundError:
#         print(f"Error: File not found at '{csv_filepath}'")
#         return None
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None

# if __name__ == "__main__":
#     file_path = input("Please enter the path to your CSV file: ")
#     default_fill_value = input("Please enter the integer value to fill missing entries with (press Enter for 0): ")
#     if default_fill_value:
#         try:
#             fill_value = int(default_fill_value)
#         except ValueError:
#             print("Invalid integer input. Using default fill value of 0.")
#             fill_value = 0
#     else:
#         fill_value = 0

#     modified_df = fill_missing_round_int(file_path, fill_value)

#     if modified_df is not None:
#         output_filepath = input("Please enter the path to save the modified CSV file (or press Enter to just display it): ")
#         if output_filepath:
#             try:
#                 modified_df.to_csv(output_filepath, index=False)
#                 print(f"Modified CSV file saved to '{output_filepath}'")
#             except Exception as e:
#                 print(f"Error saving the modified CSV: {e}")
#         else:
#             print("\nModified DataFrame:")
#             print(modified_df)

# import pandas as pd

# # Load your dataset (change the filename as needed)
# df = pd.read_csv('flights.csv')  # Replace with your actual file name

# # Extract the unique airport codes (replace 'airport_code' with your column name)
# unique_airports = df['dest'].dropna().unique()  # Drop NaNs if any

# # Sort for consistency (optional)
# unique_airports = sorted(unique_airports)

# # Save to a CSV file
# pd.DataFrame(unique_airports, columns=['airport_code']).to_csv('unique_airports.csv', index=False)

# # Or save as a plain text file if preferred
# with open('unique_airports.txt', 'w') as f:
#     for code in unique_airports:
#         f.write(code + '\n')

# print("Unique airport codes saved to 'unique_airports.csv' and 'unique_airports.txt'")


# import pandas as pd

# def get_unique_airlines(csv_filepath, output_filepath):
#     """
#     Reads a CSV file, extracts unique airline names, and writes them to a new file.

#     Args:
#         csv_filepath (str): The path to the input CSV file.
#         output_filepath (str): The path to the output file where unique airline names will be written.
#     """
#     try:
#         # Read the CSV file into a pandas DataFrame
#         df = pd.read_csv(csv_filepath)

#         # Check if the 'name' column exists
#         if 'name' not in df.columns:
#             print(f"Error: The CSV file '{csv_filepath}' does not contain a 'name' column.")
#             return

#         # Get the unique airline names from the 'name' column
#         unique_airlines = df['name'].unique()

#         # Write the unique airline names to the output file, one per line
#         with open(output_filepath, 'w') as outfile:
#             for airline in unique_airlines:
#                 outfile.write(f"{airline}\n")

#         print(f"Successfully extracted unique airline names and wrote them to '{output_filepath}'.")

#     except FileNotFoundError:
#         print(f"Error: The CSV file '{csv_filepath}' was not found.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# # Example usage:
# input_csv_file = 'flights.csv'  # Replace with the actual path to your CSV file
# output_text_file = 'unique_airlines.txt'      # Replace with the desired path for the output file

# get_unique_airlines(input_csv_file, output_text_file)





# import heapq
# import math
# from collections import defaultdict
# from django.http import JsonResponse

# def dijkstra(graph, start_node, end_node=None, weight_type='cost'):
#     distances = defaultdict(lambda: float('inf'))
#     distances[start_node] = 0
#     paths = defaultdict(list)
#     paths[start_node] = [(start_node, 0)]  # (node, arrival_time_minutes)
#     priority_queue = [(0, start_node, 0)]  # (cost, node, arrival_time_minutes)

#     while priority_queue:
#         current_cost, current_node, current_arrival_time = heapq.heappop(priority_queue)

#         if current_cost > distances[current_node]:
#             continue

#         if end_node and current_node == end_node:
#             break

#         for flight in graph.get(current_node, []):
#             neighbor = flight['destination']
#             cost = flight.get('cost')
#             departure_time_minutes = time_to_minutes(flight['start_time'])
#             duration = flight['duration']
#             arrival_time_minutes = departure_time_minutes + duration

#             if weight_type == 'cost':
#                 new_cost = current_cost + cost
#                 can_take_flight = True

#                 if paths[current_node] and len(paths[current_node]) > 1:
#                     previous_arrival_time = paths[current_node][-1][1]
#                     layover_duration = flight.get('layover_duration', 0)
#                     departure_from_current_node = previous_arrival_time + layover_duration
#                     if departure_from_current_node > departure_time_minutes:
#                         can_take_flight = False

#                 if can_take_flight:
#                     if new_cost < distances[neighbor]:
#                         distances[neighbor] = new_cost
#                         new_path = list(paths[current_node])
#                         new_path.append((neighbor, arrival_time_minutes))
#                         paths[neighbor] = new_path
#                         heapq.heappush(priority_queue, (new_cost, neighbor, arrival_time_minutes))
#             elif weight_type == 'duration':
#                 # Your existing duration-based logic (no change needed here)
#                 pass
#             else:
#                 raise ValueError(f"Invalid weight_type: {weight_type}")

#     if end_node:
#         return {end_node: distances[end_node]}, {end_node: [item[0] for item in paths[end_node]]}
#     else:
#         return distances, {node: [item[0] for item in path] for node, path in paths.items()}



# def dijkstra_with_time(graph, start_node, end_node=None):
#     distances = defaultdict(lambda: float('inf'))  # Earliest arrival time
#     distances[start_node] = 0
#     paths = defaultdict(list)
#     paths[start_node] = [(start_node, 0, None)]  # Initialize start node with arrival time 0
#     priority_queue = [(0, start_node, 0)]  # (arrival_time, city, previous_arrival_time)

#     while priority_queue:
#         current_arrival_time, current_node, previous_arrival_time = heapq.heappop(priority_queue)

#         if current_arrival_time > distances[current_node]:
#             continue

#         if end_node and current_node == end_node:
#             break

#         for flight in graph.get(current_node, []):
#             neighbor = flight['destination']
#             departure_time_str = flight['start_time']
#             duration = flight['duration']
#             departure_time_minutes = time_to_minutes(departure_time_str)
#             arrival_time_minutes = departure_time_minutes + duration

#             can_take_flight = True
#             start_time_for_next_flight = current_arrival_time  # Default for the first flight

#             if paths[current_node] and len(paths[current_node]) > 1:
#                 # Arrival time at the current node (after the previous flight)
#                 start_time_for_next_flight = paths[current_node][-1][1]
#                 if flight['layover'] == current_node: # Check if the current node is a layover for this flight
#                     layover_duration = flight.get('layover_duration', 0)
#                     start_time_for_next_flight += layover_duration

#             if start_time_for_next_flight > departure_time_minutes:
#                 can_take_flight = False

#             if can_take_flight:
#                 if arrival_time_minutes < distances[neighbor]:
#                     distances[neighbor] = arrival_time_minutes
#                     new_path = list(paths[current_node])
#                     new_path.append((neighbor, arrival_time_minutes, flight))
#                     paths[neighbor] = new_path
#                     heapq.heappush(priority_queue, (arrival_time_minutes, neighbor, current_arrival_time))

#     if end_node:
#         return {end_node: distances[end_node]}, {end_node: paths[end_node]}
#     else:
#         return distances, paths


# def time_to_minutes(time_str):
#     hours, minutes = map(int, time_str.split(':'))
#     return hours * 60 + minutes

# def format_time(total_minutes):
#     if total_minutes is None:
#         return "N/A"
#     hours = math.floor(total_minutes / 60)
#     minutes = total_minutes % 60
#     return f"{int(hours)} Hrs : {int(minutes)} Mins."


# def find_shortest_route(request):
#     graph_with_times = {
#         'DEL': [
#             {'destination': 'BOM', 'duration': 120, 'cost': 5000, 'layover': None, 'start_time': '08:00', 'reach_time': '10:00'},
#             {'destination': 'BLR', 'duration': 150, 'cost': 6000, 'layover': 'BOM', 'layover_duration': 60, 'start_time': '14:00', 'reach_time': '16:30'},
#             {'destination': 'HYD', 'duration': 180, 'cost': 5500, 'layover': 'BOM', 'layover_duration': 45, 'start_time': '11:30', 'reach_time': '14:30'},
#             {'destination': 'HYD', 'duration': 120, 'cost': 6000, 'layover': None, 'start_time': '16:00', 'reach_time': '18:00'},
#             # {'destination': 'MAA', 'duration': 150, 'cost': 5900, 'layover': None, 'start_time': '09:00', 'reach_time': '11:30'},
#             # {'destination': 'MAA', 'duration': 140, 'cost': 6000, 'layover': 'HYD', 'layover_duration': 30, 'start_time': '13:00', 'reach_time': '15:20'},
#         ],
#         'BOM': [
#             {'destination': 'DEL', 'duration': 130, 'cost': 4900, 'layover': None, 'start_time': '11:00', 'reach_time': '13:10'},
#             {'destination': 'BLR', 'duration': 90, 'cost': 4500, 'layover': 'DEL', 'layover_duration': 45, 'start_time': '17:00', 'reach_time': '18:30'},
#             {'destination': 'HYD', 'duration': 100, 'cost': 4700, 'layover': None, 'start_time': '14:00', 'reach_time': '15:40'},
#             {'destination': 'MAA', 'duration': 110, 'cost': 5000, 'layover': None, 'start_time': '18:00', 'reach_time': '19:50'},
#         ],
#         'BLR': [
#             {'destination': 'DEL', 'duration': 150, 'cost': 6000, 'layover': None, 'start_time': '10:00', 'reach_time': '12:30'},
#             {'destination': 'BOM', 'duration': 100, 'cost': 4500, 'layover': 'HYD', 'layover_duration': 30, 'start_time': '19:00', 'reach_time': '20:40'},
#             {'destination': 'HYD', 'duration': 60, 'cost': 4000, 'layover': None, 'start_time': '07:00', 'reach_time': '08:00'},
#             {'destination': 'MAA', 'duration': 70, 'cost': 4200, 'layover': None, 'start_time': '12:00', 'reach_time': '13:10'},
#         ],
#         'HYD': [
#             {'destination': 'DEL', 'duration': 170, 'cost': 5400, 'layover': 'BOM', 'layover_duration': 60, 'start_time': '06:00', 'reach_time': '08:50'},
#             {'destination': 'BOM', 'duration': 100, 'cost': 4700, 'layover': None, 'start_time': '15:00', 'reach_time': '16:40'},
#             {'destination': 'BLR', 'duration': 50, 'cost': 3900, 'layover': None, 'start_time': '11:00', 'reach_time': '11:50'},
#             {'destination': 'MAA', 'duration': 60, 'cost': 4100, 'layover': None, 'start_time': '14:29', 'reach_time': '16:40'},
#         ],
#         'MAA': [
#             {'destination': 'DEL', 'duration': 165, 'cost': 5600, 'layover': None, 'start_time': '14:00', 'reach_time': '16:45'},
#             {'destination': 'BOM', 'duration': 115, 'cost': 5100, 'layover': 'HYD', 'layover_duration': 45, 'start_time': '20:00', 'reach_time': '21:55'},
#             {'destination': 'BLR', 'duration': 70, 'cost': 4200, 'layover': None, 'start_time': '09:00', 'reach_time': '10:10'},
#             {'destination': 'HYD', 'duration': 60, 'cost': 4100, 'layover': None, 'start_time': '13:00', 'reach_time': '14:00'},
#         ],
#     }

#     start = 'DEL'
#     end = 'MAA'

#     cost_distances, cost_paths = dijkstra(graph_with_times, start, end_node=end, weight_type='cost')
#     time_distances, time_paths = dijkstra_with_time(graph_with_times, start, end_node=end)

#     result = {
#         'minimum_cost': {
#             'distance': cost_distances.get(end),
#             'path': cost_paths.get(end)
#         },
#         'earliest_arrival': {
#             'arrival_time_minutes': format_time(time_distances.get(end)),
#             'path': time_paths.get(end)
#         }
#     }

#     return JsonResponse(result)











# import heapq
# import math
# from collections import defaultdict
# from datetime import datetime, timedelta
# from django.http import JsonResponse

# # Converts date and time strings into datetime object
# def parse_datetime(date_str, time_str):
#     return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

# def format_time(dt_obj):
#     if dt_obj is None or dt_obj == float('inf'):
#         return "N/A"
#     return dt_obj.strftime("%Y-%m-%d %H:%M")

# def dijkstra(graph, start_node, end_node=None, weight_type='cost'):
#     distances = defaultdict(lambda: float('inf'))
#     distances[start_node] = 0
#     paths = defaultdict(list)
#     paths[start_node] = [(start_node, 0)]  # (node, cumulative_cost)

#     priority_queue = [(0, start_node)]

#     while priority_queue:
#         current_cost, current_node = heapq.heappop(priority_queue)

#         if current_cost > distances[current_node]:
#             continue

#         if end_node and current_node == end_node:
#             break

#         for flight in graph.get(current_node, []):
#             neighbor = flight['destination']
#             cost = flight.get('cost')

#             if weight_type == 'cost':
#                 new_cost = current_cost + cost
#             elif weight_type == 'duration':
#                 duration = flight['duration']
#                 new_cost = current_cost + duration
#             else:
#                 raise ValueError(f"Invalid weight_type: {weight_type}")

#             if new_cost < distances[neighbor]:
#                 distances[neighbor] = new_cost
#                 new_path = list(paths[current_node])
#                 new_path.append((neighbor, new_cost))
#                 paths[neighbor] = new_path
#                 heapq.heappush(priority_queue, (new_cost, neighbor))

#     if end_node:
#         return {end_node: distances[end_node]}, {end_node: [node for node, _ in paths[end_node]]}
#     else:
#         return distances, {node: [n for n, _ in path] for node, path in paths.items()}

# def dijkstra_with_time(graph, start_node, end_node=None):
#     arrival_times = defaultdict(lambda: datetime.max)
#     # paths = defaultdict(list)
#     paths = defaultdict(list)
#     journey_start = datetime(2025, 5, 1, 0, 0)
#     paths[start_node] = [(start_node, journey_start, None)]  # Add start point


#     # Assume the journey starts at an arbitrary early date
   
#     arrival_times[start_node] = journey_start

#     priority_queue = [(journey_start, start_node)]

#     while priority_queue:
#         current_arrival_time, current_node = heapq.heappop(priority_queue)

#         if current_arrival_time > arrival_times[current_node]:
#             continue

#         if end_node and current_node == end_node:
#             break

#         for flight in graph.get(current_node, []):
#             neighbor = flight['destination']
#             departure_datetime = parse_datetime(flight['date'], flight['start_time'])
#             duration_minutes = flight['duration']
#             arrival_datetime = departure_datetime + timedelta(minutes=duration_minutes)

#             # Layover handling
#             layover_duration = flight.get('layover_duration', 0)
#             earliest_departure_time = current_arrival_time + timedelta(minutes=layover_duration)

#             can_take_flight = departure_datetime >= earliest_departure_time

#             if can_take_flight and arrival_datetime < arrival_times[neighbor]:
#                 arrival_times[neighbor] = arrival_datetime
#                 new_path = list(paths[current_node])
#                 new_path.append((neighbor, arrival_datetime, flight))
#                 paths[neighbor] = new_path
#                 heapq.heappush(priority_queue, (arrival_datetime, neighbor))

#     if end_node:
#         return {end_node: arrival_times[end_node]}, {end_node: paths[end_node]}
#     else:
#         return arrival_times, paths
    
     
# def find_shortest_route(request):
#     # (same graph_with_times)
#     graph_with_times = {
#         'DEL': [
#             {'destination': 'BOM', 'duration': 120, 'cost': 5000, 'layover': None, 'start_time': '08:00', 'reach_time': '10:00', 'date': '2025-05-01'},
#             {'destination': 'BLR', 'duration': 150, 'cost': 6000, 'layover': 'BOM', 'layover_duration': 60, 'start_time': '14:00', 'reach_time': '16:30', 'date': '2025-05-01'},
#             {'destination': 'HYD', 'duration': 180, 'cost': 5500, 'layover': 'BOM', 'layover_duration': 45, 'start_time': '11:30', 'reach_time': '14:30', 'date': '2025-05-01'},
#             {'destination': 'HYD', 'duration': 120, 'cost': 6000, 'layover': None, 'start_time': '16:00', 'reach_time': '18:00', 'date': '2025-05-01'},
#         ],
#         'BOM': [
#             {'destination': 'DEL', 'duration': 130, 'cost': 4900, 'layover': None, 'start_time': '11:00', 'reach_time': '13:10', 'date': '2025-05-01'},
#             {'destination': 'BLR', 'duration': 90, 'cost': 4500, 'layover': 'DEL', 'layover_duration': 45, 'start_time': '17:00', 'reach_time': '18:30', 'date': '2025-05-01'},
#             {'destination': 'HYD', 'duration': 100, 'cost': 4700, 'layover': None, 'start_time': '14:00', 'reach_time': '15:40', 'date': '2025-05-01'},
#             {'destination': 'MAA', 'duration': 110, 'cost': 5000, 'layover': None, 'start_time': '18:00', 'reach_time': '19:50', 'date': '2025-05-01'},
#         ],
#         'BLR': [
#             {'destination': 'DEL', 'duration': 150, 'cost': 6000, 'layover': None, 'start_time': '10:00', 'reach_time': '12:30', 'date': '2025-05-01'},
#             {'destination': 'BOM', 'duration': 100, 'cost': 4500, 'layover': 'HYD', 'layover_duration': 30, 'start_time': '19:00', 'reach_time': '20:40', 'date': '2025-05-01'},
#             {'destination': 'HYD', 'duration': 60, 'cost': 4000, 'layover': None, 'start_time': '07:00', 'reach_time': '08:00', 'date': '2025-05-01'},
#             {'destination': 'MAA', 'duration': 70, 'cost': 4200, 'layover': None, 'start_time': '12:00', 'reach_time': '13:10', 'date': '2025-05-01'},
#         ],
#         'HYD': [
#             {'destination': 'DEL', 'duration': 170, 'cost': 5400, 'layover': 'BOM', 'layover_duration': 60, 'start_time': '06:00', 'reach_time': '08:50', 'date': '2025-05-01'},
#             {'destination': 'BOM', 'duration': 100, 'cost': 4700, 'layover': None, 'start_time': '15:00', 'reach_time': '16:40', 'date': '2025-05-01'},
#             {'destination': 'BLR', 'duration': 50, 'cost': 3900, 'layover': None, 'start_time': '11:00', 'reach_time': '11:50', 'date': '2025-05-01'},
#             {'destination': 'MAA', 'duration': 60, 'cost': 4100, 'layover': None, 'start_time': '14:29', 'reach_time': '15:29', 'date': '2025-05-01'},
#         ],
#         'MAA': [
#             {'destination': 'DEL', 'duration': 165, 'cost': 5600, 'layover': None, 'start_time': '14:00', 'reach_time': '16:45', 'date': '2025-05-01'},
#             {'destination': 'BOM', 'duration': 115, 'cost': 5100, 'layover': 'HYD', 'layover_duration': 45, 'start_time': '20:00', 'reach_time': '21:55', 'date': '2025-05-01'},
#             {'destination': 'BLR', 'duration': 70, 'cost': 4200, 'layover': None, 'start_time': '09:00', 'reach_time': '10:10', 'date': '2025-05-01'},
#             {'destination': 'HYD', 'duration': 60, 'cost': 4100, 'layover': None, 'start_time': '13:00', 'reach_time': '14:00', 'date': '2025-05-01'},
#         ],
#     }


#     start = 'DEL'
#     end = 'MAA'

#     cost_distances, cost_paths = dijkstra(graph_with_times, start, end_node=end, weight_type='cost')
#     time_distances, time_paths = dijkstra_with_time(graph_with_times, start, end_node=end)

#     time_path = time_paths.get(end, [])
#     if time_path:
#         # Find the first non-None flight
#         for node, arrival_time, flight in time_path:
#             if flight is not None:
#                 first_departure = parse_datetime(flight['date'], flight['start_time'])
#                 break
#         else:
#             first_departure = None  # If no flight found

#         last_arrival = time_path[-1][1]

#         if first_departure:
#             total_travel_time = last_arrival - first_departure
#             total_minutes = int(total_travel_time.total_seconds() // 60)
#         else:
#             total_minutes = None
#     else:
#         total_minutes = None


#     result = {
#         'minimum_cost': {
#             'cost': cost_distances.get(end),
#             'path': cost_paths.get(end)
#         },
#         'earliest_arrival': {
#             'arrival_time': format_time(time_distances.get(end)),
#             'path': [node for node, _, _ in time_paths.get(end, [])],
#             'total_travel_time_minutes': total_minutes
#         }
#     }

#     return JsonResponse(result)



# converted_flight_data = [
#     {"year": 2025, "month": 5, "day": 1, "dep_time": 800, "sched_dep_time": 800, "arr_time": 1000, "sched_arr_time": 1000, "flight": 1000, "origin": "DEL", "dest": "BOM", "air_time": 120, "distance": 1000, "hour": 8, "minute": 0, "name": "Demo Airlines", "flight_cost": 5000},
#     {"year": 2025, "month": 5, "day": 1, "dep_time": 1400, "sched_dep_time": 1400, "arr_time": 1630, "sched_arr_time": 1630, "flight": 1001, "origin": "DEL", "dest": "BLR", "air_time": 150, "distance": 1000, "hour": 14, "minute": 0, "name": "Demo Airlines", "flight_cost": 6000},
#     {"year": 2025, "month": 5, "day": 1, "dep_time": 1130, "sched_dep_time": 1130, "arr_time": 1430, "sched_arr_time": 1430, "flight": 1002, "origin": "DEL", "dest": "HYD", "air_time": 180, "distance": 1000, "hour": 11, "minute": 30, "name": "Demo Airlines", "flight_cost": 5500},
#     {"year": 2025, "month": 5, "day": 1, "dep_time": 1600, "sched_dep_time": 1600, "arr_time": 1800, "sched_arr_time": 1800, "flight": 1003, "origin": "DEL", "dest": "HYD", "air_time": 120, "distance": 1000, "hour": 16, "minute": 0, "name": "Demo Airlines", "flight_cost": 6000},
    
#     {"year": 2025, "month": 5, "day": 1, "dep_time": 1100, "sched_dep_time": 1100, "arr_time": 1310, "sched_arr_time": 1310, "flight": 1004, "origin": "BOM", "dest": "DEL", "air_time": 130, "distance": 1000, "hour": 11, "minute": 0, "name": "Demo Airlines", "flight_cost": 4900},
#     {"year": 2025, "month": 5, "day": 1, "dep_time": 1700, "sched_dep_time": 1700, "arr_time": 1830, "sched_arr_time": 1830, "flight": 1005, "origin": "BOM", "dest": "BLR", "air_time": 90, "distance": 1000, "hour": 17, "minute": 0, "name": "Demo Airlines", "flight_cost": 4500},
#     {"year": 2025, "month": 5, "day": 1, "dep_time": 1400, "sched_dep_time": 1400, "arr_time": 1540, "sched_arr_time": 1540, "flight": 1006, "origin": "BOM", "dest": "HYD", "air_time": 100, "distance": 1000, "hour": 14, "minute": 0, "name": "Demo Airlines", "flight_cost": 4700},
#     {"year": 2025, "month": 5, "day": 1, "dep_time": 1800, "sched_dep_time": 1800, "arr_time": 1950, "sched_arr_time": 1950, "flight": 1007, "origin": "BOM", "dest": "MAA", "air_time": 110, "distance": 1000, "hour": 18, "minute": 0, "name": "Demo Airlines", "flight_cost": 5000},

#     {"year": 2025, "month": 5, "day": 1, "dep_time": 1000, "sched_dep_time": 1000, "arr_time": 1230, "sched_arr_time": 1230, "flight": 1008, "origin": "BLR", "dest": "DEL", "air_time": 150, "distance": 1000, "hour": 10, "minute": 0, "name": "Demo Airlines", "flight_cost": 6000},
#     {"year": 2025, "month": 5, "day": 1, "dep_time": 1900, "sched_dep_time": 1900, "arr_time": 2040, "sched_arr_time": 2040, "flight": 1009, "origin": "BLR", "dest": "BOM", "air_time": 100, "distance": 1000, "hour": 19, "minute": 0, "name": "Demo Airlines", "flight_cost": 4500},
#     {"year": 2025, "month": 5, "day": 1, "dep_time": 700, "sched_dep_time": 700, "arr_time": 800, "sched_arr_time": 800, "flight": 1010, "origin": "BLR", "dest": "HYD", "air_time": 60, "distance": 1000, "hour": 7, "minute": 0, "name": "Demo Airlines", "flight_cost": 4000},
#     {"year": 2025, "month": 5, "day": 1, "dep_time": 1200, "sched_dep_time": 1200, "arr_time": 1310, "sched_arr_time": 1310, "flight": 1011, "origin": "BLR", "dest": "MAA", "air_time": 70, "distance": 1000, "hour": 12, "minute": 0, "name": "Demo Airlines", "flight_cost": 4200},

#     {"year": 2025, "month": 5, "day": 1, "dep_time": 600, "sched_dep_time": 600, "arr_time": 850, "sched_arr_time": 850, "flight": 1012, "origin": "HYD", "dest": "DEL", "air_time": 170, "distance": 1000, "hour": 6, "minute": 0, "name": "Demo Airlines", "flight_cost": 5400},
#     {"year": 2025, "month": 5, "day": 1, "dep_time": 1500, "sched_dep_time": 1500, "arr_time": 1640, "sched_arr_time": 1640, "flight": 1013, "origin": "HYD", "dest": "BOM", "air_time": 100, "distance": 1000, "hour": 15, "minute": 0, "name": "Demo Airlines", "flight_cost": 4700},
#     {"year": 2025, "month": 5, "day": 1, "dep_time": 1100, "sched_dep_time": 1100, "arr_time": 1150, "sched_arr_time": 1150, "flight": 1014, "origin": "HYD", "dest": "BLR", "air_time": 50, "distance": 1000, "hour": 11, "minute": 0, "name": "Demo Airlines", "flight_cost": 3900},
#     {"year": 2025, "month": 5, "day": 1, "dep_time": 1429, "sched_dep_time": 1429, "arr_time": 1529, "sched_arr_time": 1529, "flight": 1015, "origin": "HYD", "dest": "MAA", "air_time": 60, "distance": 1000, "hour": 14, "minute": 29, "name": "Demo Airlines", "flight_cost": 4100},

#     {"year": 2025, "month": 5, "day": 1, "dep_time": 1400, "sched_dep_time": 1400, "arr_time": 1645, "sched_arr_time": 1645, "flight": 1016, "origin": "MAA", "dest": "DEL", "air_time": 165, "distance": 1000, "hour": 14, "minute": 0, "name": "Demo Airlines", "flight_cost": 5600},
#     {"year": 2025, "month": 5, "day": 1, "dep_time": 2000, "sched_dep_time": 2000, "arr_time": 2155, "sched_arr_time": 2155, "flight": 1017, "origin": "MAA", "dest": "BOM", "air_time": 115, "distance": 1000, "hour": 20, "minute": 0, "name": "Demo Airlines", "flight_cost": 5100},
#     {"year": 2025, "month": 5, "day": 1, "dep_time": 900, "sched_dep_time": 900, "arr_time": 1010, "sched_arr_time": 1010, "flight": 1018, "origin": "MAA", "dest": "BLR", "air_time": 70, "distance": 1000, "hour": 9, "minute": 0, "name": "Demo Airlines", "flight_cost": 4200},
#     {"year": 2025, "month": 5, "day": 1, "dep_time": 1300, "sched_dep_time": 1300, "arr_time": 1400, "sched_arr_time": 1400, "flight": 1019, "origin": "MAA", "dest": "HYD", "air_time": 60, "distance": 1000, "hour": 13, "minute": 0, "name": "Demo Airlines", "flight_cost": 4100},
# ]















# import heapq
# import math
# from collections import defaultdict
# from datetime import datetime, timedelta
# from django.http import JsonResponse

# # Converts date and time strings into datetime object
# def parse_datetime(date_str, time_str):
#     return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

# def format_time(dt_obj):
#     if dt_obj is None or dt_obj == float('inf'):
#         return "N/A"
#     return dt_obj.strftime("%Y-%m-%d %H:%M")

# def dijkstra(graph, start_node, end_node=None, weight_type='cost'):
#     distances = defaultdict(lambda: float('inf'))
#     distances[start_node] = 0
#     paths = defaultdict(list)
#     paths[start_node] = [(start_node, 0)]  # (node, cumulative_cost)

#     priority_queue = [(0, start_node)]

#     while priority_queue:
#         current_cost, current_node = heapq.heappop(priority_queue)

#         if current_cost > distances[current_node]:
#             continue

#         if end_node and current_node == end_node:
#             break

#         for flight in graph.get(current_node, []):
#             neighbor = flight['destination']
#             cost = flight.get('cost')

#             if weight_type == 'cost':
#                 new_cost = current_cost + cost
#             elif weight_type == 'duration':
#                 duration = flight['duration']
#                 new_cost = current_cost + duration
#             else:
#                 raise ValueError(f"Invalid weight_type: {weight_type}")

#             if new_cost < distances[neighbor]:
#                 distances[neighbor] = new_cost
#                 new_path = list(paths[current_node])
#                 new_path.append((neighbor, new_cost))
#                 paths[neighbor] = new_path
#                 heapq.heappush(priority_queue, (new_cost, neighbor))

#     if end_node:
#         return {end_node: distances[end_node]}, {end_node: [node for node, _ in paths[end_node]]}
#     else:
#         return distances, {node: [n for n, _ in path] for node, path in paths.items()}

# def dijkstra_with_time(graph, start_node, end_node=None):
#     arrival_times = defaultdict(lambda: datetime.max)
#     # paths = defaultdict(list)
#     paths = defaultdict(list)
#     #journey_start = datetime(2025, 5, 1, 0, 0)
    
#     first_flights = graph.get(start_node, [])
#     if not first_flights:
#         return {}, {}
#     journey_start = min(parse_datetime(f['date'], f['start_time']) for f in first_flights)

    
#     paths[start_node] = [(start_node, journey_start, None)]  # Add start point


#     # Assume the journey starts at an arbitrary early date
   
#     arrival_times[start_node] = journey_start

#     priority_queue = [(journey_start, start_node)]

#     while priority_queue:
#         current_arrival_time, current_node = heapq.heappop(priority_queue)

#         if current_arrival_time > arrival_times[current_node]:
#             continue

#         if end_node and current_node == end_node:
#             break

#         for flight in graph.get(current_node, []):
#             neighbor = flight['destination']
#             departure_datetime = parse_datetime(flight['date'], flight['start_time'])
#             duration_minutes = flight['duration']
#             arrival_datetime = departure_datetime + timedelta(minutes=duration_minutes)

#             # Layover handling
#             layover_duration = flight.get('layover_duration') or 0
#             earliest_departure_time = current_arrival_time + timedelta(minutes=layover_duration)

#             can_take_flight = departure_datetime >= earliest_departure_time

#             if can_take_flight and arrival_datetime < arrival_times[neighbor]:
#                 arrival_times[neighbor] = arrival_datetime
#                 new_path = list(paths[current_node])
#                 new_path.append((neighbor, arrival_datetime, flight))
#                 paths[neighbor] = new_path
#                 heapq.heappush(priority_queue, (arrival_datetime, neighbor))

#     if end_node:
#         return {end_node: arrival_times[end_node]}, {end_node: paths[end_node]}
#     else:
#         return arrival_times, paths
    

# def convert_to_graph_structure(flight_data):
#     graph = defaultdict(list)
#     for flight in flight_data:
#         origin = flight['origin']
#         destination = flight['dest']
#         duration = flight['air_time']
#         cost = flight['flight_cost']
#         date = f"{flight['year']}-{int(flight['month']):02d}-{int(flight['day']):02d}"
#         start_hour = int(flight['hour'])
#         start_minute = int(flight['minute'])
#         start_time = f"{start_hour:02d}:{start_minute:02d}"
        
#         arr_time = int(flight['arr_time'])
#         arr_hour = arr_time // 100
#         arr_minute = arr_time % 100
#         reach_time = f"{arr_hour:02d}:{arr_minute:02d}"
#         airline=flight['airline_name']
#         distance=flight['distance']
#         sch_dep_time=flight['sched_dep_time']
#         sch_arr_time=flight['sched_arr_time']
#         id=flight['id']



#         graph[origin].append({
#             'destination': destination,
#             'duration': duration,
#             'cost': cost,
#             'layover': None,  # or compute based on your needs
#             'start_time': start_time,
#             'reach_time': reach_time,
#             'date': date,
#             'name':airline,
#             "distance":distance,
#             'dep_time':sch_dep_time,
#             'arr_time':sch_arr_time,
#             'id':id,
            

#         })
#     return graph


# from .utils import load_flight_data

# def find_shortest_route(request):
#     converted_flight_data = load_flight_data()
#     graph_with_times = convert_to_graph_structure(converted_flight_data)

#     start = 'LGA'
#     end = 'IAD'
    
#     cost_distances, cost_paths = dijkstra(graph_with_times, start, end_node=end, weight_type='cost')
#     time_distances, time_paths = dijkstra_with_time(graph_with_times, start, end_node=end)

#     # time_path = time_paths.get(end, [])
#     # if time_path:
#     #     for node, arrival_time, flight in time_path:
#     #         if flight is not None:
#     #             first_departure = parse_datetime(flight['date'], flight['start_time'])
#     #             break
#     #     else:
#     #         first_departure = None

#     #     last_arrival = time_path[-1][1]
#     #     total_minutes = int((last_arrival - first_departure).total_seconds() // 60) if first_departure else None
#     # else:
#     #     total_minutes = None

#     time_path = time_paths.get(end, [])
#     flights_only = [flight for _, _, flight in time_path if flight is not None]

#     if flights_only:
#         first_departure = parse_datetime(flights_only[0]['date'], flights_only[0]['start_time'])
#         last_arrival = parse_datetime(flights_only[-1]['date'], flights_only[-1]['start_time']) + timedelta(minutes=flights_only[-1]['duration'])
#         total_minutes = int((last_arrival - first_departure).total_seconds() // 60)
#     else:
#         total_minutes = None


#     result = {
#         'minimum_cost': {
#             'cost': cost_distances.get(end),
#             'path': cost_paths.get(end)
#         },
#         'earliest_arrival': {
#             'arrival_time': format_time(time_distances.get(end)),
#             'path': [node for node, _, _ in time_paths.get(end, [])],
#             'total_travel_time_minutes': total_minutes
#         }
#     }

#     return JsonResponse(result)



# import heapq
# import math
# from collections import defaultdict
# from datetime import datetime, timedelta
# from django.http import JsonResponse

# # Converts date and time strings into datetime object
# def parse_datetime(date_str, time_str):
#     return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

# def format_time(dt_obj):
#     if dt_obj is None or dt_obj == float('inf'):
#         return "N/A"
#     return dt_obj.strftime("%Y-%m-%d %H:%M")

# def dijkstra(graph, start_node, end_node=None, weight_type='cost'):
#     distances = defaultdict(lambda: float('inf'))
#     distances[start_node] = 0
#     paths = defaultdict(list)
#     paths[start_node] = [(start_node, 0, None)]  # (node, cumulative_cost, flight_id)

#     priority_queue = [(0, start_node)]

#     while priority_queue:
#         current_cost, current_node = heapq.heappop(priority_queue)

#         if current_cost > distances[current_node]:
#             continue

#         if end_node and current_node == end_node:
#             break

#         for flight in graph.get(current_node, []):
#             neighbor = flight['destination']
#             cost = flight.get('cost')
#             flight_id = flight.get('id')

#             if weight_type == 'cost':
#                 new_cost = current_cost + cost
#             elif weight_type == 'duration':
#                 duration = flight['duration']
#                 new_cost = current_cost + duration
#             else:
#                 raise ValueError(f"Invalid weight_type: {weight_type}")

#             if new_cost < distances[neighbor]:
#                 distances[neighbor] = new_cost
#                 new_path = list(paths[current_node])
#                 new_path.append((neighbor, new_cost, flight_id))
#                 paths[neighbor] = new_path
#                 heapq.heappush(priority_queue, (new_cost, neighbor))

#     if end_node:
#         return {end_node: distances[end_node]}, {end_node: paths[end_node]}
#     else:
#         return distances, paths

# def dijkstra_with_time(graph, start_node, end_node=None):
#     arrival_times = defaultdict(lambda: datetime.max)
#     paths = defaultdict(list)
    
#     first_flights = graph.get(start_node, [])
#     if not first_flights:
#         return {}, {}
#     journey_start = min(parse_datetime(f['date'], f['start_time']) for f in first_flights)

    
#     paths[start_node] = [(start_node, journey_start, None)]  # (node, arrival_time, flight_id)

#     arrival_times[start_node] = journey_start

#     priority_queue = [(journey_start, start_node)]

#     while priority_queue:
#         current_arrival_time, current_node = heapq.heappop(priority_queue)

#         if current_arrival_time > arrival_times[current_node]:
#             continue

#         if end_node and current_node == end_node:
#             break

#         for flight in graph.get(current_node, []):
#             neighbor = flight['destination']
#             departure_datetime = parse_datetime(flight['date'], flight['start_time'])
#             duration_minutes = flight['duration']
#             arrival_datetime = departure_datetime + timedelta(minutes=duration_minutes)
#             flight_id = flight.get('id')


#             # Layover handling
#             layover_duration = flight.get('layover_duration') or 0
#             earliest_departure_time = current_arrival_time + timedelta(minutes=layover_duration)

#             can_take_flight = departure_datetime >= earliest_departure_time

#             if can_take_flight and arrival_datetime < arrival_times[neighbor]:
#                 arrival_times[neighbor] = arrival_datetime
#                 new_path = list(paths[current_node])
#                 new_path.append((neighbor, arrival_datetime, flight_id))
#                 paths[neighbor] = new_path
#                 heapq.heappush(priority_queue, (arrival_datetime, neighbor))

#     if end_node:
#         return {end_node: arrival_times[end_node]}, {end_node: paths[end_node]}
#     else:
#         return arrival_times, paths
    

# def convert_to_graph_structure(flight_data):
#     graph = defaultdict(list)
#     for flight in flight_data:
#         origin = flight['origin']
#         destination = flight['dest']
#         duration = flight['air_time']
#         cost = flight['flight_cost']
#         date = f"{flight['year']}-{int(flight['month']):02d}-{int(flight['day']):02d}"
#         start_hour = int(flight['hour'])
#         start_minute = int(flight['minute'])
#         start_time = f"{start_hour:02d}:{start_minute:02d}"
        
#         arr_time = int(flight['arr_time'])
#         arr_hour = arr_time // 100
#         arr_minute = arr_time % 100
#         reach_time = f"{arr_hour:02d}:{arr_minute:02d}"
#         airline=flight['airline_name']
#         distance=flight['distance']
#         sch_dep_time=flight['sched_dep_time']
#         sch_arr_time=flight['sched_arr_time']
#         id=flight['id']



#         graph[origin].append({
#             'destination': destination,
#             'duration': duration,
#             'cost': cost,
#             'layover': None,  # or compute based on your needs
#             'start_time': start_time,
#             'reach_time': reach_time,
#             'date': date,
#             'name':airline,
#             "distance":distance,
#             'dep_time':sch_dep_time,
#             'arr_time':sch_arr_time,
#             'id':id,
            

#         })
#     return graph


# from .utils import load_flight_data

# def find_shortest_route(request):
#     converted_flight_data = load_flight_data()
#     graph_with_times = convert_to_graph_structure(converted_flight_data)

#     start = 'LGA'
#     end = 'ATL'
    
#     cost_distances, cost_paths_with_ids = dijkstra(graph_with_times, start, end_node=end, weight_type='cost')
#     time_distances, time_paths_with_ids = dijkstra_with_time(graph_with_times, start, end_node=end)

#     def get_flight_details(flight_id):
#         for flight in converted_flight_data:
#             if flight['id'] == flight_id:
#                 return flight
#         return None

#     cost_path_details = []
#     cost_path_with_ids = cost_paths_with_ids.get(end, [])
#     for _, _, flight_id in cost_path_with_ids[1:]:  # Exclude the start node
#         flight_detail = get_flight_details(flight_id)
#         if flight_detail:
#             cost_path_details.append(flight_detail)

#     time_path_details = []
#     time_path_with_ids = time_paths_with_ids.get(end, [])
#     first_departure_time = None
#     last_arrival_time = None

#     for i, (node, arrival_time, flight_id) in enumerate(time_path_with_ids[1:]): # Exclude the start node
#         flight_detail = get_flight_details(flight_id)
#         if flight_detail:
#             time_path_details.append(flight_detail)
#             departure_date_str = f"{flight_detail['year']}-{int(flight_detail['month']):02d}-{int(flight_detail['day']):02d}"
#             departure_time_str = f"{int(flight_detail['hour']):02d}:{int(flight_detail['minute']):02d}"
#             arrival_time_str = f"{int(flight_detail['arr_time']) // 100:02d}:{int(flight_detail['arr_time']) % 100:02d}"

#             if i == 0:
#                 first_departure_time = parse_datetime(departure_date_str, departure_time_str)

#             # We need to construct the arrival datetime using the departure date and arrival time,
#             # assuming the arrival is on the same day for simplicity in this calculation.
#             # For multi-day flights, this logic would need to be more robust.
#             last_arrival_time = parse_datetime(departure_date_str, arrival_time_str) + timedelta(minutes=flight_detail['air_time'])


#     total_travel_time_minutes_time = int((last_arrival_time - first_departure_time).total_seconds() // 60) if first_departure_time and last_arrival_time else None

#     min_cost={
#             'cost': cost_distances.get(end),
#             'path_nodes': [node for node, _, _ in cost_paths_with_ids.get(end, [])],
#             'path_details': cost_path_details
#         }
#     min_time= {
#             'arrival_time': format_time(time_distances.get(end)),
#             'path_nodes': [node for node, _, _ in time_paths_with_ids.get(end, [])],
#             'path_details': time_path_details,
#             'total_travel_time_minutes': total_travel_time_minutes_time
#         }
#     result = {
#         'minimum_cost': {
#             'cost': cost_distances.get(end),
#             'path_nodes': [node for node, _, _ in cost_paths_with_ids.get(end, [])],
#             'path_details': cost_path_details
#         },
#         'earliest_arrival': {
#             'arrival_time': format_time(time_distances.get(end)),
#             'path_nodes': [node for node, _, _ in time_paths_with_ids.get(end, [])],
#             'path_details': time_path_details,
#             'total_travel_time_minutes': total_travel_time_minutes_time
#         }
#     }

#     return JsonResponse(result)





import heapq
import math
from collections import defaultdict
from datetime import datetime, timedelta
from django.http import JsonResponse

# Converts date and time strings into datetime object
def parse_datetime(date_str, time_str):
    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

def format_time(dt_obj):
    if dt_obj is None or dt_obj == float('inf'):
        return "N/A"
    return dt_obj.strftime("%Y-%m-%d %H:%M")

def dijkstra(graph, start_node, end_node=None, weight_type='cost'):
    distances = defaultdict(lambda: float('inf'))
    distances[start_node] = 0
    paths = defaultdict(list)
    paths[start_node] = [(start_node, 0, None)]  # (node, cumulative_cost, flight_id)

    priority_queue = [(0, start_node)]

    while priority_queue:
        current_cost, current_node = heapq.heappop(priority_queue)

        if current_cost > distances[current_node]:
            continue

        if end_node and current_node == end_node:
            break

        for flight in graph.get(current_node, []):
            neighbor = flight['destination']
            cost = flight.get('cost')
            flight_id = flight.get('id')

            if weight_type == 'cost':
                new_cost = current_cost + cost
            elif weight_type == 'duration':
                duration = flight['duration']
                new_cost = current_cost + duration
            else:
                raise ValueError(f"Invalid weight_type: {weight_type}")

            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                new_path = list(paths[current_node])
                new_path.append((neighbor, new_cost, flight_id))
                paths[neighbor] = new_path
                heapq.heappush(priority_queue, (new_cost, neighbor))

    if end_node:
        return {end_node: distances[end_node]}, {end_node: paths[end_node]}
    else:
        return distances, paths

def dijkstra_with_time(graph, start_node, end_node=None):
    arrival_times = defaultdict(lambda: datetime.max)
    paths = defaultdict(list)
    
    first_flights = graph.get(start_node, [])
    if not first_flights:
        return {}, {}
    journey_start = min(parse_datetime(f['date'], f['start_time']) for f in first_flights)

    paths[start_node] = [(start_node, journey_start, None)]  # (node, arrival_time, flight_id)

    arrival_times[start_node] = journey_start

    priority_queue = [(journey_start, start_node)]

    while priority_queue:
        current_arrival_time, current_node = heapq.heappop(priority_queue)

        if current_arrival_time > arrival_times[current_node]:
            continue

        if end_node and current_node == end_node:
            break

        for flight in graph.get(current_node, []):
            neighbor = flight['destination']
            departure_datetime = parse_datetime(flight['date'], flight['start_time'])
            duration_minutes = flight['duration']
            arrival_datetime = departure_datetime + timedelta(minutes=duration_minutes)
            flight_id = flight.get('id')

            layover_duration = flight.get('layover_duration') or 0
            earliest_departure_time = current_arrival_time + timedelta(minutes=layover_duration)

            can_take_flight = departure_datetime >= earliest_departure_time

            if can_take_flight and arrival_datetime < arrival_times[neighbor]:
                arrival_times[neighbor] = arrival_datetime
                new_path = list(paths[current_node])
                new_path.append((neighbor, arrival_datetime, flight_id))
                paths[neighbor] = new_path
                heapq.heappush(priority_queue, (arrival_datetime, neighbor))

    if end_node:
        return {end_node: arrival_times[end_node]}, {end_node: paths[end_node]}
    else:
        return arrival_times, paths

def convert_to_graph_structure(flight_data):
    graph = defaultdict(list)
    for flight in flight_data:
        origin = flight['origin']
        destination = flight['dest']
        duration = flight['air_time']
        cost = flight['flight_cost']
        date = f"{flight['year']}-{int(flight['month']):02d}-{int(flight['day']):02d}"
        start_hour = int(flight['hour'])
        start_minute = int(flight['minute'])
        start_time = f"{start_hour:02d}:{start_minute:02d}"
        
        arr_time = int(flight['arr_time'])
        arr_hour = arr_time // 100
        arr_minute = arr_time % 100
        reach_time = f"{arr_hour:02d}:{arr_minute:02d}"
        airline = flight['airline_name']
        distance = flight['distance']
        sch_dep_time = flight['sched_dep_time']
        sch_arr_time = flight['sched_arr_time']
        id = flight['id']

        graph[origin].append({
            'destination': destination,
            'duration': duration,
            'cost': cost,
            'layover': None,
            'start_time': start_time,
            'reach_time': reach_time,
            'date': date,
            'name': airline,
            'distance': distance,
            'dep_time': sch_dep_time,
            'arr_time': sch_arr_time,
            'id': id,
        })
    return graph

from .utils import load_flight_data

def find_shortest_route(request):
    converted_flight_data = load_flight_data()
    graph_with_times = convert_to_graph_structure(converted_flight_data)

    start = 'LGA'
    end = 'ATL'
    
    cost_distances, cost_paths_with_ids = dijkstra(graph_with_times, start, end_node=end, weight_type='cost')
    time_distances, time_paths_with_ids = dijkstra_with_time(graph_with_times, start, end_node=end)

    def get_flight_details(flight_id):
        for flight in converted_flight_data:
            if flight['id'] == flight_id:
                return flight
        return None

    # --- Cost path ---
    cost_path_details = []
    cost_path_with_ids = cost_paths_with_ids.get(end, [])
    for _, _, flight_id in cost_path_with_ids[1:]:
        flight_detail = get_flight_details(flight_id)
        if flight_detail:
            cost_path_details.append(flight_detail)

    # --- Time path ---
    time_path_details = []
    time_path_with_ids = time_paths_with_ids.get(end, [])
    first_departure_time = None
    last_arrival_time = None

    for i, (_, arrival_time, flight_id) in enumerate(time_path_with_ids[1:]):
        flight_detail = get_flight_details(flight_id)
        if flight_detail:
            time_path_details.append(flight_detail)
            dep_date = f"{flight_detail['year']}-{int(flight_detail['month']):02d}-{int(flight_detail['day']):02d}"
            dep_time = f"{int(flight_detail['hour']):02d}:{int(flight_detail['minute']):02d}"
            arr_time = f"{int(flight_detail['arr_time']) // 100:02d}:{int(flight_detail['arr_time']) % 100:02d}"

            if i == 0:
                first_departure_time = parse_datetime(dep_date, dep_time)
            last_arrival_time = parse_datetime(dep_date, arr_time) + timedelta(minutes=flight_detail['air_time'])

    total_travel_time_minutes_time = int((last_arrival_time - first_departure_time).total_seconds() // 60) if first_departure_time and last_arrival_time else None

    # --- Balanced path ---
    def dijkstra_balanced(graph, start_node, end_node, min_cost, max_cost, min_dur, max_dur):
        distances = defaultdict(lambda: float('inf'))
        distances[start_node] = 0
        paths = defaultdict(list)
        paths[start_node] = [(start_node, 0, None)]
        queue = [(0, start_node)]

        while queue:
            score, node = heapq.heappop(queue)
            if score > distances[node]:
                continue
            if node == end_node:
                break
            for flight in graph[node]:
                neighbor = flight['destination']
                cost = flight['cost']
                duration = flight['duration']
                flight_id = flight['id']
                norm_cost = (cost - min_cost) / (max_cost - min_cost) if max_cost > min_cost else 0
                norm_dur = (duration - min_dur) / (max_dur - min_dur) if max_dur > min_dur else 0
                weight = 0.5 * norm_cost + 0.5 * norm_dur
                total = score + weight
                if total < distances[neighbor]:
                    distances[neighbor] = total
                    new_path = list(paths[node])
                    new_path.append((neighbor, total, flight_id))
                    paths[neighbor] = new_path
                    heapq.heappush(queue, (total, neighbor))
        return distances, paths

    all_costs = [f['cost'] for flights in graph_with_times.values() for f in flights]
    all_durations = [f['duration'] for flights in graph_with_times.values() for f in flights]
    min_cost_val = min(all_costs) if all_costs else 0
    max_cost_val = max(all_costs) if all_costs else 0
    min_dur_val = min(all_durations) if all_durations else 0
    max_dur_val = max(all_durations) if all_durations else 0

    bal_distances, bal_paths = dijkstra_balanced(graph_with_times, start, end, min_cost_val, max_cost_val, min_dur_val, max_dur_val)
    bal_path_details = []
    bal_path_with_ids = bal_paths.get(end, [])
    bal_first_time = None
    bal_last_time = None

    for i, (_, _, flight_id) in enumerate(bal_path_with_ids[1:]):
        flight_detail = get_flight_details(flight_id)
        if flight_detail:
            bal_path_details.append(flight_detail)
            dep_date = f"{flight_detail['year']}-{int(flight_detail['month']):02d}-{int(flight_detail['day']):02d}"
            dep_time = f"{int(flight_detail['hour']):02d}:{int(flight_detail['minute']):02d}"
            arr_time = f"{int(flight_detail['arr_time']) // 100:02d}:{int(flight_detail['arr_time']) % 100:02d}"
            if i == 0:
                bal_first_time = parse_datetime(dep_date, dep_time)
            bal_last_time = parse_datetime(dep_date, arr_time) + timedelta(minutes=flight_detail['air_time'])

    total_bal_minutes = int((bal_last_time - bal_first_time).total_seconds() // 60) if bal_first_time and bal_last_time else None

    result = {
        'minimum_cost': {
            'cost': cost_distances.get(end),
            'path_nodes': [node for node, _, _ in cost_paths_with_ids.get(end, [])],
            'path_details': cost_path_details
        },
        'earliest_arrival': {
            'arrival_time': format_time(time_distances.get(end)),
            'path_nodes': [node for node, _, _ in time_paths_with_ids.get(end, [])],
            'path_details': time_path_details,
            'total_travel_time_minutes': total_travel_time_minutes_time
        },
        'balanced': {
            'score': round(bal_distances.get(end), 3),
            'path_nodes': [node for node, _, _ in bal_paths.get(end, [])],
            'path_details': bal_path_details,
            'total_travel_time_minutes': total_bal_minutes
        }
    }

    return JsonResponse(result)