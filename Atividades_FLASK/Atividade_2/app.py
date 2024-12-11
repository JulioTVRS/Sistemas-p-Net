from flask import Flask, request, render_template, url_for, redirect
import sqlite3

app = Flask(__name__)


def get_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dash():
    nome = request.args.get('nome')
    senha = request.args.get('senha')

    if nome and senha:
        conn = get_connection()
        user = conn.execute('SELECT * FROM users WHERE nome = ? and senha = ?', (nome, senha)).fetchone()
        conn.close()

        if user:
            return render_template('dashboard.html', nome=nome)
    
    
    return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        conn = get_connection()
        user = conn.execute('SELECT * FROM users WHERE nome = ? and senha = ?', (nome, senha)).fetchone()
        conn.close()

        if user:
            return redirect(url_for('dash', nome=nome, senha=senha))
        else:
            return "Usuário não existe ou a senha está incorreta."

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']

        conn = get_connection()
        user = conn.execute('SELECT * FROM users WHERE nome = ?',(nome,)).fetchone()

        if user:
            return "Usuário já cadastrado"
        else:
            conn.execute('INSERT INTO users (nome, senha) VALUES (?, ?)', (nome, senha))
            conn.commit()
            conn.close()
            return redirect(url_for('dash', nome=nome, senha=senha))

    return render_template('register.html')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    return render_template('index.html')