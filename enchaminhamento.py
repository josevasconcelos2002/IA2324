import math
import itertools

RADIUS = 150  # Parece ser em metros
R = 6371  # Raio do planeta


def create_sections(list_encomendas):
    sections = {}
    used = []
    length = len(list_encomendas)
    sec_count = 0
    for i in range(0, length):
        if list_encomendas[i] not in used:
            enc = list_encomendas[i]
            for j in range(0, length):
                if j != i and list_encomendas[j] not in used:
                    enc2 = list_encomendas[j]
                    dist = calculate_euclidean_distance(enc.destination[1]['x'], enc.destination[1]['y'],
                                                        enc2.destination[1]['x'], enc2.destination[1]['y'])
                    print('dist = ' + str(dist))
                    if dist <= RADIUS:
                        if enc not in used:
                            used.append(enc)
                        used.append(enc2)
                        if sec_count not in sections.keys():
                            sections[sec_count] = [enc]
                        sections[sec_count].append(enc2)
            sec_count = sec_count + 1
    # sections['sectionless'] = [enc for enc in list_encomendas if enc not in used]
    sectionless = [enc for enc in list_encomendas if enc not in used]
    closest_section = {}
    max_dist = 9999999
    chosen_sec = 0
    for enc in sectionless:
        for k, v in sections.items():
            closest_section[k] = []
            distances = []
            for enc2 in v:
                distances.append(calculate_euclidean_distance(enc.destination[1]['x'], enc.destination[1]['y'],
                                                              enc2.destination[1]['x'], enc2.destination[1]['y']))
                min_dist = min(distances)
                if min_dist < max_dist:
                    max_dist = min_dist
                    chosen_sec = k
        sections[chosen_sec].append(enc)
    return sections


def calculate_euclidean_distance(lat1, lon1, lat2, lon2):
    x1 = R * math.cos(lat1) * math.cos(lon1)
    x2 = R * math.cos(lat2) * math.cos(lon2)
    y1 = R * math.cos(lat1) * math.sin(lon1)
    y2 = R * math.cos(lat2) * math.sin(lon2)
    z1 = R * math.sin(lat1)
    z2 = R * math.sin(lat2)

    return math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2) + math.pow((z2 - z1), 2))
    # mid = (lat1 + lat2) / 2
    # return R * math.sqrt(math.pow((lat2 - lat1), 2) + math.pow(math.cos(mid * math.pow(lon2 - lon1, 2)), 2))


def combine_by_weight(sections):
    # Ranges de peso dos vehículos
    weight_ranges = {
        3: range(1, 6),
        2: range(6, 21),
        1: range(21, 101),
    }

    all_combinations = {}

    for key, encomenda_list in sections.items():
        # Ordena as encomendas por peso
        encomenda_list = sorted(encomenda_list, key=lambda x: x.weight)
        # Para cada tipos de vehículo, pega no nome e na range de pesos que pode levar
        for weight_range, weight_values in weight_ranges.items():
            filtered_combinations = set()
            # r é o numero de elementos que cada agrupamento vai ter, e tem de variar de 1 ate ao tamanho da lista
            for r in range(1, len(encomenda_list) + 1):  # Vary the length of combinations
                # Para cada combinação possível de encomendas com r elementos
                for combination in itertools.combinations(encomenda_list, r):
                    # Calcula o peso total dessa combinação
                    total_weight = sum(item.weight for item in combination)
                    # Assim tem todas as combinações que um vehiculo pode ter:
                    # if total_weight <= max(weight_values):
                    # Assim tem todas as combinaçõe que o vehiculo pode ter mas não as de outros vehículos:
                    if max(weight_values) >= total_weight >= min(weight_values):
                        # Isto é para remover agrupamentos que ainda tem espaço possível para outras encomendas
                        if r != 1:
                            # Para todos os agrupamentos de r - 1 dos agrupamentos de r
                            for comb in itertools.combinations(combination, r - 1):
                                if comb in filtered_combinations:
                                    filtered_combinations.remove(comb)
                        filtered_combinations.add(combination)

            if filtered_combinations:
                all_combinations[key, weight_range] = filtered_combinations

    # Prints
    for (list_key, weight_range), combinations in all_combinations.items():
        print(f"{list_key} combinations ({weight_range} weight range):")
        for comb in combinations:
            for e in comb:
                print(str(e.weight) + " -> " + str(e.idnt))
            print("============")
    return all_combinations


def route(list_estafetas, sections, grouped_sections, algoritmo, graph, start):
    estafetas_by_vehicle = {1: [], 2: [], 3: []}
    for estafeta in list_estafetas:
        estafetas_by_vehicle[estafeta.vehicle.value['type']].append(estafeta)

    assigned_encomendas = {}
    for (section, vehicle), encomendas in grouped_sections.items():
        visited_deliveries = []
        origin = start
        for comb in encomendas:
            for enc in comb:
                if enc not in visited_deliveries:
                    _, path, _ = algoritmo(graph, origin, str(enc.destination[0]))
                    if calculate_delivery_time(path, estafetas_by_vehicle[vehicle][0].vehicle, enc.weight, graph) <= enc.deadline + 15:
                        origin = str(enc.destination[0])
                        visited_deliveries.append(enc)
                        if (section, vehicle) not in assigned_encomendas.keys():
                            assigned_encomendas[(section, vehicle)] = []
                        assigned_encomendas[(section, vehicle)].append(enc)
    return assigned_encomendas

# Calcula o tempo de entregar uma encomenda
def calculate_delivery_time(path, vehicle, weight, graph):
    # Por cada kilo na encomenda, diminui a velocidade por 0.1
    max_speed = vehicle.value['speed'] - (weight / 100)
    total_time = 0
    for i in range(0, len(path) - 1):
        edge = graph[path[i]][path[i + 1]]
        total_time += edge['length'] / (max_speed * edge['traffic'])
    return total_time
