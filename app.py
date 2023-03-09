from flask import Flask, session, request, redirect, url_for, render_template
from flask_pymongo import PyMongo
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'key'

host_add = '0.0.0.0'
port_add = 5005

app.config["MONGO_URI"] = "mongodb://localhost:27017/hotel"
mongo = PyMongo(app)


@app.route('/', methods=['GET', 'POST'])
def Login():
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if 'loggedin' in session:
        return redirect(url_for('Index'))
    if request.method == 'POST':
        session['loggedin'] = True
    return render_template('login.html')


@app.route("/index")
def Index():
    if 'loggedin' in session:
        return render_template('index.html')
    return redirect(url_for('Login'))


color_data = {}
guest_name = {}


def color(datas):
    i = 0
    for data in datas:
        if data['status'] == 'True':
            color_data[i] = "#1cc88a"
            guest_name[i] = data['guest_name'].upper()
        else:
            color_data[i] = "white"
            guest_name[i] = "N/A"
        i = i+1
    return(color_data, guest_name)


@app.route("/reception")
def Reception():
    if 'loggedin' in session:
        guest_data = mongo.db.temp.find_one({"status": "current"})
        color_data, guest_name = color(guest_data['reception'])
        return render_template('reception.html', guest_data=guest_data['reception'], color=color_data, guest=guest_name)
    return redirect(url_for('Login'))


@app.route("/stock")
def Stock():
    if 'loggedin' in session:
        return render_template('stock.html')
    return redirect(url_for('Login'))


@app.route("/profile")
def Profile():
    if 'loggedin' in session:
        return render_template('profile.html')
    return redirect(url_for('Login'))


@app.route("/registration", methods=['GET', 'POST'])
def Registration():
    if 'loggedin' in session:
        flag_a = True
        status = request.args.get('status')
        room = status[:3]
        action = status[4:]
        if action == 'checkin' or action == 'checkout':
            flag_a = True
        else:
            flag_a = False
        if request.method == 'POST':
            data = {"room": room,
                    "status": "True",
                    "guest_name": request.form.get('guest_name'),
                    "friend_name": request.form.get('friend_name'),
                    "address": request.form.get('address'),
                    "nationality": request.form.get('nationality'),
                    "id_type": request.form.get('id_type'),
                    "id_no": request.form.get('id_no'),
                    "pax": request.form.get('pax'),
                    "coming_from": request.form.get('coming_from'),
                    "purpose": request.form.get('purpose'),
                    "mobile_no": request.form.get('mobile_no'),
                    "rate": request.form.get('rate'),
                    "advance": request.form.get('advance'),
                    "date": datetime.now().strftime("%Y/%m/%d %H:%M:%S")}
            print(data)
            mongo.db.reception.insert_one(data)
            mongo.db.temp.update_one(
                {"reception": {"$elemMatch": {"room": room}}}, {"$set": {"reception.$.room": data['room'],
                                                                         "reception.$.status": data['status'],
                                                                         "reception.$.guest_name": data['guest_name'],
                                                                         "reception.$.friend_name": data['friend_name'],
                                                                         "reception.$.address": data['address'],
                                                                         "reception.$.nationality": data['nationality'],
                                                                         "reception.$.id_type": data['id_type'],
                                                                         "reception.$.id_no": data['id_no'],
                                                                         "reception.$.pax": data['pax'],
                                                                         "reception.$.coming_from": data['coming_from'],
                                                                         "reception.$.purpose": data['purpose'],
                                                                         "reception.$.mobile_no": data['mobile_no'],
                                                                         "reception.$.rate": data['rate'],
                                                                         "reception.$.advance": data['advance'],
                                                                         "reception.$.date": data['date']}})
            return redirect(url_for('Reception'))
        return render_template('registration.html', room=room, action=action, flag_a=flag_a, color=['#1cc88a', 'white'])
    return redirect(url_for('Login'))


@app.route("/add")
def Add():
    # mongo.db.temp.insert_one()
    return ("done")


if __name__ == "__main__":
    app.run(host=host_add, port=port_add, debug=True)
