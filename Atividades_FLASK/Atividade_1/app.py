from flask import Flask, render_template, request, redirect, url_for

import sqlite3

app = Flask(__name__)

def get_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('pages/index.html')

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['password']
        conexao = get_connection()
        SQL= f"INSERT INTO (email, senha) VALUES ({email}, {senha})"
        conexao.execute(SQL)
        conexao.commit()
        conexao.close()
        return redirect(url_for('index'))

    return render_template('pages/create.html')