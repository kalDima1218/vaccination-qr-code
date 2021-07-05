import os
import hashlib
import pyqrcode
from flask_socketio import SocketIO
from flask import Flask, request, render_template, send_file

app = Flask(__name__)
app.debug = False


@app.route('/', methods=['POST', 'GET'])
def index():
    message = ''
    if request.method == 'POST':
        fio = request.form.get('fio')
        month = request.form.get('month')
        day = request.form.get('day')

        if len(fio.split(" ")) == 3 and (int(day) > 0 and int(day) < 32):
            message = "Все данные введены верно, QR-код создан"
            first_name = fio.split()[0][0] + ((len(fio.split()[0]) - 1) * "*")
            second_name = fio.split()[1][0] + ((len(fio.split()[1]) - 1) * "*")
            patronymic = fio.split()[2][0] + ((len(fio.split()[2]) - 1) * "*")
            date = day + " " + month
            hash = hashlib.sha256((fio + " " + date).encode('utf-8')).hexdigest()[:12].upper()
            file_qr = os.getcwd().replace("\\", "/") + "/templates/static/" + 'qr-' + hash + '.png'
            file_html = os.getcwd().replace("\\", "/") + "/templates/" + 'qr-' + hash + '.html'
            if not os.path.exists(file_qr):
                with open(file_html, "w") as f:
                    f.write("""<!DOCTYPE html><html lang="ru" translate="no"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="theme-color" content="#000000"><meta property="og:type" content="website"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="keywords" content="QR-код, QR код, кьюаркод, куар код, код вакцина, qr code, qr код, qr-код, куаркод, Кьюар код, посещение общественного места, общественное место в Москве, QR, проход в клуб, бар, ресторан, проходка на концерт, регистрация на вход, регистрация"><meta name="descriptions" content="Получение QR-кода на посещение общественного места в Москве"><meta name="url" content="immune.mos.ru"><meta name="image:alt" content="Получение QR-кода на посещение общественного места в Москве"><title>Получение QR-кода на посещение общественного места в Москве</title><link rel="shortcut icon" type="image/x-icon" href="https://www.mos.ru/static/images/favicon/favicon.ico"><link href="https://immune.mos.ru/static/css/0.3a1fd90d.chunk.css" rel="stylesheet"><link href="https://immune.mos.ru/static/css/qrcode.e2b37103.chunk.css" rel="stylesheet"></head><body><div class="main-container"><div class="main_content" id="root"><div class="immun-page"><div class="white_bg_status"><div class="content-container informer-start-bottom centered"><br><img src="https://immune.mos.ru/img/mos_logo.svg" width="60%"><br><br><div id="print"><div class="status-container"><div><span class="status-value">Действителен</span></div></div><br><div><h4 class="status-param">Сведения о владельце QR-кода:<br>Имя Фамилия Отчество</h4><h4 class="status-param">Дата рождения: дата</h4><h4 class="status-param">Срок действия: 16.10.2021</h4></div></div></div></div></div></div></div><iframe name="easyXDM_pecXDM_pec-channel-mpgu_provider" id="easyXDM_pecXDM_pec-channel-mpgu_provider" src="cid:frame-4FFA734BDD0662C012A5978CA29488D2@mhtml.blink" frameborder="0" style="position: absolute; top: -2000px; left: 0px;"></iframe></body></html>""".replace("Имя", first_name).replace("Фамилия", second_name).replace("Отчество", patronymic).replace("дата", date))
                url = pyqrcode.create("http://immune.mos.tmweb.ru:5000/qr?id=" + hash)
                url.png(file_qr, scale=5)
            return send_file(file_qr, as_attachment=True, mimetype='image/png')
        else:
            message = "Данные введены неверно"
            return render_template('index.html')
    else:
        return render_template('index.html')


@app.route('/qr')
def qr():
    id = request.args.get("id")
    return render_template("qr-" + id + ".html")


socketio = SocketIO()
socketio.init_app(app)
socketio.run(app, host="immune.mos.tmweb.ru")
