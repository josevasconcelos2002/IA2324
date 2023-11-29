import math

RADIUS = 5  # KM
R = 6371  # Raio do planeta


# Divide as encomendas em secções
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
                        if enc not in sections.keys():
                            sections[sec_count] = [enc]
                        sections[sec_count].append(enc2)
            sec_count = sec_count + 1
    sections['sectionless'] = [enc for enc in list_encomendas if enc not in used]
    return sections

#Calcula a distancia euclideana entre dois pointos, usando a latitude e longitude desse ponto
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
