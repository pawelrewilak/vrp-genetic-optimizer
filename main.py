from typing import List
import random

class School:
    def __init__(self, id: int, profit: float, visit_cost: float, 
                 service_time: float, time_window_start: float, time_window_end: float):
        self.id = id
        self.profit = profit          
        self.visit_cost = visit_cost  
        self.service_time = service_time      
        self.time_window_start = time_window_start 
        self.time_window_end = time_window_end     

    def __repr__(self):
        return f"School(id={self.id}, Okno=[{self.time_window_start}-{self.time_window_end}])"


class Graph:
    def __init__(self, depot_id: int = 0, 
                 vehicle_hiring_cost: float = 1100.0, 
                 max_vehicle_time: float = 480.0,    
                 penalty_factor: float = 1000.0,     
                 weights: List[List[float]] = None, 
                 nodes: List[School] = None):
        
        self.nodes_dict = {s.id: s for s in nodes} if nodes else {}
        self.depot_id = depot_id
        self.vehicle_hiring_cost = vehicle_hiring_cost
        self.max_vehicle_time = max_vehicle_time
        self.penalty_factor = penalty_factor
        
        self.weights = weights if weights is not None else []
        self.nodes = nodes if nodes is not None else []

    def get_travel_time(self, i: int, j: int) -> float:
        return self.weights[i][j]


def calculate_fitness(routes: List[List[int]], graph: Graph) -> float:

    total_profit = 0.0
    total_visit_costs = 0.0
    total_hiring_cost = 0.0
    
    total_penalty = 0.0 

    for route in routes:
        if not route:
            continue
            
        total_hiring_cost += graph.vehicle_hiring_cost
        
        current_node_id = graph.depot_id
        current_time = 0.0 
        
        for next_node_id in route:
            school = graph.nodes_dict[next_node_id]
            
            travel_time = graph.get_travel_time(current_node_id, next_node_id)
            arrival_time = current_time + travel_time
            
            start_service_time = max(arrival_time, school.time_window_start)
            
            if start_service_time > school.time_window_end:
                lateness = start_service_time - school.time_window_end
                total_penalty += lateness * graph.penalty_factor
            
            finish_time = start_service_time + school.service_time
            
            current_time = finish_time
            current_node_id = next_node_id
            
            total_profit += school.profit
            total_visit_costs += school.visit_cost
            
        return_time = graph.get_travel_time(current_node_id, graph.depot_id)
        end_of_day_time = current_time + return_time
        
        if end_of_day_time > graph.max_vehicle_time:
            overtime = end_of_day_time - graph.max_vehicle_time
            total_penalty += overtime * graph.penalty_factor / 250

    fitness = total_profit - (total_visit_costs + total_hiring_cost + total_penalty)
    
    return fitness

def decode_chromosome(chromosome: List[int], graph: Graph) -> List[List[int]]:
    
    routes = []
    current_route = []
    current_time = 0.0
    current_node_id = graph.depot_id
    
    for school_id in chromosome:
        school = graph.nodes_dict[school_id]
        dist_to = graph.get_travel_time(current_node_id, school_id)
        dist_back = graph.get_travel_time(school_id, graph.depot_id)
        
        arrival = current_time + dist_to
        start = max(arrival, school.time_window_start)
        finish = start + school.service_time
        total_time_if_added = finish + dist_back
        
        if total_time_if_added <= graph.max_vehicle_time:
            current_route.append(school_id)
            current_time = finish
            current_node_id = school_id
        else:
            if current_route:
                routes.append(current_route)
            
            current_route = [school_id]
            dist_from_depot = graph.get_travel_time(graph.depot_id, school_id)
            start_new = max(dist_from_depot, school.time_window_start)
            current_time = start_new + school.service_time
            current_node_id = school_id
            
    if current_route:
        routes.append(current_route)
        
    return routes

#Funkcja pomocnicza do oceny populacji raz na pokolenie
def score_population(gen: List[List[int]], graph: Graph) -> List[tuple]:
    scored = []
    for chromosome in gen:
        routes = decode_chromosome(chromosome, graph)
        fitness = calculate_fitness(routes, graph)
        scored.append((chromosome, fitness))
    return scored

def selection_nbest(n: int, scored_gen: List[tuple]) -> List[List[int]]:
    scored_gen.sort(key=lambda x: x[1], reverse=True)
    return [individual[0] for individual in scored_gen[:n]]

def selection_tournament(scored_gen: List[tuple], tournament_size: int = 3) -> List[int]:

    tournament = random.sample(scored_gen, tournament_size)
    tournament.sort(key=lambda x: x[1], reverse=True)
    return tournament[0][0]

def order_crossover(p1: List[int], p2: List[int]) -> List[int]:
    size = len(p1)


    index_dolny = random.randint(0, size - 2)
    index_gorny = random.randint(index_dolny + 1, size - 1)
    lenght = index_gorny - index_dolny + 1


    child = [-1] * size

    for i in range(lenght):
        child[index_dolny + i] = p1[index_dolny + i]

    k = (index_gorny + 1) % size
    m = (index_gorny + 1) % size

    succes = 0
    while succes < (size - lenght):
        
        if p2[k] not in child:
            while child[m] != -1:
                m = (m + 1) % size
            child[m] = p2[k]
            succes += 1
            m = (m + 1) % size
        k = (k + 1) % size

    return child

def swap_mutate(chromosome: List[int], mutation_rate: float = 0.55) -> List[int]:

    if random.random() > mutation_rate:
        return chromosome

    idx_a, idx_b = sorted(random.sample(range(len(chromosome)), 2))
    chromosome[idx_a], chromosome[idx_b] = chromosome[idx_b], chromosome[idx_a]

    return chromosome

def inversion_mutate(chromosome: List[int], mutation_rate: float = 0.05) -> List[int]:
    if random.random() > mutation_rate:
        return chromosome
    
    idx_a, idx_b = sorted(random.sample(range(len(chromosome)), 2))
    chromosome =  chromosome[:idx_a] + chromosome[idx_a : idx_b + 1][::-1] + chromosome[idx_b + 1:]

    return chromosome

def insertion_mutate(chromosome: List[int], mutation_rate: float = 0.55) -> List[int]:
    if random.random() > mutation_rate:
        return chromosome
    
    new_chromosome = chromosome[:] 
    idx_from = random.randint(0, len(new_chromosome) - 1)
    idx_to = random.randint(0, len(new_chromosome) - 1)

    school_id = new_chromosome.pop(idx_from)
    new_chromosome.insert(idx_to, school_id)

    return new_chromosome

def scramble_mutate(chromosome: List[int], mutation_rate: float = 0.55) -> List[int]:
    if random.random() > mutation_rate:
        return chromosome
    
    idx_a, idx_b = sorted(random.sample(range(len(chromosome)), 2))
    shuffle = chromosome[idx_a : idx_b + 1]
    random.shuffle(shuffle)
    chromosome[idx_a : idx_b + 1] = shuffle

    return chromosome

def mutator(chromosome: List[int], mode: str, mutation_rates: List[float] = [0.55, 0.55, 0.55, 0.55, 1]) -> List[int]:
    operators = [swap_mutate, inversion_mutate, insertion_mutate, scramble_mutate]

    match mode:
        case "swap":
            return swap_mutate(chromosome, mutation_rates[0])
        case "inv":
            return inversion_mutate(chromosome, mutation_rates[1])
        case "ins":
            return insertion_mutate(chromosome, mutation_rates[2])
        case "scr":
            return scramble_mutate(chromosome, mutation_rates[3])
        case "hybrid":
            idx = random.randint(0, 3)
            return operators[idx](chromosome, mutation_rates[4]) # Zmiana mutation_rates[4] na [idx] pozwala na uzyskanie pełnej kontroli nad szansą wystąpienia konkretnego typu mutacji
                                                                 # również wewnątrz trybu mieszanego, zachowując spójność parametrów zdefiniowanych dla poszczególnych operatorów.
    
    return chromosome

def run_evolution(graph: Graph, pop_size: int = 60, generations: int = 200, mutation_mode: str = 'swap', mut_rates: List[float] = [0.55, 0.55, 0.55, 0.55, 1], selection_mode:str = 'turn'):
    all_school_ids = [s.id for s in graph.nodes if s.id != graph.depot_id]
    population = [random.sample(all_school_ids,len(all_school_ids)) for _ in range(pop_size)]

    best_global_chromosome = None
    best_global_fitness = float("inf")

    for _ in range(generations):
        scored_generation = score_population(population, graph)
        scored_generation.sort(key=lambda x: x[1], reverse=True)

        best_local_chromosome , best_local_fitness = scored_generation[0]

        if best_local_fitness > best_global_fitness:
            best_global_fitness = best_local_fitness
            best_global_chromosome = best_local_chromosome
    
    new_population = [selection_nbest(2,scored_generation)] # Elitaryzm, 2 najlepsze zostają

    while len(new_population) < pop_size:
        if selection_mode is 'turn':
            p1 = selection_tournament(scored_generation)
            p2 = selection_tournament(scored_generation)

            child = order_crossover(p1,p2)



    