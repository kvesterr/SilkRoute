from config import *

def crd2float(coords: str):
    """Возвращает кортеж координат типа float, полученный из координат типа str."""
    y, x = coords[7:len(coords)-1].split()
    y = y[:len(y)-1]
    return (float(x), float(y))

def route(start, end):
    """Возвращает маршрут от координат start до end."""
    route = ''
    try:
        route = client.directions(
            coordinates=[list(reversed(start)), list(reversed(end))],
            profile='driving-car', format='geojson'
        )
    except:
        return 1

    return route['features'][0]['geometry']['coordinates']

def routestr(start, end):
    """Возвращает маршрут в виде строки."""
    res = ''
    rt = route(start, end)
    if rt == 1:
        return res

    for coord in rt:
        res += str(coord) + ', '

    return res[:len(res)-2]

def get_search_suggestions(text):
    """Возвращает список подсказок адресов в зависимости от входного текста."""
    response = client.pelias_autocomplete(text=text, focus_point=(37.5, 55.5), sources=['oa'], rect_min_x=35.3,
                                    rect_min_y=54.7, rect_max_x=40, rect_max_y=56.9)
    suggestions = [feature['properties']['label'] for feature in response['features']]
    return suggestions

