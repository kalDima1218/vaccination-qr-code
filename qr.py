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
        user_key = request.form.get('key')
        with open(os.getcwd() + "/key.txt", "r") as f:
            original_key = f.readline()
        print(user_key, original_key)

        if user_key == original_key and len(fio.split(" ")) == 3 and (int(day) > 0 and int(day) < 32):
            message = "Все данные введены верно, QR-код создан"
            first_name = fio.split()[0][0] + ((len(fio.split()[0]) - 1) * "*")
            second_name = fio.split()[1][0] + ((len(fio.split()[1]) - 1) * "*")
            patronymic = fio.split()[2][0] + ((len(fio.split()[2]) - 1) * "*")
            date = day + " " + month
            hash = hashlib.sha256((fio + " " + date).encode('utf-8')).hexdigest()[:12].upper()
            file_qr = os.getcwd() + "/templates/static/png/" + 'qr-' + hash + '.png'
            file_html = os.getcwd() + "/templates/static/html/" + 'qr-' + hash + '.html'
            if not os.path.exists(file_qr):
                with open(os.getcwd() + "/templates/static/html/qr-demo.html", "r") as f:
                    demo_html = f.readline()
                with open(file_html, "w") as f:
                    f.write(demo_html.replace("Имя", first_name).replace("Фамилия", second_name).replace("Отчество", patronymic).replace("дата", date))
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
    return render_template("/static/html/qr-" + id + ".html")


socketio = SocketIO()
socketio.init_app(app)
socketio.run(app, host="immune.mos.tmweb.ru")
