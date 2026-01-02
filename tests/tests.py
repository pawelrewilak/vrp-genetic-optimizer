import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from typing import List
import random
import time
import csv
from algorithm import run_evolution, School, Graph

def generate_random_instance(num_schools: int, map_size: int = 600, seed: int = None) -> List[School]:
    """Generuje listę losowych szkół dla zadanej liczby punktów."""
    if seed is not None:
        random.seed(seed)
    
    schools = []
    depot = School(id=0, x=map_size/2, y=30, profit=0, service_time=0, 
                   time_window_start=0, time_window_end=1000)
    schools.append(depot)

    for i in range(1, num_schools + 1):

        x = random.randint(10, map_size - 10)
        y = random.randint(10, map_size - 10)

        profit = random.randint(300, 1000)
        t_start = random.randint(0, 300)
        duration = random.randint(60, 240)
        t_end = min(t_start + duration, 480)
        service_time_factor = random.uniform(0.2, 0.4)
        service_time = int((t_end - t_start) * service_time_factor)
        
        s = School(
            id=i,
            x=x, y=y,
            profit=profit,
            service_time=service_time,
            time_window_start=t_start,
            time_window_end=t_end
        )
        schools.append(s)
        
    return schools


def main_benchmark(num_trials=1, output_file='benchmark_results.csv'):

    basic_configs = [
         # Grupa kontrolna - test ktory pojedyńczy oprator działa najlepiej
        {'mut' : 'swap', 'rates': [0.15, 0.25, 0.10, 0.05, 1.0], 'crs': 'order', 'config_name': 'swap_0.15_ord'},
        {'mut' : 'inv', 'rates': [0.15, 0.25, 0.10, 0.05, 1.0], 'crs': 'order', 'config_name': 'inv_0.25_ord'},
        {'mut' : 'ins', 'rates': [0.15, 0.25, 0.10, 0.05, 1.0], 'crs': 'order', 'config_name': 'ins_0.1_ord'},
        {'mut' : 'scr', 'rates': [0.15, 0.25, 0.10, 0.05, 1.0], 'crs': 'order', 'config_name': 'scr_0.05_ord'},
        {'mut' : 'hybrid', 'rates': [0.15, 0.25, 0.10, 0.05, 1.0], 'crs': 'order', 'config_name': 'hybrid_ord'}
    ]

    advanced_configs = [
        # 1. Sprawdzenie krzyżowania ERX (często lepsze dla tras)
        {'mut': 'hybrid', 'rates': [0.15, 0.25, 0.10, 0.05, 1.0], 'crs': 'erx', 'config_name': 'hybrid_ERX'},
        # 2. Wersja "Agresywna" (podwojone szanse)
        {'mut': 'hybrid', 'rates': [0.30, 0.50, 0.20, 0.10, 1.0], 'crs': 'order', 'config_name': 'hybrid_Aggressive'},
        # 3. Wersja "Stabilna" (bardzo małe mutacje)
        {'mut': 'hybrid', 'rates': [0.05, 0.05, 0.05, 0.05, 1.0], 'crs': 'order', 'config_name': 'hybrid_Stable'},
        # 4. Wersja skupiona tylko na Inwersji i ERX (prawdopodobnie najsilniejsza)
        {'mut': 'inv', 'rates': [0.15, 0.4, 0.10, 0.05, 1.0], 'crs': 'erx', 'config_name': 'inv_Heavy_ERX'}
    ]

    School_quantity = [10, 20, 50, 100]
    school_data_base = []

    for quantity in School_quantity:
        instance = generate_random_instance(quantity, seed=42)
        school_data_base.append(Graph(instance))
    
    results = []
    convergence_logs = []

    total_steps = num_trials*len(basic_configs + advanced_configs)*len(School_quantity)
    current_step = 0

    test_start_time = time.time()
    one_step_avg_time_sum = 0
    one_step_avg_time = 0

    print(f"Rozpoczynam benchmark. Łączna liczba testów do wykonania: {total_steps}")
    for graph in school_data_base:
        num_schools = len(graph.nodes) - 1

        for config in (basic_configs + advanced_configs):
            #print(f"Testowanie: {config['config_name']} dla {num_schools} szkół...")

            for trial in range(num_trials):
                start_time = time.time()

                output = run_evolution(
                    graph=graph,
                    pop_size=60, 
                    generations=300, 
                    mutation_mode=config['mut'],
                    mut_rates=config['rates'],
                    cross_mode=config['crs']
                )


                duration = time.time() - start_time
                
                results.append({
                    'size': num_schools,
                    'config': config['config_name'],
                    'trial': trial,
                    'fitness': output['best_fitness'],
                    'time': duration,
                    'routes_count': len(output['routes'])
                })

                if trial == 0:
                    convergence_logs.append({
                        'size': num_schools,
                        'config': config['config_name'],
                        'history': output['history_best']
                    })

                current_step += 1
                one_step_avg_time_sum += duration
                
                progress = (current_step / total_steps) * 100
                avg_time_per_step = one_step_avg_time_sum / current_step
                remaining_steps = total_steps - current_step
                time_left_seconds = remaining_steps * avg_time_per_step
                
                eta_min = int(time_left_seconds // 60)
                eta_sec = int(time_left_seconds % 60)

                print(
                    f"\rPostęp: {progress:.2f}% | "
                    f"ETA: {eta_min}m {eta_sec}s | "
                    f"Aktualnie: {config['config_name']} ({num_schools} szkół)   ", 
                    end='', flush=True
                )

    print(f"\rPostęp: 100.00% | ETA: 0m 0s | ", end="", flush=True)
    total_duration = time.time() - test_start_time
    et_min = int(total_duration // 60)
    et_sec = int(total_duration % 60)
    print(f"Testy zakończone sukcesem w czasie: {et_min}m {et_sec}s")
    print()

    results_dir = 'tests_results' 

    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    csv_path = os.path.join(results_dir, output_file)
    json_path = os.path.join(results_dir, 'convergence_data.json')

    keys = results[0].keys()
    with open(csv_path, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)
    
    print(f"\nBenchmark zakończony. Wyniki zapisano w: {csv_path}")

    with open(json_path, 'w') as f:
        json.dump(convergence_logs, f)
    
    print(f"Dane zbieżności zapisano w: {json_path}")

if __name__ == '__main__':
    main_benchmark(30)