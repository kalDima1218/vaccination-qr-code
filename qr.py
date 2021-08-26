import os
import base64
import hashlib
import pyqrcode
#from flask_socketio import SocketIO
from flask import Flask, request, render_template, send_file

app = Flask(__name__)
app.debug = False


@app.route('/', methods=['POST', 'GET'])
def index():
    #message = ''
    if request.method == 'POST':
        fio = request.form.get('fio')
        month = request.form.get('month')
        day = request.form.get('day')
        #user_key = request.form.get('key')
        #with open(os.getcwd() + "/key.txt", "r") as f:
            #original_key = f.readline()
        if len(fio.split(" ")) == 3 and (int(day) > 0 and int(day) < 32) and month != "Выберите месяц рождения": #user_key == original_key
            #message = "Все данные введены верно, QR-код создан"
            first_name = fio.split()[0][0] + ((len(fio.split()[0]) - 1) * "*")
            second_name = fio.split()[1][0] + ((len(fio.split()[1]) - 1) * "*")
            patronymic = fio.split()[2][0] + ((len(fio.split()[2]) - 1) * "*")
            date = day + " " + month

            hash = base64.b64encode(bytes(first_name + " " + second_name + " " + patronymic + " " + date, 'utf-8')).decode()

            file_qr = os.getcwd() + "/templates/png/" + 'qr-' + hash + '.png'
            if not os.path.exists(file_qr):
                url = pyqrcode.create("https://immune.mos.tmweb.ru:5000/qr?id=" + hash)
                url.png(file_qr, scale=5)
            return send_file(file_qr, as_attachment=True, mimetype='image/png')
        else:
            #message = "Данные введены неверно"
            return render_template('index.html')
    else:
        return render_template('index.html')


@app.route('/qr')
def qr():
    id = request.args.get("id")
    data = base64.b64decode(bytes(id, 'utf-8')).decode().split(" ")
    return render_template("qr-demo.html", message=data)


#socketio = SocketIO()
#socketio.init_app(app)
#socketio.run(app, host="immune.mos.tmweb.ru")
app.run(host="immune.mos.tmweb.ru", ssl_context=('cert.pem', 'privkey.pem'))
