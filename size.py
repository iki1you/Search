import math

def getsize(toponym):
    delta = str(max(float(str(abs(float(toponym["boundedBy"]["Envelope"]["lowerCorner"].split()[0]) -
                                  float(toponym["boundedBy"]["Envelope"]["upperCorner"].split()[0])))[0:6]),
                    float(str(abs(float(toponym["boundedBy"]["Envelope"]["lowerCorner"].split()[1]) -
                                  float(toponym["boundedBy"]["Envelope"]["upperCorner"].split()[1])))[0:6])))

    for i in range(len(delta)):
        if delta[i] != '0' and delta[i] != '.':
            delta = list(delta)
            delta[i] = '1'
            delta = str(''.join(delta))
            delta = delta[0:i + 1]
            break

    return delta


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000  # 111 километров в метрах
    a_lon, a_lat = float(a[0]), float(a[1])
    b_lon, b_lat = float(b[0]), float(b[1])

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)

    return distance
