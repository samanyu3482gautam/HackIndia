# import heapq
# import math
# from collections import defaultdict
# from datetime import datetime, timedelta
# from django.http import JsonResponse, HttpResponseBadRequest
# from .utils import load_flight_data
# from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import render, redirect
# from django.contrib import messages
# import networkx as nx

# # Converts date and time strings into datetime object
# def parse_datetime(date_str, time_str):
#     return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

# def format_time(dt_obj):
#     if dt_obj is None or dt_obj == float('inf'):
#         return "N/A"
#     return dt_obj.strftime("%Y-%m-%d %H:%M")

# def format_duration(minutes):
#     if minutes is None:
#         return "N/A"
#     hours = minutes // 60
#     remaining_minutes = minutes % 60
#     return f"{hours:02d}:{remaining_minutes:02d}"
# import networkx as nx

# def create_networkx_graph(flight_data):
#     graph = nx.DiGraph()
#     for flight in flight_data:
#         origin = flight['origin']
#         destination = flight['dest']
#         cost = flight['flight_cost']
#         duration = flight['air_time']
#         graph.add_edge(origin, destination, flight_data=flight, cost=cost, duration=duration)
#         if origin not in graph:
#             graph.add_node(origin)
#         if destination not in graph:
#             graph.add_node(destination)
#     return graph

# def dijkstra(graph, start_node, end_node=None, weight_type='cost'):
#     distances = defaultdict(lambda: float('inf'))
#     distances[start_node] = 0
#     paths = defaultdict(list)
#     paths[start_node] = [(start_node, 0, None)]  # (node, cumulative_weight, flight_id)

#     priority_queue = [(0, start_node)]

#     while priority_queue:
#         current_weight, current_node = heapq.heappop(priority_queue)

#         if current_weight > distances[current_node]:
#             continue

#         if end_node and current_node == end_node:
#             break

#         for flight in graph.get(current_node, []):
#             neighbor = flight['destination']
#             cost = flight.get('cost')
#             duration = flight.get('duration')
#             flight_id = flight.get('id')

#             if weight_type == 'cost':
#                 new_weight = current_weight + cost
#             elif weight_type == 'duration':
#                 new_weight = current_weight + duration
#             elif weight_type == 'balanced':
#                 # This will be handled in the balanced Dijkstra function
#                 raise ValueError("Use dijkstra_balanced for balanced weight_type")
#             else:
#                 raise ValueError(f"Invalid weight_type: {weight_type}")

#             if new_weight < distances[neighbor]:
#                 distances[neighbor] = new_weight
#                 new_path = list(paths[current_node])
#                 new_path.append((neighbor, new_weight, flight_id))
#                 paths[neighbor] = new_path
#                 heapq.heappush(priority_queue, (new_weight, neighbor))

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

# def dijkstra_balanced(graph, start_node, end_node, min_cost, max_cost, min_duration, max_duration):
#     distances = defaultdict(lambda: float('inf'))
#     distances[start_node] = 0
#     paths = defaultdict(list)
#     paths[start_node] = [(start_node, 0, None)]  # (node, cumulative_score, flight_id)

#     priority_queue = [(0, start_node)]

#     while priority_queue:
#         current_score, current_node = heapq.heappop(priority_queue)

#         if current_score > distances[current_node]:
#             continue

#         if end_node and current_node == end_node:
#             break

#         for flight in graph.get(current_node, []):
#             neighbor = flight['destination']
#             cost = flight.get('cost')
#             duration = flight.get('duration')
#             flight_id = flight.get('id')

#             # Normalize cost and duration (scaling to 0-1)
#             normalized_cost = (cost - min_cost) / (max_cost - min_cost) if max_cost > min_cost else 0
#             normalized_duration = (duration - min_duration) / (max_duration - min_duration) if max_duration > min_duration else 0

#             # Combine normalized cost and duration (you can adjust the weights)
#             balanced_score = (normalized_cost + normalized_duration) / 2  # Simple average

#             new_score = current_score + balanced_score

#             if new_score < distances[neighbor]:
#                 distances[neighbor] = new_score
#                 new_path = list(paths[current_node])
#                 new_path.append((neighbor, new_score, flight_id))
#                 paths[neighbor] = new_path
#                 heapq.heappush(priority_queue, (new_score, neighbor))

#     if end_node:
#         return {end_node: distances[end_node]}, {end_node: paths[end_node]}
#     else:
#         return distances, paths

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



# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse

# # @csrf_exempt
# # def find_shortest_route(request):
# #     start = request.GET.get('start', '').upper()
# #     end = request.GET.get('end', '').upper()

# #     if not start or not end:
# #         return JsonResponse({'error': 'Missing start or end parameter'}, status=400)

# #     converted_flight_data = load_flight_data()
# #     graph_with_times = convert_to_graph_structure(converted_flight_data)

# #     all_costs = [flight['cost'] for flights in graph_with_times.values() for flight in flights]
# #     all_durations = [flight['duration'] for flights in graph_with_times.values() for flight in flights]

# #     min_cost = min(all_costs) if all_costs else 0
# #     max_cost = max(all_costs) if all_costs else 0
# #     min_duration = min(all_durations) if all_durations else 0
# #     max_duration = max(all_durations) if all_durations else 0

# #     cost_distances, cost_paths_with_ids = dijkstra(graph_with_times, start, end_node=end, weight_type='cost')
# #     time_distances, time_paths_with_ids = dijkstra_with_time(graph_with_times, start, end_node=end)
# #     balanced_distances, balanced_paths_with_ids = dijkstra_balanced(
# #         graph_with_times, start, end, min_cost, max_cost, min_duration, max_duration
# #     )

# #     def get_flight_details(flight_id):
# #         for flight in converted_flight_data:
# #             if flight['id'] == flight_id:
# #                 return flight
# #         return None

# #     def get_path_details(paths_with_ids):
# #         path_details = []
# #         path_with_ids = paths_with_ids.get(end, [])
# #         for _, _, flight_id in path_with_ids[1:]:
# #             flight_detail = get_flight_details(flight_id)
# #             if flight_detail:
# #                 path_details.append(flight_detail)
# #         return path_details

# #     cost_path_details = get_path_details(cost_paths_with_ids)
# #     time_path_details = get_path_details(time_paths_with_ids)
# #     balanced_path_details = get_path_details(balanced_paths_with_ids)

# #     def calculate_total_travel_time(path_details):
# #         if not path_details:
# #             return None
# #         if len(path_details) == 1:
# #             return path_details[0]['air_time']
# #         else:
# #             first_flight = path_details[0]
# #             first_departure_datetime = parse_datetime(
# #                 f"{first_flight['year']}-{int(first_flight['month']):02d}-{int(first_flight['day']):02d}",
# #                 f"{int(first_flight['hour']):02d}:{int(first_flight['minute']):02d}"
# #             )

# #             last_flight = path_details[-1]
# #             arrival_datetime_last_segment = parse_datetime(
# #                 f"{last_flight['year']}-{int(last_flight['month']):02d}-{int(last_flight['day']):02d}",
# #                 f"{int(last_flight['arr_time']) // 100:02d}:{int(last_flight['arr_time']) % 100:02d}"
# #             )
# #             last_arrival_datetime = arrival_datetime_last_segment + timedelta(minutes=last_flight['air_time'])

# #             total_minutes = int((last_arrival_datetime - first_departure_datetime).total_seconds() // 60)
# #             return total_minutes

# #     total_travel_time_cost_minutes = calculate_total_travel_time(cost_path_details)
# #     total_travel_time_time_minutes = calculate_total_travel_time(time_path_details)
# #     total_travel_time_balanced_minutes = calculate_total_travel_time(balanced_path_details)

# #     result = {
# #         'cheapest': {
# #             'cost': cost_distances.get(end),
# #             'path_nodes': [node for node, _, _ in cost_paths_with_ids.get(end, [])],
# #             'path_details': cost_path_details,
# #             'total_travel_time': format_duration(total_travel_time_cost_minutes),
# #         },
# #         'fastest': {
# #             'arrival_time': format_time(time_distances.get(end)),
# #             'path_nodes': [node for node, _, _ in time_paths_with_ids.get(end, [])],
# #             'path_details': time_path_details,
# #             'total_travel_time': format_duration(total_travel_time_time_minutes),
# #         },
# #         'best_value': {
# #             'score': balanced_distances.get(end),
# #             'path_nodes': [node for node, _, _ in balanced_paths_with_ids.get(end, [])],
# #             'path_details': balanced_path_details,
# #             'total_travel_time': format_duration(total_travel_time_balanced_minutes),
# #         }
# #     }

# #     return JsonResponse(result)
# @csrf_exempt
# def find_shortest_route(request):
#     if request.method != 'GET':
#         return HttpResponseBadRequest("Only GET requests are allowed")

#     start = request.GET.get('start', '').upper()
#     end = request.GET.get('end', '').upper()

#     print(f"DEBUG: find_shortest_route called with start='{start}', end='{end}'")  # VERY IMPORTANT

#     if not start or not end:
#         return JsonResponse({'error': 'Missing start or end parameter'}, status=400)

#     converted_flight_data = load_flight_data()
#     graph_with_times = convert_to_graph_structure(converted_flight_data)

#     # ... (rest of your find_shortest_route logic)

#     result = {
#         # ... (your result data)
#     }

#     print(f"DEBUG: find_shortest_route result: {result}")  # VERY IMPORTANT
#     return JsonResponse(result)


# def search_flights(request):
#     if request.method == 'GET':
#         return render(request, 'search.html')
#     elif request.method == 'POST':
#         start = request.POST.get('start')
#         end = request.POST.get('end')

#         print(f"DEBUG: search_flights (POST) start='{start}', end='{end}'")  # VERY IMPORTANT

#         if not start or not end:
#             messages.error(request, "Both Departure and Destination are required.")
#             return redirect('search_flights')

#         return redirect(f'/find_route/?start={start.upper()}&end={end.upper()}')






# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.contrib.auth import authenticate,login,logout


# def search_flights(request):
#     if request.method == 'GET':
#         return render(request, 'search.html')
#     elif request.method == 'POST':
#         start = request.POST.get('start')
#         end = request.POST.get('end')
#         if start and end:
#             # Directly call find_shortest_route and return its response
#             return find_shortest_route(request)  # Assuming find_shortest_route handles the request object
#         else:
#             messages.error(request, "Both start and end must be provided.")
#             return redirect('search_flights')





# import heapq
# import math
# from collections import defaultdict
# from datetime import datetime, timedelta
# from django.http import JsonResponse, HttpResponseBadRequest
# from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import render, redirect
# from django.contrib import messages
# import networkx as nx

# # Converts date and time strings into datetime object
# def parse_datetime(date_str, time_str):
#     return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

# def format_time(dt_obj):
#     if dt_obj is None or dt_obj == float('inf'):
#         return "N/A"
#     return dt_obj.strftime("%Y-%m-%d %H:%M")

# def format_duration(minutes):
#     if minutes is None:
#         return "N/A"
#     hours = minutes // 60
#     remaining_minutes = minutes % 60
#     return f"{hours:02d}:{remaining_minutes:02d}"

# def dijkstra(graph, start_node, end_node=None, weight_type='cost'):
#     distances = defaultdict(lambda: float('inf'))
#     distances[start_node] = 0
#     paths = defaultdict(list)
#     paths[start_node] = [(start_node, 0, None)]  # (node, cumulative_weight, flight_id)

#     priority_queue = [(0, start_node)]

#     while priority_queue:
#         current_weight, current_node = heapq.heappop(priority_queue)

#         if current_weight > distances[current_node]:
#             continue

#         if end_node and current_node == end_node:
#             break

#         for neighbor, flight_data in graph.get(current_node, {}).items(): # Changed
#             cost = flight_data.get('cost')
#             duration = flight_data.get('duration')
#             flight_id = flight_data.get('id')

#             if weight_type == 'cost':
#                 new_weight = current_weight + cost
#             elif weight_type == 'duration':
#                 new_weight = current_weight + duration
#             elif weight_type == 'balanced':
#                 # This will be handled in the balanced Dijkstra function
#                 raise ValueError("Use dijkstra_balanced for balanced weight_type")
#             else:
#                 raise ValueError(f"Invalid weight_type: {weight_type}")

#             if new_weight < distances[neighbor]:
#                 distances[neighbor] = new_weight
#                 new_path = list(paths[current_node])
#                 new_path.append((neighbor, new_weight, flight_id))
#                 paths[neighbor] = new_path
#                 heapq.heappush(priority_queue, (new_weight, neighbor))

#         if end_node:
#             return {end_node: distances[end_node]}, {end_node: paths[end_node]}
#         else:
#             return distances, paths

# def dijkstra_with_time(graph, start_node, end_node=None):
#     arrival_times = defaultdict(lambda: datetime.max)
#     paths = defaultdict(list)

#     if start_node not in graph:
#         return {}, {}

#     first_flights = graph[start_node] # changed
#     if not first_flights:
#         return {}, {}
#     journey_start = min(parse_datetime(f['date'], f['start_time']) for f in first_flights.values())

#     paths[start_node] = [(start_node, journey_start, None)]  # (node, arrival_time, flight_id)

#     arrival_times[start_node] = journey_start

#     priority_queue = [(journey_start, start_node)]

#     while priority_queue:
#         current_arrival_time, current_node = heapq.heappop(priority_queue)

#         if current_arrival_time > arrival_times[current_node]:
#             continue

#         if end_node and current_node == end_node:
#             break

#         for neighbor, flight_data in graph.get(current_node, {}).items(): # Changed
#             departure_datetime = parse_datetime(flight_data['date'], flight_data['start_time'])
#             duration_minutes = flight_data['duration']
#             arrival_datetime = departure_datetime + timedelta(minutes=duration_minutes)
#             flight_id = flight_data.get('id')

#             # Layover handling
#             layover_duration = flight_data.get('layover_duration') or 0
#             earliest_departure_time = current_arrival_time + timedelta(minutes=layover_duration)

#             can_take_flight = departure_datetime >= earliest_departure_time

#             if can_take_flight and arrival_datetime < arrival_times[neighbor]:
#                 arrival_times[neighbor] = arrival_datetime
#                 new_path = list(paths[current_node])
#                 new_path.append((neighbor, arrival_datetime, flight_id))
#                 paths[neighbor] = new_path
#                 heapq.heappush(priority_queue, (arrival_datetime, neighbor))

#         if end_node:
#             return {end_node: arrival_times[end_node]}, {end_node: paths[end_node]}
#         else:
#             return arrival_times, paths

# def dijkstra_balanced(graph, start_node, end_node, min_cost, max_cost, min_duration, max_duration):
#     distances = defaultdict(lambda: float('inf'))
#     distances[start_node] = 0
#     paths = defaultdict(list)
#     paths[start_node] = [(start_node, 0, None)]  # (node, cumulative_score, flight_id)
#     priority_queue = [(0, start_node)]

#     while priority_queue:
#         current_score, current_node = heapq.heappop(priority_queue)

#         if current_score > distances[current_node]:
#             continue

#         if end_node and current_node == end_node:
#             break

#         for neighbor, flight_data in graph.get(current_node, {}).items(): #changed
#             cost = flight_data.get('cost')
#             duration = flight_data.get('duration')
#             flight_id = flight_data.get('id')

#             # Normalize cost and duration (scaling to 0-1)
#             normalized_cost = (cost - min_cost) / (max_cost - min_cost) if max_cost > min_cost else 0
#             normalized_duration = (duration - min_duration) / (max_duration - min_duration) if max_duration > min_duration else 0

#             # Simple weighted average (you can adjust weights)
#             score = 0.6 * normalized_cost + 0.4 * normalized_duration
#             new_score = current_score + score

#             if new_score < distances[neighbor]:
#                 distances[neighbor] = new_score
#                 new_path = list(paths[current_node])
#                 new_path.append((neighbor, new_score, flight_id))
#                 paths[neighbor] = new_path
#                 heapq.heappush(priority_queue, (new_score, neighbor))

#         if end_node:
#             return {end_node: distances[end_node]}, {end_node: paths[end_node]}
#         else:
#             return distances, paths

# def convert_to_graph_structure(flight_data):
#     graph = defaultdict(dict) # Changed to default dict of dict
#     for flight in flight_data:
#         origin = flight['origin']
#         destination = flight['dest']
#         date = f"{flight['year']}-{flight['month']:02d}-{flight['day']:02d}"
#         start_time = f"{flight['hour']:02d}:{flight['minute']:02d}"
#         duration = flight['air_time']
#         cost = flight['flight_cost']
#         flight_id = flight['id']
#         airline = flight['airline_name']
#         flight_number = flight['flight_number']

#         if origin not in graph:
#             graph[origin] = {}
#         graph[origin][destination] = { # Changed the structure.
#             'date': date,
#             'start_time': start_time,
#             'duration': duration,
#             'cost': cost,
#             'id': flight_id,
#             'airline': airline,
#             'flight_number': flight_number,
#         }
#     return graph

# from .utils import load_flight_data
# def find_shortest_route(request):
#     if request.method != 'GET':
#         return HttpResponseBadRequest("Only GET requests are allowed")

#     start = 'JFK'  # Hardcoded start
#     end = 'LAX'    # Hardcoded end

#     print(f"DEBUG: find_shortest_route called with start='{start}', end='{end}'")

#     converted_flight_data = load_flight_data()
#     graph_with_times = convert_to_graph_structure(converted_flight_data)

    


#     # Basic Dijkstra for cost and time
#     cost_distances, cost_paths_with_ids = dijkstra(graph_with_times, start, end)
#     time_distances, time_paths_with_ids = dijkstra_with_time(graph_with_times, start, end)

#     # Balanced Dijkstra setup
#     all_costs = [flight['cost'] for flight_data in graph_with_times.values() for flight in flight_data.values()] # changed
#     all_durations = [flight['duration'] for flight_data in graph_with_times.values() for flight in flight_data.values()] # changed

#     min_cost = min(all_costs) if all_costs else 0
#     max_cost = max(all_costs) if all_costs else 0
#     min_duration = min(all_durations) if all_durations else 0
#     max_duration = max(all_durations) if all_durations else 0

#     balanced_distances, balanced_paths_with_ids = dijkstra_balanced(
#         graph_with_times, start, end, min_cost, max_cost, min_duration, max_duration
#     )

#     def get_path_details(paths_with_ids, graph):
#         path_details = []
#         if end in paths_with_ids:
#             path = paths_with_ids[end]
#             for i in range(len(path) - 1):
#                 current_node, _, _ = path[i]
#                 next_node, _, _ = path[i + 1]
#                 if current_node in graph and next_node in graph[current_node]: # added check
#                     path_details.append(graph[current_node][next_node])
                
#             return path_details

#     cost_path_details = get_path_details(cost_paths_with_ids, graph_with_times)
#     time_path_details = get_path_details(time_paths_with_ids, graph_with_times)
#     balanced_path_details = get_path_details(balanced_paths_with_ids, graph_with_times)

#     # Calculate total travel times
#     def calculate_total_travel_time(path_details):
#         if not path_details:
#             return 0
#         total_minutes = 0
#         for flight in path_details:
#             total_minutes += flight['duration']
#         return total_minutes

#     total_travel_time_cost_minutes = calculate_total_travel_time(cost_path_details)
#     total_travel_time_time_minutes = calculate_total_travel_time(time_path_details)
#     total_travel_time_balanced_minutes = calculate_total_travel_time(balanced_path_details)

#     result = {
#         'cheapest': {
#             'cost': cost_distances.get(end),
#             'path_nodes': [node for node, _, _ in cost_paths_with_ids.get(end, [])],
#             'path_details': cost_path_details,
#             'total_travel_time': format_duration(total_travel_time_cost_minutes),
#         },
#         'fastest': {
#             'arrival_time': format_time(time_distances.get(end)),
#             'path_nodes': [node for node, _, _ in time_paths_with_ids.get(end, [])],
#             'path_details': time_path_details,
#             'total_travel_time': format_duration(total_travel_time_time_minutes),
#         },
#         'best_value': {
#             'score': balanced_distances.get(end),
#             'path_nodes': [node for node, _, _ in balanced_paths_with_ids.get(end, [])],
#             'path_details': balanced_path_details,
#             'total_travel_time': format_duration(total_travel_time_balanced_minutes),
#         }
#     }

#     print(f"DEBUG: find_shortest_route result: {result}")
#     return JsonResponse(result)


import heapq
import math
from collections import defaultdict
from datetime import datetime, timedelta
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib import messages
import networkx as nx

# Converts date and time strings into datetime object
def parse_datetime(date_str, time_str):
    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")

def format_time(dt_obj):
    if dt_obj is None or dt_obj == float('inf'):
        return "N/A"
    return dt_obj.strftime("%Y-%m-%d %H:%M")

def format_duration(minutes):
    if minutes is None:
        return "N/A"
    hours = minutes // 60
    remaining_minutes = minutes % 60
    return f"{hours:02d}:{remaining_minutes:02d}"

def dijkstra(graph, start_node, end_node=None, weight_type='cost'):
    distances = defaultdict(lambda: float('inf'))
    distances[start_node] = 0
    paths = defaultdict(list)
    paths[start_node] = [(start_node, 0, None)]  # (node, cumulative_weight, flight_id)

    priority_queue = [(0, start_node)]

    while priority_queue:
        current_weight, current_node = heapq.heappop(priority_queue)

        if current_weight > distances[current_node]:
            continue

        if end_node and current_node == end_node:
            break

        for neighbor, flight_data in graph.get(current_node, {}).items(): # Changed
            cost = flight_data.get('cost')
            duration = flight_data.get('duration')
            flight_id = flight_data.get('id')

            if weight_type == 'cost':
                new_weight = current_weight + cost
            elif weight_type == 'duration':
                new_weight = current_weight + duration
            elif weight_type == 'balanced':
                # This will be handled in the balanced Dijkstra function
                raise ValueError("Use dijkstra_balanced for balanced weight_type")
            else:
                raise ValueError(f"Invalid weight_type: {weight_type}")

            if new_weight < distances[neighbor]:
                distances[neighbor] = new_weight
                new_path = list(paths[current_node])
                new_path.append((neighbor, new_weight, flight_id))
                paths[neighbor] = new_path
                heapq.heappush(priority_queue, (new_weight, neighbor))

        if end_node:
            return {end_node: distances[end_node]}, {end_node: paths[end_node]}
        else:
            return distances, paths

def dijkstra_with_time(graph, start_node, end_node=None):
    arrival_times = defaultdict(lambda: datetime.max)
    paths = defaultdict(list)

    if start_node not in graph:
        return {}, {}

    first_flights = graph[start_node] # changed
    if not first_flights:
        return {}, {}
    journey_start = min(parse_datetime(f['date'], f['start_time']) for f in first_flights.values())

    paths[start_node] = [(start_node, journey_start, None)]  # (node, arrival_time, flight_id)

    arrival_times[start_node] = journey_start

    priority_queue = [(journey_start, start_node)]

    while priority_queue:
        current_arrival_time, current_node = heapq.heappop(priority_queue)

        if current_arrival_time > arrival_times[current_node]:
            continue

        if end_node and current_node == end_node:
            break

        for neighbor, flight_data in graph.get(current_node, {}).items(): # Changed
            departure_datetime = parse_datetime(flight_data['date'], flight_data['start_time'])
            duration_minutes = flight_data['duration']
            arrival_datetime = departure_datetime + timedelta(minutes=duration_minutes)
            flight_id = flight_data.get('id')

            # Layover handling
            layover_duration = flight_data.get('layover_duration') or 0
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

def dijkstra_balanced(graph, start_node, end_node, min_cost, max_cost, min_duration, max_duration):
    distances = defaultdict(lambda: float('inf'))
    distances[start_node] = 0
    paths = defaultdict(list)
    paths[start_node] = [(start_node, 0, None)]  # (node, cumulative_score, flight_id)
    priority_queue = [(0, start_node)]

    while priority_queue:
        current_score, current_node = heapq.heappop(priority_queue)

        if current_score > distances[current_node]:
            continue

        if end_node and current_node == end_node:
            break

        for neighbor, flight_data in graph.get(current_node, {}).items(): #changed
            cost = flight_data.get('cost')
            duration = flight_data.get('duration')
            flight_id = flight_data.get('id')

            # Normalize cost and duration (scaling to 0-1)
            normalized_cost = (cost - min_cost) / (max_cost - min_cost) if max_cost > min_cost else 0
            normalized_duration = (duration - min_duration) / (max_duration - min_duration) if max_duration > min_duration else 0

            # Simple weighted average (you can adjust weights)
            score = 0.5 * normalized_cost + 0.5 * normalized_duration # Equal weights for balance
            new_score = current_score + score

            if new_score < distances[neighbor]:
                distances[neighbor] = new_score
                new_path = list(paths[current_node])
                new_path.append((neighbor, new_score, flight_id))
                paths[neighbor] = new_path
                heapq.heappush(priority_queue, (new_score, neighbor))

        if end_node:
            return {end_node: distances[end_node]}, {end_node: paths[end_node]}
        else:
            return distances, paths

def convert_to_graph_structure(flight_data):
    graph = defaultdict(dict) # Changed to default dict of dict
    for flight in flight_data:
        origin = flight['origin']
        destination = flight['dest']
        date = f"{flight['year']}-{flight['month']:02d}-{flight['day']:02d}"
        start_time = f"{flight['hour']:02d}:{flight['minute']:02d}"
        duration = flight['air_time']
        cost = flight['flight_cost']
        flight_id = flight['id']
        airline = flight['airline_name']
        flight_number = flight['flight_number']

        if origin not in graph:
            graph[origin] = {}
        graph[origin][destination] = { # Changed the structure.
            'date': date,
            'start_time': start_time,
            'duration': duration,
            'cost': cost,
            'id': flight_id,
            'airline': airline,
            'flight_number': flight_number,
        }
    return graph

from .utils import load_flight_data
def find_shortest_route(request):
    if request.method != 'GET':
        return HttpResponseBadRequest("Only GET requests are allowed")

    start = 'LGA'  # Hardcoded start
    end = 'IAD'    # Hardcoded end

    print(f"DEBUG: find_shortest_route called with start='{start}', end='{end}'")

    converted_flight_data = load_flight_data()
    graph_with_times = convert_to_graph_structure(converted_flight_data)


    # Basic Dijkstra for cost and time
    cost_distances, cost_paths_with_ids = dijkstra(graph_with_times, start, end)
    time_distances, time_paths_with_ids = dijkstra_with_time(graph_with_times, start, end)

    # Balanced Dijkstra setup
    all_costs = [flight['cost'] for flight_data in graph_with_times.values() for flight in flight_data.values()] # changed
    all_durations = [flight['duration'] for flight_data in graph_with_times.values() for flight in flight_data.values()] # changed

    min_cost = min(all_costs) if all_costs else 0
    max_cost = max(all_costs) if all_costs else 0
    min_duration = min(all_durations) if all_durations else 0
    max_duration = max(all_durations) if all_durations else 0

    balanced_distances, balanced_paths_with_ids = dijkstra_balanced(
        graph_with_times, start, end, min_cost, max_cost, min_duration, max_duration
    )

    def get_path_details(paths_with_ids, graph):
        path_details = []
        if end in paths_with_ids:
            path = paths_with_ids[end]
            for i in range(len(path) - 1):
                current_node, _, _ = path[i]
                next_node, _, _ = path[i + 1]
                if current_node in graph and next_node in graph[current_node]: # added check
                    path_details.append(graph[current_node][next_node])

            return path_details

    cost_path_details = get_path_details(cost_paths_with_ids, graph_with_times)
    time_path_details = get_path_details(time_paths_with_ids, graph_with_times)
    balanced_path_details = get_path_details(balanced_paths_with_ids, graph_with_times)

    # Calculate total travel times
    def calculate_total_travel_time(path_details):
        if not path_details:
            return 0
        total_minutes = 0
        for flight in path_details:
            total_minutes += flight['duration']
        return total_minutes

    total_travel_time_cost_minutes = calculate_total_travel_time(cost_path_details)
    total_travel_time_time_minutes = calculate_total_travel_time(time_path_details)
    total_travel_time_balanced_minutes = calculate_total_travel_time(balanced_path_details)

    result = {
        'cheapest': {
            'cost': cost_distances.get(end),
            'path_nodes': [node for node, _, _ in cost_paths_with_ids.get(end, [])],
            'path_details': cost_path_details,
            'total_travel_time': format_duration(total_travel_time_cost_minutes),
        },
        'fastest': {
            'arrival_time': format_time(time_distances.get(end)),
            'path_nodes': [node for node, _, _ in time_paths_with_ids.get(end, [])],
            'path_details': time_path_details,
            'total_travel_time': format_duration(total_travel_time_time_minutes),
        },
        'best_value': {
            'score': balanced_distances.get(end),
            'path_nodes': [node for node, _, _ in balanced_paths_with_ids.get(end, [])],
            'path_details': balanced_path_details,
            'total_travel_time': format_duration(total_travel_time_balanced_minutes),
        }
    }

    print(f"DEBUG: find_shortest_route result: {result}")
    return JsonResponse(result)