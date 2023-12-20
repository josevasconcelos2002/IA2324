import math
import itertools

R = 6371  # Raio do planeta


def create_routes(graph, encomendas, estafetas, algorythm):
    encomendas = sort_encomendas(graph, encomendas)
    estafetas = sort_estafetas(estafetas)
    sections = create_sections(encomendas, estafetas)
    return route(estafetas, sections, algorythm, graph)


# Ordena encomendas por distancia do destino ao ponto de origem, por ordem crescente
def sort_encomendas(graph, encomendas):
    origin = graph.nodes(data=True)['ORIGIN']
    return sorted(encomendas, key=lambda enc: calculate_euclidean_distance(origin['x'], origin['y']
                                                                           , enc.destination[1]['x'],
                                                                           enc.destination[1]['y']))


# Ordena estafetas por vehiculo, primeiro os de bicicleta, depois os de mota, depois os de carro
def sort_estafetas(estafetas):
    return sorted(estafetas, key=lambda est: est.vehicle.value['type'], reverse=True)


def create_sections(encomendas, estafetas):
    n_estafetas = len(estafetas)
    sections = {i: ([], 0) for i in range(n_estafetas)}
    used = []
    length = len(encomendas)
    sec_count = 0
    for i in range(length):
        radius = estafetas[sec_count].vehicle.value['radius']
        max_weight = estafetas[sec_count].vehicle.value['max_weight']
        if encomendas[i] not in used:
            enc = encomendas[i]
            cur_weight = enc.weight
            for j in range(length):
                if j != i and encomendas[j] not in used:
                    enc2 = encomendas[j]
                    dist = calculate_euclidean_distance(enc.destination[1]['x'], enc.destination[1]['y'],
                                                        enc2.destination[1]['x'], enc2.destination[1]['y'])
                    print('dist = ' + str(dist))
                    if dist <= radius and cur_weight + enc2.weight <= max_weight:
                        if enc not in used:
                            used.append(enc)
                        used.append(enc2)
                        if len(sections[sec_count][0]) == 0:
                            sections[sec_count] = ([enc], cur_weight)
                        sections[sec_count] = (sections[sec_count][0] + [enc2], sections[sec_count][1] + enc2.weight)
                        cur_weight += enc2.weight
            sec_count += 1
            if sec_count == n_estafetas:
                break

    sectionless = [enc for enc in encomendas if enc not in used]
    max_dist = 9999999
    chosen_sec = 0
    sectioned = []

    for enc in sectionless:
        for k, (l, w) in sections.items():
            distances = []
            for enc2 in l:
                distances.append(calculate_euclidean_distance(enc.destination[1]['x'], enc.destination[1]['y'],
                                                              enc2.destination[1]['x'], enc2.destination[1]['y']))
                min_dist = min(distances)
                if min_dist < max_dist and enc.weight + w <= estafetas[k].vehicle.value['max_weight']:
                    max_dist = min_dist
                    chosen_sec = k
        sections[chosen_sec] = (sections[chosen_sec][0] + [enc], sections[chosen_sec][1] + enc.weight)
        sectioned.append(enc)
    sectionless = [enc for enc in sectionless if enc not in sectioned]
    used += sectioned
    print(f"THERE ARE {len(sectionless)} SECTIONLESS")
    print(f"THERE ARE {len(used)} USED")
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


"""
def combine_by_weight(sections, estafetas):
    # Ranges de peso dos vehículos
    weight_ranges = {
        3: range(1, 6),
        2: range(6, 21),
        1: range(21, 101),
    }

    all_combinations = {}

    for section, encomenda_list in sections.items():
        # Ordena as encomendas por peso
        encomenda_list = sorted(encomenda_list, key=lambda x: x.weight)
        # Para cada tipos de vehículo, pega no nome e na range de pesos que pode levar
        vehicle = estafetas[section].vehicle.value['type']
        weight_values = weight_ranges[vehicle]
        # for weight_range, weight_values in weight_ranges.items():
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
            all_combinations[section, vehicle] = filtered_combinations


# Prints
    for (list_key, weight_range), combinations in all_combinations.items():
        print(f"{list_key} combinations ({weight_range} weight range):")
        for comb in combinations:
            for e in comb:
                print(str(e.weight) + " -> " + str(e.idnt))
            print("============")
    return all_combinations
"""


def route(estafetas, sections, algoritmo, graph):
    unused_estafetas = []
    estafetas_by_vehicle = {1: [], 2: [], 3: []}
    for estafeta in estafetas:
        estafetas_by_vehicle[estafeta.vehicle.value['type']].append(estafeta)

    assigned_encomendas = {}
    for section, (encomendas, max_weight) in sections.items():
        if len(encomendas) == 0:
            unused_estafetas.append(section)
            continue
        visited_deliveries = []
        # 5379 e o nodo que fica mais proximo do CTT mais proximo do centro de Braga
        aux = list(graph.nodes(data=True))
        origin = str(aux[5379][0])
        vehicle = estafetas[section].vehicle
        for enc in encomendas:
            if enc not in visited_deliveries:
                _, path, _ = algoritmo(graph, origin, str(enc.destination[0]))
                time = calculate_delivery_time(path, vehicle, enc.weight, graph)
                if time <= enc.deadline + 15:
                    origin = str(enc.destination[0])
                    visited_deliveries.append(enc)
                    if section not in assigned_encomendas.keys():
                        assigned_encomendas[section] = []
                    assigned_encomendas[section].append(enc)
                #else:
                    # TODO: LIDAR COM ENCOMENDAS ATRASADAS
                    # secalhar tentar atribuir a estafetas que nao tem encomendas, se nao for possivel, atribuir a estafeta
                    # mais proximo
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
