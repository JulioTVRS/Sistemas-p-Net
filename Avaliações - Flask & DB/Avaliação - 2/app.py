from flask import Flask, render_template, url_for, request, redirect
import sqlite3

app = Flask(__name__)

def obter_conexao():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('pages/index.html')

@app.route('/create', methods=['GET','POST'])
def create_user():
    if request.method == 'POST':
        nome = request.form['nome']
        conn = obter_conexao()
        conn.execute("INSERT INTO usuarios(nome) VALUES(?)", (nome,))
        conn.commit()
        conn.close()
        return redirect(url_for('listar'))

    return render_template('pages/create-user.html')


@app.route('/listar-usuario')
def listar():
    conn = obter_conexao()
    users = conn.execute('SELECT * FROM usuarios').fetchall()
    conn.close()
    return render_template('pages/listar-users.html', users = users)

@app.route('/<int:id>/listar')
def listar_user(id):
    conn = obter_conexao()
    user = conn.execute("SELECT * FROM usuarios WHERE id = ?", (id,)).fetchone()
    conn.close()
    if user:
        return render_template('pages/show-user.html', user=user)        
    return "Usuário não encontrado"


@app.route('/create_peca', methods=['POST', 'GET'])
def create_peca():
    if request.method == 'POST':
        titulo = request.form['titulo']
        conn = obter_conexao()
        conn.execute("INSERT INTO pecas(titulo) VALUES(?)", (titulo,))
        conn.commit()
        conn.close()
        return redirect(url_for('listar_pecas'))
    return render_template('pages/create-pecas.html')
    
@app.route('/listar_pecas', methods=['GET','POST'])
def listar_pecas():
    remover = request.args.get('remover')
    titulo = request.args.get('titulo')
    
    conn = obter_conexao()
    pecas = conn.execute('SELECT * FROM pecas').fetchall()
    conn.close()

    if remover:
        conn = obter_conexao()
        conn.execute("DELETE FROM pecas WHERE titulo = ?",(titulo,))
        conn.commit()
        pecas = conn.execute('SELECT * FROM pecas').fetchall()
        conn.close()
        return render_template('pages/listar-pecas.html', pecas = pecas)

    return render_template('pages/listar-pecas.html', pecas = pecas) 

@app.route('/<int:id>/listar_peca')
def listar_peca(id):
    conn = obter_conexao()
    peca = conn.execute("SELECT * FROM pecas WHERE id = ?", (id,)).fetchone()
    conn.close()
    if peca:
        return render_template('pages/show-peca.html', peca=peca)
    return "Esta peça não existe";

@app.route('/create_dancas', methods=['GET','POST'])
def create_dancas():
    if request.method == 'POST':
        grupo = request.form['grupo']
        user = request.form['user']
        conn = obter_conexao()
        conn.execute("INSERT INTO dancas(grupo, usuario) VALUES(?, ?)", (grupo, user))
        conn.commit()
        conn.close()
        return render_template('pages/create-dancas.html')

    return render_template('pages/create-dancas.html')