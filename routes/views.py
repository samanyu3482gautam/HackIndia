



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

    start = "JFK"
    end = "LAX"

    if not start or not end:
        return JsonResponse({'error': 'Missing start or end'}, status=400)

    
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

from django.shortcuts import render



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # Important!
import json

# ... (your existing imports and functions)

@csrf_exempt  # **Use with caution in production!**
def process_flight_results(request):
    if request.method == 'POST':
        try:
            results = json.loads(request.body)  # Parse the JSON data
            print("Received flight results from frontend:", results)

            # ***YOUR DJANGO LOGIC HERE:***
            # - Process the results (e.g., store in the database,
            #   perform further calculations)
            processed_data = process_the_flight_results(results)

            return JsonResponse({'message': 'Results received and processed', 'processed_data': processed_data})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests allowed'}, status=405)

def process_the_flight_results(results):
    # Process the flight results here
    # Example:
    processed_minimum_cost = results['minimum_cost']
    processed_minimum_cost['cost'] *= 1.1 # Add a tax
    return {'processed_minimum_cost': processed_minimum_cost}

def get_processed_data(request):
    # Here you would retrieve the processed data (e.g., from a database)
    # and send it back to the frontend
    processed_data_from_db = {
        'processed_minimum_cost': {
            'cost': 1234,
            'path_nodes': ['A', 'B', 'C']
        }
    }
    return JsonResponse(processed_data_from_db)


from django.shortcuts import render
def search_flights(request):
    context = {}
    if request.method == 'POST':
        start = request.POST.get('start', '').upper()
        end = request.POST.get('end', '').upper()
        priority = request.POST.get('priority')

        if not start or not end:
            context['no_results'] = True
            return render(request, 'search.html', context)

        converted_flight_data = load_flight_data()
        graph_with_times = convert_to_graph_structure(converted_flight_data)

        def get_flight_by_id(fid):
            for f in converted_flight_data:
                if f['id'] == fid:
                    return f
            return None

        path = []
        if priority == 'time':
            _, path = dijkstra_with_time(graph_with_times, start, end_node=end)
        elif priority == 'cost':
            _, path = dijkstra(graph_with_times, start, end_node=end, weight_type='cost')
        elif priority == 'balanced':
            all_costs = [f['cost'] for flights in graph_with_times.values() for f in flights]
            all_durations = [f['duration'] for flights in graph_with_times.values() for f in flights]
            min_cost = min(all_costs) if all_costs else 0
            max_cost = max(all_costs) if all_costs else 0
            min_dur = min(all_durations) if all_durations else 0
            max_dur = max(all_durations) if all_durations else 0

            def dijkstra_balanced(graph, start_node, end_node):
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

            _, path = dijkstra_balanced(graph_with_times, start, end)

        flight_ids = [fid for _, _, fid in path.get(end, [])[1:]]
        flights = [get_flight_by_id(fid) for fid in flight_ids if fid is not None]

        if flights:
            for f in flights:
                f['formatted_dep_time'] = f"{f['hour']:02d}:{f['minute']:02d}"
                dep_datetime = datetime(
                    int(f['year']), int(f['month']), int(f['day']),
                    int(f['hour']), int(f['minute'])
                )
                arr_datetime = dep_datetime + timedelta(minutes=f['air_time'])
                f['formatted_arr_time'] = arr_datetime.strftime("%H:%M")


            context['flights'] = flights
        else:
            context['no_results'] = True

    return render(request, 'search.html', context)


def payment_page(request):
    return render(request,'payment.html')
