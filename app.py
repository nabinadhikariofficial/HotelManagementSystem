from flask import Flask, session, request, redirect, url_for, render_template

app = Flask(__name__)
app.secret_key = 'key'

host_add = '0.0.0.0'
port_add = 800


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


@app.route("/reception")
def Reception():
    if 'loggedin' in session:
        return render_template('reception.html')
    return redirect(url_for('Login'))


@app.route("/stock")
def Stock():
    if 'loggedin' in session:
        username = request.args.get('username')
        print(username)
        return render_template('stock.html')
    return redirect(url_for('Login'))


@app.route("/profile")
def Profile():
    if 'loggedin' in session:
        return render_template('profile.html')
    return redirect(url_for('Login'))


@app.route("/registration")
def Registration():
    if 'loggedin' in session:
        status = request.args.get('status')
        return render_template('registration.html', status=status)
    return redirect(url_for('Login'))


if __name__ == "__main__":
    app.run(host=host_add, port=port_add, debug=True)
