from flask import Flask, render_template, request, url_for, redirect
from database import db
from database.models import User, Book
from database.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registraruser', methods=['POST', 'GET'])
def registraruser():
    if request.method == "POST":
        nome = request.form['nome']
        senha = request.form['senha']

        newUser = User(nome=nome, senha=senha)

        db.session.add(newUser)
        db.session.commit()

        return redirect(url_for('listarusers'))

    return render_template('registraruser.html')

@app.route('/registrarbook', methods=['POST', 'GET'])
def registrarbook():
    if request.method == "POST":
        titulo = request.form['titulo']
        autor = request.form['autor']

        newBook = Book(titulo=titulo, autor=autor)

        db.session.add(newBook)
        db.session.commit()

        return redirect(url_for('listarbooks'))

    return render_template('registrarbook.html')

@app.route('/listarusers')
def listarusers():
    resultado = db.session.query(User).all()
    return render_template('listarusers.html', resultado=resultado)

@app.route('/listarbooks')
def listarbooks():
    resultado = db.session.query(Book).all()
    return render_template('listarbooks.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
