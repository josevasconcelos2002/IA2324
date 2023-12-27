import math

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

def route(estafetas, sections, algoritmo, graph):
    unused_estafetas = []
    estafetas_by_vehicle = {1: [], 2: [], 3: []}
    for estafeta in estafetas:
        estafetas_by_vehicle[estafeta.vehicle.value['type']].append(estafeta)

    assigned_encomendas = {}
    estafeta_rating = {}
    extra_time = 15
    for section, (encomendas, max_weight) in sections.items():
        if len(encomendas) == 0:
            unused_estafetas.append(section)
            continue
        visited_deliveries = []
        # 5379 e o nodo que fica mais proximo do CTT mais proximo do centro de Braga
        aux = list(graph.nodes(data=True))
        origin = str(aux[5379][0])
        vehicle = estafetas[section].vehicle
        estafeta_rating[section] = [0, {}, len(encomendas)]
        for enc in encomendas:
            #Soma dos ratings, dicionario encomendas atrasas e qual o tempo atrasado, n# de encomendas associadas
            if enc not in visited_deliveries:
                _, path, _ = algoritmo(graph, origin, str(enc.destination[0]))
                time = calculate_delivery_time(path, vehicle, enc.weight, graph)
                rating = 5
                #Existe um tempo extra de 15 minutos
                if time <= enc.deadline + extra_time:
                    estafeta_rating[section][0] += 5
                else:
                    elapsed_time = time - (enc.deadline + extra_time)
                    #E retirado 0.1 ao rating por cada 5 minutos que ultrapassa o tempo, mas nunca fica menor que 0
                    rating = 5 - 0.1 * (elapsed_time / 5)
                    if rating < 1:
                        rating = 1
                    estafeta_rating[section][0] += rating
                    estafeta_rating[section][1][enc.idnt] = elapsed_time + extra_time
                origin = str(enc.destination[0])
                visited_deliveries.append(enc)
                if section not in assigned_encomendas.keys():
                    assigned_encomendas[section] = []
                assigned_encomendas[section].append(path)
    return assigned_encomendas, estafeta_rating


# Calcula o tempo de entregar uma encomenda
def calculate_delivery_time(path, vehicle, weight, graph):
    # Por cada kilo na encomenda, diminui a velocidade por 0.1
    max_speed = vehicle.value['speed'] - (weight / 100)
    total_time = 0
    for i in range(0, len(path) - 1):
        edge = graph[path[i]][path[i + 1]]
        aux = aux_get(edge)
        total_time += aux['length'] / (max_speed * aux['traffic'])
    return total_time

def aux_get(x):
    return list(x.values())[0]
