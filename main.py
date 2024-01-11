from flask import Flask, render_template, request, Response, jsonify
import time

from utils import *

app = Flask(__name__)

def generate_updates():
    """Функция необходимая для отправки (обновления) на страницу данных."""
    global start, end, upd
    while True:
        time.sleep(2)
        coords = ''
        if (upd == True) and (not (start == 0)) and (not (end == 0)):
            coords = routestr(start, end)
            if not (coords == ''):
                yield f"data: {coords}\n\n"
        upd = False

@app.route('/updates')
def updates():
    """Маршрут для выполнения обновлений."""
    return Response(generate_updates(), content_type='text/event-stream')

@app.route('/from', methods=['POST'])
def frm():
    """Функция для обработки нажатия кнопки (Маршрут отсюда)."""
    global start, upd
    data = request.form.get('data')
    start = crd2float(data)
    upd = True

    return data

@app.route('/to', methods=['POST'])
def to():
    """Функция для обработки нажатия кнопки (Маршрут сюда)."""
    global end, upd
    data = request.form.get('data')
    end = crd2float(data)
    upd = True

    return data

@app.route('/search', methods=['POST'])
def search():
    """Функция для обновления значений start и end при вводе адресов в виде текста."""
    start_addr = request.form.get('start')
    end_addr = request.form.get('end')

    global start, end, upd
    start = client.pelias_search(start_addr, focus_point=(37.5, 55.5), sources=['osm', 'oa'], rect_min_x=35.3,
                                    rect_min_y=54.7, rect_max_x=40, rect_max_y=56.9)
    if len(start['features']) > 0:
        start = list(reversed(start['features'][0]['geometry']['coordinates']))

    end = client.pelias_search(end_addr, focus_point=(37.5, 55.5), sources=['osm', 'oa'], rect_min_x=35.3,
                                    rect_min_y=54.7, rect_max_x=40, rect_max_y=56.9)
    if len(end['features']) > 0:
        end = list(reversed(end['features'][0]['geometry']['coordinates']))

    upd = True

    return [start, end]

@app.route('/search_suggestions', methods=['GET'])
def search_suggestions():
    """Функция получающая со страницы текст и возвращающая список подсказок на основе этого текста."""
    query = request.args.get('query')
    suggestions = get_search_suggestions(query)
    return jsonify(suggestions)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
