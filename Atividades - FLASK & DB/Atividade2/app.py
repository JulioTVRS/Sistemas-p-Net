from flask import Flask, request, render_template, url_for, \
    session, redirect

app = Flask(__name__)

bancodados = {}

app.config['SECRET_KEY'] = 'superdificil'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dash():    
    if 'user' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('register'))

@app.route('/login', methods=['POST', 'GET'])
def login():

    if 'user' in session:
        return redirect(url_for('dash'))

    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        if nome in bancodados and bancodados[nome] == senha:
            session['user'] = nome
            return redirect(url_for('dash'))
        else:
            return "usuario inexistente ou senha incorreta"


    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():

    ## esse bloco tanto para register quanto para login
    if 'user' in session:
        return redirect(url_for('dash'))

    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        # regsitrar no banco 
        if nome not in bancodados:
            bancodados[nome] = senha
            session['user'] = nome
            return redirect(url_for('dash'))
        else:
            return "Ja estas cadastrado"

    return render_template('register.html')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))