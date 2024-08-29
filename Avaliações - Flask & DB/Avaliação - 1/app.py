from flask import Flask, render_template, url_for, redirect, request
import sqlite3

app = Flask(__name__)

def get_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        cargo = request.form['cargo']

        conn = get_connection()
        if cargo == "aluno":
            user = conn.execute("SELECT * FROM alunos WHERE nome = ?",(nome,)).fetchone()
            if user:
                return "Esse usuário já está cadastrado."
            else:
                conn.execute("INSERT INTO alunos (nome, senha) VALUES (?, ?)",(nome,senha))
                conn.commit()
                conn.close()
                return redirect(url_for('dash', nome=nome, senha=senha, cargo=cargo))
        elif cargo == "professor":
            user = conn.execute("SELECT * FROM professores WHERE nome = ?",(nome,)).fetchone()
            if user:
                return "Esse usuário já está cadastrado."
            else:
                conn.execute("INSERT INTO professores (nome, senha) VALUES (?, ?)",(nome, senha))
                conn.commit()
                conn.close()
                return redirect(url_for('dash', nome=nome, senha=senha, cargo=cargo))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        cargo = request.form['cargo']

        conn = get_connection()
        if cargo == "aluno":
            user = conn.execute("SELECT * FROM alunos WHERE nome = ? and senha = ?",(nome, senha)).fetchone()
            conn.close()
            if user:
                return redirect(url_for('dash', nome=nome, senha=senha, cargo=cargo))
            else:
                return "Usuário não existe, ou a senha está incorreta. Vale também checar caso a opção Professor/Aluno tenha sido trocada!"
        elif cargo == "professor":
            user = conn.execute("SELECT * FROM professores WHERE nome = ? and senha = ?",(nome, senha)).fetchone()
            conn.close()
            if user:
                return redirect(url_for('dash', nome=nome, senha=senha, cargo=cargo))
            else:
                return "Usuário não existe, ou a senha está incorreta. Vale também checar caso a opção Professor/Aluno tenha sido trocada!"
        
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dash():
    nome = request.args.get('nome')
    cargo = request.args.get('cargo')
    return render_template('dashboard.html', nome=nome, cargo=cargo)